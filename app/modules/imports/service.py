import csv
import hashlib
import unicodedata
from io import BytesIO
from io import StringIO
from pathlib import Path
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.modules.imports.models import ImportHistory

SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}
REQUIRED_COLUMNS = {"nf", "transportadora"}
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
    return columns, rows, ext.replace(".", ""), _hash_bytes(raw)


def persist_import_history(
    db: Session,
    *,
    filename: str,
    file_type: str,
    file_hash: str,
    rows_received: int,
) -> ImportHistory:
    history = ImportHistory(
        filename=filename,
        file_type=file_type,
        file_hash=file_hash,
        rows_received=rows_received,
        duplicates_count=0,
        status="SUCCESS",
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    return history


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
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def _validate_required_columns(columns: list[str]) -> None:
    missing = sorted(REQUIRED_COLUMNS - set(columns))
    if missing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"colunas obrigatorias ausentes: {', '.join(missing)}",
        )


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


def _hash_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()
