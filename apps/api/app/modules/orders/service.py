import csv
import hashlib
import json
import re
from collections import Counter
from datetime import date
from decimal import Decimal, InvalidOperation
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.modules.imports.models import ImportHistory
from app.modules.orders.models import Order

REQUIRED_COLUMNS = [
    "source",
    "external_number",
    "order_date",
    "customer_name",
    "origin_zip",
    "origin_uf",
    "destination_zip",
    "destination_uf",
    "weight_kg",
    "volume_count",
    "goods_value",
    "currency",
]
VALID_UFS = {
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
    "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
}
MAX_FILE_SIZE = 20 * 1024 * 1024
XML_NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def preview_order_import(db: Session, upload: UploadFile, user_id: int) -> dict[str, Any]:
    filename = upload.filename or "unknown"
    extension = Path(filename).suffix.lower()
    if extension not in {".csv", ".xlsx"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="use arquivo CSV ou XLSX")
    raw = upload.file.read(MAX_FILE_SIZE + 1)
    if not raw:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="arquivo vazio")
    if len(raw) > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="arquivo excede 20 MB")

    columns, rows = _parse_csv(raw) if extension == ".csv" else _parse_xlsx(raw)
    missing = [column for column in REQUIRED_COLUMNS if column not in columns]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"colunas obrigatorias ausentes: {', '.join(missing)}",
        )

    natural_keys = [(row.get("source", "").strip(), row.get("external_number", "").strip()) for row in rows]
    counts = Counter(natural_keys)
    existing = {
        (source, external_number)
        for source, external_number in db.query(Order.source, Order.external_number).filter(
            Order.source.in_({key[0] for key in natural_keys})
        )
    }
    validated: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    duplicate_rows = 0
    for row_number, raw_row in enumerate(rows, start=2):
        row_errors, normalized = _validate_row(raw_row, row_number)
        key = (normalized.get("source", ""), normalized.get("external_number", ""))
        if counts[key] > 1:
            duplicate_rows += 1
            row_errors.append(_error(row_number, "external_number", "pedido duplicado no arquivo", key[1]))
        if key in existing:
            warnings.append(_error(row_number, "external_number", "pedido existente sera atualizado", key[1]))
        errors.extend(row_errors)
        validated.append({"row_number": row_number, "data": normalized, "errors": row_errors, "is_valid": not row_errors})

    valid = [item["data"] for item in validated if item["is_valid"]]
    file_hash = hashlib.sha256(raw).hexdigest()
    metadata = json.dumps(
        {"rows": valid, "errors": errors, "warnings": warnings}, default=str, ensure_ascii=False
    )
    history = ImportHistory(
        filename=filename,
        file_type=extension[1:],
        file_hash=file_hash,
        rows_received=len(rows),
        duplicates_count=duplicate_rows,
        imported_count=0,
        rejected_count=len(rows) - len(valid),
        status="PENDING",
        source="orders_erp",
        import_metadata=metadata,
        imported_by=user_id,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return {
        "import_id": history.id,
        "filename": filename,
        "file_hash": file_hash,
        "total_rows": len(rows),
        "valid_rows": len(valid),
        "invalid_rows": len(rows) - len(valid),
        "duplicate_rows": duplicate_rows,
        "preview_items": validated[:10],
        "errors": errors,
        "warnings": warnings,
    }


def confirm_order_import(db: Session, import_id: int, user_id: int) -> ImportHistory:
    history = db.get(ImportHistory, import_id)
    if history is None or history.source != "orders_erp":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="preview de pedidos nao encontrado")
    if history.status == "CONFIRMED":
        return history
    previous = (
        db.query(ImportHistory)
        .filter(
            ImportHistory.source == "orders_erp",
            ImportHistory.file_hash == history.file_hash,
            ImportHistory.status == "CONFIRMED",
        )
        .order_by(ImportHistory.id)
        .first()
    )
    if previous is not None:
        return previous
    try:
        payload = json.loads(history.import_metadata or "{}")
        rows = payload.get("rows", [])
        for row in rows:
            order = (
                db.query(Order)
                .filter(Order.source == row["source"], Order.external_number == row["external_number"])
                .one_or_none()
            )
            values = _order_values(row, history.id)
            if order is None:
                order = Order(**values, created_by=user_id)
                db.add(order)
            else:
                for field, value in values.items():
                    setattr(order, field, value)
        history.imported_count = len(rows)
        history.status = "CONFIRMED"
        history.imported_by = user_id
        db.commit()
        db.refresh(history)
        return history
    except Exception:
        db.rollback()
        raise


def list_orders(
    db: Session,
    page: int,
    page_size: int,
    status_filter: str | None,
    source: str | None,
    external_number: str | None,
) -> dict[str, Any]:
    query = db.query(Order)
    if status_filter:
        query = query.filter(Order.status == status_filter)
    if source:
        query = query.filter(Order.source == source)
    if external_number:
        query = query.filter(Order.external_number.contains(external_number))
    total = query.count()
    items = query.order_by(Order.order_date.desc(), Order.id.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def _order_values(row: dict[str, Any], import_history_id: int) -> dict[str, Any]:
    return {
        **row,
        "order_date": date.fromisoformat(row["order_date"]),
        "weight_kg": Decimal(row["weight_kg"]),
        "volume_count": int(row["volume_count"]),
        "goods_value": Decimal(row["goods_value"]),
        "import_history_id": import_history_id,
        "status": "active",
    }


def _parse_csv(raw: bytes) -> tuple[list[str], list[dict[str, str]]]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="CSV deve usar UTF-8") from exc
    reader = csv.DictReader(StringIO(text))
    columns = [str(column).strip().lower() for column in (reader.fieldnames or [])]
    if not columns:
        raise HTTPException(status_code=400, detail="arquivo sem cabecalho")
    rows = [{str(key).strip().lower(): (value or "").strip() for key, value in row.items()} for row in reader]
    if not rows:
        raise HTTPException(status_code=400, detail="arquivo sem linhas")
    return columns, rows


def _parse_xlsx(raw: bytes) -> tuple[list[str], list[dict[str, str]]]:
    try:
        with ZipFile(BytesIO(raw)) as archive:
            sheet = archive.read("xl/worksheets/sheet1.xml")
            if b"<f" in sheet:
                raise HTTPException(status_code=400, detail="formulas nao sao permitidas")
            shared: list[str] = []
            if "xl/sharedStrings.xml" in archive.namelist():
                shared_root = ElementTree.fromstring(archive.read("xl/sharedStrings.xml"))
                shared = ["".join(node.itertext()) for node in shared_root.findall("s:si", XML_NS)]
    except (BadZipFile, KeyError, ElementTree.ParseError) as exc:
        raise HTTPException(status_code=400, detail="XLSX invalido") from exc
    root = ElementTree.fromstring(sheet)
    matrix: list[list[str]] = []
    for xml_row in root.findall(".//s:sheetData/s:row", XML_NS):
        values: list[str] = []
        for cell in xml_row.findall("s:c", XML_NS):
            value = cell.find("s:v", XML_NS)
            inline = cell.find("s:is/s:t", XML_NS)
            text = inline.text if inline is not None else (value.text if value is not None else "")
            if cell.get("t") == "s" and text:
                text = shared[int(text)]
            values.append((text or "").strip())
        matrix.append(values)
    if len(matrix) < 2:
        raise HTTPException(status_code=400, detail="XLSX sem linhas")
    columns = [column.strip().lower() for column in matrix[0]]
    return columns, [dict(zip(columns, values, strict=False)) for values in matrix[1:]]


def _validate_row(row: dict[str, str], row_number: int) -> tuple[list[dict[str, Any]], dict[str, str]]:
    normalized = {field: (row.get(field) or "").strip() for field in REQUIRED_COLUMNS}
    normalized["origin_uf"] = normalized["origin_uf"].upper()
    normalized["destination_uf"] = normalized["destination_uf"].upper()
    normalized["currency"] = normalized["currency"].upper()
    errors: list[dict[str, Any]] = []
    for field, value in normalized.items():
        if not value:
            errors.append(_error(row_number, field, "campo obrigatorio", value))
        if value.startswith(("=", "+", "@")) or (value.startswith("-") and not _is_decimal(value)):
            errors.append(_error(row_number, field, "conteudo ativo nao permitido", value))
    try:
        date.fromisoformat(normalized["order_date"])
    except ValueError:
        errors.append(_error(row_number, "order_date", "data deve usar AAAA-MM-DD", normalized["order_date"]))
    for field in ("origin_zip", "destination_zip"):
        if not re.fullmatch(r"\d{8}", normalized[field]):
            errors.append(_error(row_number, field, "CEP deve conter oito digitos", normalized[field]))
    for field in ("origin_uf", "destination_uf"):
        if normalized[field] not in VALID_UFS:
            errors.append(_error(row_number, field, "UF invalida", normalized[field]))
    for field in ("weight_kg", "goods_value"):
        if not _is_positive_decimal(normalized[field]):
            errors.append(_error(row_number, field, "valor deve ser positivo", normalized[field]))
    try:
        if int(normalized["volume_count"]) <= 0:
            raise ValueError
    except ValueError:
        errors.append(_error(row_number, "volume_count", "volumes deve ser inteiro positivo", normalized["volume_count"]))
    if normalized["currency"] != "BRL":
        errors.append(_error(row_number, "currency", "apenas BRL e aceito no MVP", normalized["currency"]))
    return errors, normalized


def _is_decimal(value: str) -> bool:
    try:
        Decimal(value)
        return True
    except InvalidOperation:
        return False


def _is_positive_decimal(value: str) -> bool:
    try:
        return Decimal(value) > 0
    except InvalidOperation:
        return False


def _error(row_number: int, field: str, message: str, value: Any) -> dict[str, Any]:
    return {"row_number": row_number, "field": field, "message": message, "value": value}
