import csv
import hashlib
import unicodedata
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from io import BytesIO
from io import StringIO
from pathlib import Path
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.modules.imports.models import Delivery, ImportHistory

SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}
REQUIRED_COLUMNS = {"nf", "transportadora", "data_coleta", "valor_frete", "percentual_frete"}
XML_NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def parse_uploaded_file(
    upload: UploadFile,
) -> tuple[list[str], list[dict[str, str]], str, str]:
    ext = Path(upload.filename or "").suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="formato de arquivo nao suportado. use CSV ou XLSX",
        )

    raw = upload.file.read()
    if not raw:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="arquivo vazio")

    if ext == ".csv":
        columns, rows = _parse_csv(raw)
    else:
        columns, rows = _parse_xlsx(raw)
    _validate_duplicate_nf(rows)
    _validate_required_fields(rows)
    _validate_financial_fields(rows)
    return columns, rows, ext.replace(".", ""), _hash_bytes(raw)


def persist_import_history(
    db: Session,
    *,
    filename: str,
    file_type: str,
    file_hash: str,
    rows_received: int,
    imported_count: int = 0,
    rejected_count: int = 0,
    duplicates_count: int = 0,
    status: str = "SUCCESS",
) -> ImportHistory:
    history = ImportHistory(
        filename=filename,
        file_type=file_type,
        file_hash=file_hash,
        rows_received=rows_received,
        duplicates_count=duplicates_count,
        imported_count=imported_count,
        rejected_count=rejected_count,
        status=status,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


def persist_deliveries(db: Session, rows: list[dict[str, str]]) -> None:
    # LOG-010: transacao atomica - commit unico ao final
    for row in rows:
        db.add(
            Delivery(
                nf=(row.get("nf") or "").strip(),
                transportadora=(row.get("transportadora") or "").strip(),
                data_coleta=_parse_date(row.get("data_coleta")),
                valor_frete=_parse_decimal(row.get("valor_frete"), field="valor_frete"),
                percentual_frete=_parse_decimal(row.get("percentual_frete"), field="percentual_frete"),
            )
        )
    db.commit()


def list_deliveries(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    nf: str | None = None,
    transportadora: str | None = None,
    data_coleta: str | None = None,
) -> dict[str, any]:
    """List deliveries with pagination and filtering."""
    # Build query
    query = db.query(Delivery)

    # Apply filters
    if nf:
        query = query.filter(Delivery.nf == nf)
    if transportadora:
        query = query.filter(Delivery.transportadora == transportadora)
    if data_coleta:
        try:
            parsed_date = date.fromisoformat(data_coleta)
            query = query.filter(Delivery.data_coleta == parsed_date)
        except ValueError:
            pass  # Invalid date format, ignore filter

    # Get total count
    total = query.count()

    # Apply sorting (created_at desc, then id desc)
    query = query.order_by(Delivery.created_at.desc(), Delivery.id.desc())

    # Apply pagination
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()

    # Convert to dict format
    items_data = []
    for item in items:
        items_data.append({
            "id": item.id,
            "nf": item.nf,
            "transportadora": item.transportadora,
            "data_coleta": item.data_coleta,
            "valor_frete": float(item.valor_frete),
            "percentual_frete": float(item.percentual_frete),
            "created_at": item.created_at,
        })

    return {
        "items": items_data,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


def _parse_csv(raw: bytes) -> tuple[list[str], list[dict[str, str]]]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="csv invalido") from exc

    reader = csv.DictReader(StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="csv sem cabecalho")
    columns = [_normalize_header(c) for c in reader.fieldnames if c and c.strip()]
    _validate_required_columns(columns)
    rows = [
        {_normalize_header(k): (v or "").strip() for k, v in row.items() if k and k.strip()}
        for row in reader
    ]
    # LOG-007: rejeitar CSV com cabecalho mas sem linhas de dados
    if not rows:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="csv sem dados: nenhuma linha encontrada")
    return columns, rows


def _parse_xlsx(raw: bytes) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with ZipFile(BytesIO(raw), "r") as zf:
            xml_bytes = zf.read("xl/worksheets/sheet1.xml")
    except KeyError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="xlsx sem worksheet") from exc
    except BadZipFile as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="xlsx invalido") from exc

    root = ElementTree.fromstring(xml_bytes)
    rows: list[list[str]] = []
    for row in root.findall(".//s:sheetData/s:row", XML_NS):
        values: list[str] = []
        for cell in row.findall("s:c", XML_NS):
            inline_text = cell.find("s:is/s:t", XML_NS)
            value_node = cell.find("s:v", XML_NS)
            if inline_text is not None and inline_text.text is not None:
                values.append(inline_text.text.strip())
            elif value_node is not None and value_node.text is not None:
                values.append(value_node.text.strip())
            else:
                values.append("")
        rows.append(values)

    if not rows:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="xlsx vazio")

    columns = [_normalize_header(c) for c in rows[0] if c.strip()]
    _validate_required_columns(columns)
    data_rows: list[dict[str, str]] = []
    for values in rows[1:]:
        row_map: dict[str, str] = {}
        for idx, col in enumerate(columns):
            row_map[col] = values[idx].strip() if idx < len(values) else ""
        data_rows.append(row_map)
    return columns, data_rows


def _normalize_header(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value.strip().lower())
    without_accents = "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")
    return without_accents.replace(" ", "_")


def _validate_required_columns(columns: list[str]) -> None:
    missing = sorted(REQUIRED_COLUMNS - set(columns))
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"colunas obrigatorias ausentes: {', '.join(missing)}",
        )


def _validate_duplicate_nf_in_db(db: Session, rows: list[dict[str, str]]) -> int:
    # LOG-010: valida duplicidade de NF no banco e retorna contador
    from app.modules.imports.models import Delivery
    nfs = {(row.get("nf") or "").strip() for row in rows}
    existing = db.query(Delivery.nf).filter(Delivery.nf.in_(nfs)).all()
    existing_nfs = {nf for (nf,) in existing}
    return len(existing_nfs)


def _validate_duplicate_nf(rows: list[dict[str, str]]) -> None:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for row in rows:
        nf = (row.get("nf") or "").strip()
        if not nf:
            continue
        if nf in seen:
            duplicates.add(nf)
        else:
            seen.add(nf)
    if duplicates:
        ordered = ", ".join(sorted(duplicates))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"duplicidades detectadas para nf: {ordered}",
        )


def _validate_required_fields(rows: list[dict[str, str]]) -> None:
    # LOG-008: validar campos obrigatorios com valor nao vazio por linha
    for row in rows:
        nf = (row.get("nf") or "").strip()
        if not nf:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="nf obrigatoria: campo nf nao pode ser vazio",
            )
        transportadora = (row.get("transportadora") or "").strip()
        if not transportadora:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="transportadora obrigatoria: campo transportadora nao pode ser vazio",
            )


def _validate_financial_fields(rows: list[dict[str, str]]) -> None:
    for row in rows:
        valor_frete = _parse_decimal(row.get("valor_frete"), field="valor_frete")
        if valor_frete < Decimal("0"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="valor_frete deve ser maior ou igual a 0",
            )

        percentual_frete = _parse_decimal(row.get("percentual_frete"), field="percentual_frete")
        if percentual_frete < Decimal("0") or percentual_frete > Decimal("100"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="percentual_frete deve estar entre 0 e 100",
            )

        _parse_date(row.get("data_coleta"))


def _parse_decimal(value: str | None, *, field: str) -> Decimal:
    raw = (value or "").strip()
    if not raw:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{field} obrigatorio")
    normalized = raw.replace(",", ".")
    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{field} invalido") from exc


def _parse_date(value: str | None):
    raw = (value or "").strip()
    if not raw:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="data_coleta obrigatoria")
    try:
        return datetime.strptime(raw, "%Y-%m-%d").date()
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="data_coleta invalida") from exc


def _hash_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()
