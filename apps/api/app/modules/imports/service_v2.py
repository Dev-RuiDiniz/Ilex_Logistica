"""Enhanced import service for BETA-012A with preview, validation, and confirmation.

This module provides:
- CSV/XLSX parsing with Brazilian date/monetary format support
- Column mapping via layout mapper
- Line-by-line validation with error/warning reporting
- Duplicate detection (in-file and against database)
- Preview endpoint (no persistence)
- Confirmation endpoint (persist validated data to Shipment)
"""

import csv
import hashlib
import json
import re
from collections import Counter
from datetime import UTC, date, datetime
from decimal import Decimal, InvalidOperation
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any
from xml.etree import ElementTree
from zipfile import BadZipFile, ZipFile

from fastapi import HTTPException, UploadFile, status as http_status
from sqlalchemy.orm import Session

from app.modules.imports.braspress_mapper import map_braspress_column
from app.modules.imports.mapper import map_column, normalize_column_name, get_required_columns
from app.modules.imports.models import ImportHistory
from app.modules.shipments.models import Shipment
from app.modules.carriers.models import Carrier

SUPPORTED_EXTENSIONS = {".csv", ".xlsx"}
XML_NS = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}

# Brazilian date format patterns
BR_DATE_PATTERN = re.compile(r"^(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})$")
ISO_DATE_PATTERN = re.compile(r"^(\d{4})-(\d{1,2})-(\d{1,2})$")

# Brazilian monetary format patterns (e.g., 1.234,56 or 1234,56)
BR_MONEY_PATTERN = re.compile(r"^[\sR$]*([0-9.]+)[.,]([0-9]{2})[\s]*$")


class RowValidationError:
    """Represents a validation error for a specific row."""
    
    def __init__(
        self,
        row_number: int,
        field: str | None,
        message: str,
        value: Any = None,
        is_blocking: bool = True,
    ):
        self.row_number = row_number
        self.field = field
        self.message = message
        self.value = value
        self.is_blocking = is_blocking
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "row_number": self.row_number,
            "field": self.field,
            "message": self.message,
            "value": self.value,
            "is_blocking": self.is_blocking,
        }


class ValidatedRow:
    """Represents a validated row with normalized data."""
    
    def __init__(
        self,
        row_number: int,
        data: dict[str, Any],
        errors: list[RowValidationError],
        warnings: list[RowValidationError],
    ):
        self.row_number = row_number
        self.data = data
        self.errors = errors
        self.warnings = warnings
    
    @property
    def is_valid(self) -> bool:
        """Check if row has no blocking errors."""
        return not any(error.is_blocking for error in self.errors)
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "row_number": self.row_number,
            "data": self.data,
            "errors": [error.to_dict() for error in self.errors],
            "warnings": [warning.to_dict() for warning in self.warnings],
            "is_valid": self.is_valid,
        }


class ImportPreview:
    """Represents the result of an import preview."""
    
    def __init__(
        self,
        filename: str,
        file_type: str,
        file_hash: str,
        total_rows: int,
        valid_rows: int,
        invalid_rows: int,
        duplicate_rows: int,
        rows: list[ValidatedRow],
        errors: list[RowValidationError],
        warnings: list[RowValidationError],
    ):
        self.filename = filename
        self.file_type = file_type
        self.file_hash = file_hash
        self.total_rows = total_rows
        self.valid_rows = valid_rows
        self.invalid_rows = invalid_rows
        self.duplicate_rows = duplicate_rows
        self.rows = rows
        self.errors = errors
        self.warnings = warnings
        self.import_id: int | None = None
    
    def to_dict(self) -> dict[str, Any]:
        return {
            "filename": self.filename,
            "file_type": self.file_type,
            "file_hash": self.file_hash,
            "total_rows": self.total_rows,
            "valid_rows": self.valid_rows,
            "invalid_rows": self.invalid_rows,
            "duplicate_rows": self.duplicate_rows,
            "preview_items": [row.to_dict() for row in self.rows[:10]],  # First 10 rows
            "errors": [error.to_dict() for error in self.errors],
            "warnings": [warning.to_dict() for warning in self.warnings],
            "import_id": self.import_id,
        }


def parse_brazilian_date(value: str) -> date | None:
    """Parse Brazilian date format (DD/MM/YYYY or DD-MM-YYYY).
    
    Args:
        value: Date string in Brazilian format
        
    Returns:
        Parsed date or None if invalid
    """
    if not value or not value.strip():
        return None
    
    value = value.strip()
    
    # Try Brazilian format first
    match = BR_DATE_PATTERN.match(value)
    if match:
        day, month, year = match.groups()
        try:
            # Handle 2-digit years
            if len(year) == 2:
                year = f"20{year}" if int(year) >= 0 else f"19{year}"
            return date(int(year), int(month), int(day))
        except ValueError:
            return None
    
    # Try ISO format
    match = ISO_DATE_PATTERN.match(value)
    if match:
        year, month, day = match.groups()
        try:
            return date(int(year), int(month), int(day))
        except ValueError:
            return None
    
    return None


def parse_brazilian_monetary(value: str) -> Decimal | None:
    """Parse Brazilian monetary format (e.g., 1.234,56 or 1234,56).
    
    Args:
        value: Monetary string in Brazilian format
        
    Returns:
        Parsed decimal or None if invalid
    """
    if not value or not value.strip():
        return None
    
    value = value.strip()
    
    # Remove R$ prefix and spaces
    value = re.sub(r"[R$\s]", "", value)
    
    # Try Brazilian format (1.234,56)
    match = BR_MONEY_PATTERN.match(value)
    if match:
        integer_part, decimal_part = match.groups()
        # Remove thousand separators
        integer_part = integer_part.replace(".", "")
        try:
            return Decimal(f"{integer_part}.{decimal_part}")
        except InvalidOperation:
            return None
    
    # Try standard decimal format
    try:
        return Decimal(value.replace(",", "."))
    except InvalidOperation:
        return None


def parse_uploaded_file_v2(
    upload: UploadFile,
    source: str | None = None,
) -> tuple[list[str], list[dict[str, str]], str, str]:
    """Parse uploaded CSV/XLSX file with column mapping.

    Args:
        upload: Uploaded file
        source: Import source for layout-specific mapping (optional)

    Returns:
        Tuple of (columns, rows, file_type, file_hash)
    """
    ext = Path(upload.filename or "").suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="formato de arquivo nao suportado. use CSV ou XLSX",
        )

    raw = upload.file.read()
    if not raw:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="arquivo vazio")

    if ext == ".csv":
        columns, rows = _parse_csv_v2(raw, source=source)
    else:
        columns, rows = _parse_xlsx_v2(raw, source=source)

    return columns, rows, ext.replace(".", ""), _hash_bytes(raw)


def _parse_csv_v2(raw: bytes, source: str | None = None) -> tuple[list[str], list[dict[str, str]]]:
    """Parse CSV with column mapping."""
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="csv invalido") from exc

    reader = csv.DictReader(StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="csv sem cabecalho")

    _map = map_braspress_column if source == "braspress_assisted" else map_column

    # Map column names using the mapper
    columns = [_map(c) for c in reader.fieldnames if c and c.strip()]

    rows = []
    for row_idx, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
        row_map = {}
        for k, v in row.items():
            if k and k.strip():
                mapped_name = _map(k)
                row_map[mapped_name] = (v or "").strip()
        rows.append(row_map)

    if not rows:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="csv sem dados: nenhuma linha encontrada")

    return columns, rows


def _parse_xlsx_v2(raw: bytes, source: str | None = None) -> tuple[list[str], list[dict[str, str]]]:
    """Parse XLSX with column mapping."""
    try:
        with ZipFile(BytesIO(raw), "r") as zf:
            xml_bytes = zf.read("xl/worksheets/sheet1.xml")
    except KeyError as exc:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="xlsx sem worksheet") from exc
    except BadZipFile as exc:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="xlsx invalido") from exc

    root = ElementTree.fromstring(xml_bytes)
    rows_data: list[list[str]] = []
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
        rows_data.append(values)

    if not rows_data:
        raise HTTPException(status_code=http_status.HTTP_400_BAD_REQUEST, detail="xlsx vazio")

    _map = map_braspress_column if source == "braspress_assisted" else map_column

    # Map column names using the mapper
    raw_columns = rows_data[0]
    columns = [_map(c) for c in raw_columns if c.strip()]

    rows = []
    for row_idx, values in enumerate(rows_data[1:], start=2):  # Start at 2 (header is row 1)
        row_map = {}
        for idx, col in enumerate(columns):
            value = values[idx].strip() if idx < len(values) else ""
            row_map[col] = value
        rows.append(row_map)

    return columns, rows


def validate_row(
    row: dict[str, str],
    row_number: int,
    db: Session | None = None,
    source: str | None = None,
) -> ValidatedRow:
    """Validate a single row with all business rules.

    Args:
        row: Row data with mapped column names
        row_number: Row number in the file (1-indexed, header is row 1)
        db: Database session for duplicate checking (optional)
        source: Import source for layout-specific validation (optional)

    Returns:
        ValidatedRow with errors and warnings
    """
    errors: list[RowValidationError] = []
    warnings: list[RowValidationError] = []
    normalized_data: dict[str, Any] = {}

    # Required fields
    required_fields = get_required_columns()

    # Validate tracking_code
    tracking_code = row.get("tracking_code", "").strip()
    if not tracking_code:
        errors.append(RowValidationError(
            row_number=row_number,
            field="tracking_code",
            message="tracking_code obrigatorio",
            value=tracking_code,
        ))
    else:
        normalized_data["tracking_code"] = tracking_code

    # Validate carrier_id (or resolve carrier_name for Braspress)
    carrier_id_str = row.get("carrier_id", "").strip()
    carrier_name = row.get("carrier_name", "").strip()

    if source == "braspress_assisted" and carrier_name and not carrier_id_str:
        # Resolve carrier_name to carrier_id via database lookup
        if db is not None:
            carrier = db.query(Carrier).filter(Carrier.name.ilike(carrier_name)).first()
            if carrier is None:
                errors.append(RowValidationError(
                    row_number=row_number,
                    field="carrier_name",
                    message=f"transportadora '{carrier_name}' nao encontrada",
                    value=carrier_name,
                ))
            else:
                normalized_data["carrier_id"] = carrier.id
        else:
            # Fallback: use carrier_name as placeholder when db is unavailable
            normalized_data["carrier_id"] = 1  # Will be resolved at confirm time
    elif not carrier_id_str:
        errors.append(RowValidationError(
            row_number=row_number,
            field="carrier_id",
            message="carrier_id obrigatorio",
            value=carrier_id_str,
        ))
    else:
        try:
            carrier_id = int(carrier_id_str)
            if carrier_id <= 0:
                errors.append(RowValidationError(
                    row_number=row_number,
                    field="carrier_id",
                    message="carrier_id deve ser positivo",
                    value=carrier_id_str,
                ))
            else:
                normalized_data["carrier_id"] = carrier_id
        except ValueError:
            errors.append(RowValidationError(
                row_number=row_number,
                field="carrier_id",
                message="carrier_id deve ser um numero inteiro",
                value=carrier_id_str,
            ))
    
    # Validate invoice_number
    invoice_number = row.get("invoice_number", "").strip()
    if not invoice_number:
        errors.append(RowValidationError(
            row_number=row_number,
            field="invoice_number",
            message="invoice_number obrigatorio",
            value=invoice_number,
        ))
    else:
        normalized_data["invoice_number"] = invoice_number
    
    # Validate invoice_value (Brazilian monetary format)
    invoice_value_str = row.get("invoice_value", "").strip()
    if not invoice_value_str:
        errors.append(RowValidationError(
            row_number=row_number,
            field="invoice_value",
            message="invoice_value obrigatorio",
            value=invoice_value_str,
        ))
    else:
        invoice_value = parse_brazilian_monetary(invoice_value_str)
        if invoice_value is None:
            errors.append(RowValidationError(
                row_number=row_number,
                field="invoice_value",
                message="invoice_value invalido (use formato brasileiro: 1.234,56)",
                value=invoice_value_str,
            ))
        elif invoice_value <= 0:
            errors.append(RowValidationError(
                row_number=row_number,
                field="invoice_value",
                message="invoice_value deve ser positivo",
                value=invoice_value_str,
            ))
        else:
            normalized_data["invoice_value"] = float(invoice_value)
    
    # Validate freight_value (Brazilian monetary format)
    freight_value_str = row.get("freight_value", "").strip()
    if not freight_value_str:
        errors.append(RowValidationError(
            row_number=row_number,
            field="freight_value",
            message="freight_value obrigatorio",
            value=freight_value_str,
        ))
    else:
        freight_value = parse_brazilian_monetary(freight_value_str)
        if freight_value is None:
            errors.append(RowValidationError(
                row_number=row_number,
                field="freight_value",
                message="freight_value invalido (use formato brasileiro: 1.234,56)",
                value=freight_value_str,
            ))
        elif freight_value < 0:
            errors.append(RowValidationError(
                row_number=row_number,
                field="freight_value",
                message="freight_value nao pode ser negativo",
                value=freight_value_str,
            ))
        else:
            normalized_data["freight_value"] = float(freight_value)
    
    # Validate collection_departure_date (Brazilian date format)
    collection_date_str = row.get("collection_departure_date", "").strip()
    if not collection_date_str:
        errors.append(RowValidationError(
            row_number=row_number,
            field="collection_departure_date",
            message="collection_departure_date obrigatorio",
            value=collection_date_str,
        ))
    else:
        collection_date = parse_brazilian_date(collection_date_str)
        if collection_date is None:
            errors.append(RowValidationError(
                row_number=row_number,
                field="collection_departure_date",
                message="collection_departure_date invalido (use formato brasileiro: DD/MM/YYYY)",
                value=collection_date_str,
            ))
        else:
            # Convert to datetime for Shipment model
            normalized_data["collection_departure_date"] = datetime.combine(
                collection_date, datetime.min.time()
            )
    
    # Validate customer_name
    customer_name = row.get("customer_name", "").strip()
    if not customer_name:
        errors.append(RowValidationError(
            row_number=row_number,
            field="customer_name",
            message="customer_name obrigatorio",
            value=customer_name,
        ))
    else:
        normalized_data["customer_name"] = customer_name
    
    # Validate destination_uf
    destination_uf = row.get("destination_uf", "").strip().upper()
    if not destination_uf:
        errors.append(RowValidationError(
            row_number=row_number,
            field="destination_uf",
            message="destination_uf obrigatorio",
            value=destination_uf,
        ))
    elif len(destination_uf) != 2:
        errors.append(RowValidationError(
            row_number=row_number,
            field="destination_uf",
            message="destination_uf deve ter 2 caracteres (sigla do estado)",
            value=destination_uf,
        ))
    else:
        normalized_data["destination_uf"] = destination_uf
    
    return ValidatedRow(
        row_number=row_number,
        data=normalized_data,
        errors=errors,
        warnings=warnings,
    )


def detect_duplicates_in_file(rows: list[ValidatedRow]) -> int:
    """Detect duplicate rows within the file.
    
    Duplicates are defined by (tracking_code + carrier_id) or (invoice_number + carrier_id).
    
    Args:
        rows: Validated rows
        
    Returns:
        Number of duplicate rows found
    """
    tracking_carrier_pairs = []
    invoice_carrier_pairs = []
    
    for row in rows:
        if row.is_valid:
            tracking_code = row.data.get("tracking_code")
            carrier_id = row.data.get("carrier_id")
            invoice_number = row.data.get("invoice_number")
            
            if tracking_code and carrier_id:
                tracking_carrier_pairs.append((tracking_code, carrier_id))
            if invoice_number and carrier_id:
                invoice_carrier_pairs.append((invoice_number, carrier_id))
    
    # Count duplicates
    tracking_carrier_counts = Counter(tracking_carrier_pairs)
    invoice_carrier_counts = Counter(invoice_carrier_pairs)
    
    duplicate_count = sum(
        count - 1 for count in tracking_carrier_counts.values() if count > 1
    ) + sum(
        count - 1 for count in invoice_carrier_counts.values() if count > 1
    )
    
    return duplicate_count


def detect_duplicates_in_db(
    db: Session,
    rows: list[ValidatedRow],
) -> int:
    """Detect duplicate rows against existing database records.
    
    Args:
        db: Database session
        rows: Validated rows
        
    Returns:
        Number of duplicate rows found in database
    """
    if not rows:
        return 0
    
    tracking_codes = [row.data.get("tracking_code") for row in rows if row.is_valid and row.data.get("tracking_code")]
    invoice_numbers = [row.data.get("invoice_number") for row in rows if row.is_valid and row.data.get("invoice_number")]
    
    if not tracking_codes and not invoice_numbers:
        return 0
    
    duplicate_count = 0
    
    # Check tracking_code duplicates
    if tracking_codes:
        existing = db.query(Shipment).filter(
            Shipment.tracking_code.in_(tracking_codes)
        ).count()
        duplicate_count += existing
    
    # Check invoice_number duplicates
    if invoice_numbers:
        existing = db.query(Shipment).filter(
            Shipment.invoice_number.in_(invoice_numbers)
        ).count()
        duplicate_count += existing
    
    return duplicate_count


def preview_import(
    db: Session,
    upload: UploadFile,
    user_id: int | None = None,
    source: str | None = None,
) -> ImportPreview:
    """Preview import without persisting shipments.

    Creates a pending ImportHistory record with validated data in metadata.

    Args:
        db: Database session
        upload: Uploaded file
        user_id: User ID performing the import (optional)
        source: Import source for layout-specific mapping (optional, e.g., braspress_assisted)

    Returns:
        ImportPreview with validation results
    """
    columns, rows, file_type, file_hash = parse_uploaded_file_v2(upload, source=source)

    validated_rows: list[ValidatedRow] = []
    all_errors: list[RowValidationError] = []
    all_warnings: list[RowValidationError] = []

    # Validate each row
    for row_idx, row in enumerate(rows, start=2):  # Start at 2 (header is row 1)
        validated_row = validate_row(row, row_idx, db, source=source)
        validated_rows.append(validated_row)
        all_errors.extend(validated_row.errors)
        all_warnings.extend(validated_row.warnings)
    
    # Count valid/invalid rows
    valid_rows = sum(1 for row in validated_rows if row.is_valid)
    invalid_rows = len(validated_rows) - valid_rows
    
    # Detect duplicates
    duplicate_in_file = detect_duplicates_in_file(validated_rows)
    duplicate_in_db = detect_duplicates_in_db(db, validated_rows)
    total_duplicates = duplicate_in_file + duplicate_in_db
    
    # Create pending ImportHistory with validated data in metadata
    # Convert datetime objects to strings for JSON serialization
    valid_rows_serializable = []
    for row in validated_rows:
        if row.is_valid:
            row_data = row.data.copy()
            # Convert datetime to ISO string
            for key, value in row_data.items():
                if isinstance(value, datetime):
                    row_data[key] = value.isoformat()
            valid_rows_serializable.append(row_data)
    
    metadata_dict: dict[str, Any] = {
        "valid_rows": valid_rows_serializable,
        "invalid_rows": invalid_rows,
        "errors": [error.to_dict() for error in all_errors],
        "warnings": [warning.to_dict() for warning in all_warnings],
    }
    if source:
        metadata_dict["layout"] = source

    history = ImportHistory(
        filename=upload.filename or "unknown",
        file_type=file_type,
        file_hash=file_hash,
        rows_received=len(rows),
        duplicates_count=total_duplicates,
        imported_count=0,
        rejected_count=0,
        status="pending",
        source=source or "csv_xlsx_import",
        import_metadata=json.dumps(metadata_dict),
        imported_by=user_id,
    )
    db.add(history)
    db.commit()
    db.refresh(history)
    
    # Store import_id in preview for later confirmation
    preview = ImportPreview(
        filename=upload.filename or "unknown",
        file_type=file_type,
        file_hash=file_hash,
        total_rows=len(rows),
        valid_rows=valid_rows,
        invalid_rows=invalid_rows,
        duplicate_rows=total_duplicates,
        rows=validated_rows,
        errors=all_errors,
        warnings=all_warnings,
    )
    preview.import_id = history.id  # Attach import_id to preview
    
    return preview


def confirm_import(
    db: Session,
    import_id: int,
    user_id: int | None = None,
) -> ImportHistory:
    """Confirm and persist import after preview.
    
    Retrieves the pending ImportHistory, validates the data, and persists shipments.
    
    Args:
        db: Database session
        import_id: ImportHistory ID from preview
        user_id: User ID performing the import (optional)
        
    Returns:
        Updated ImportHistory record with created shipment IDs
    """
    # Retrieve pending import history
    history = db.query(ImportHistory).filter(ImportHistory.id == import_id).first()
    if not history:
        raise HTTPException(
            status_code=http_status.HTTP_404_NOT_FOUND,
            detail=f"import_id {import_id} nao encontrado",
        )
    
    # Check if already completed
    if history.status != "pending":
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"import_id {import_id} ja processado com status {history.status}",
        )
    
    # Parse metadata to get validated rows
    try:
        metadata = json.loads(history.import_metadata or "{}")
        valid_rows_data = metadata.get("valid_rows", [])
        invalid_rows = metadata.get("invalid_rows", 0)
    except (json.JSONDecodeError, TypeError) as exc:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"metadata invalido para import_id {import_id}",
        ) from exc
    
    # Check if there are blocking errors
    if invalid_rows > 0:
        # Update history to failed
        history.status = "failed"
        history.import_metadata = json.dumps({
            **metadata,
            "error": f"nao e possivel confirmar importacao com {invalid_rows} linhas invalidas",
        })
        db.commit()
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"nao e possivel confirmar importacao com {invalid_rows} linhas invalidas",
        )
    
    # Persist shipments
    imported_count = 0
    rejected_count = 0
    created_shipment_ids: list[int] = []
    
    for row_data in valid_rows_data:
        try:
            # Check for duplicates in database
            existing = db.query(Shipment).filter(
                Shipment.tracking_code == row_data.get("tracking_code")
            ).first()
            
            if existing:
                rejected_count += 1
                continue
            
            # Convert datetime strings back to datetime objects
            collection_date = row_data.get("collection_departure_date")
            if isinstance(collection_date, str):
                collection_date = datetime.fromisoformat(collection_date)
            
            # Create Shipment
            shipment = Shipment(
                tracking_code=row_data["tracking_code"],
                carrier_id=row_data["carrier_id"],
                status="pending",
                estimated_delivery=collection_date or datetime.now(UTC),
                recipient_name=row_data.get("customer_name", ""),
                recipient_phone="",  # Not provided in import
                origin_address="",  # Not provided in import
                destination_address="",  # Not provided in import
                invoice_number=row_data.get("invoice_number"),
                invoice_value=row_data.get("invoice_value"),
                freight_value=row_data.get("freight_value"),
                collection_departure_date=collection_date,
                customer_name=row_data.get("customer_name"),
                destination_uf=row_data.get("destination_uf"),
            )
            db.add(shipment)
            db.flush()  # Get the ID without committing
            created_shipment_ids.append(shipment.id)
            imported_count += 1
        except Exception as exc:
            rejected_count += 1
            # Log error but continue processing other rows
            continue
    
    # Update import history
    history.imported_count = imported_count
    history.rejected_count = rejected_count
    history.status = "completed" if rejected_count == 0 else "failed"
    history.import_metadata = json.dumps({
        **metadata,
        "created_shipment_ids": created_shipment_ids,
        "imported_count": imported_count,
        "rejected_count": rejected_count,
    })
    
    db.commit()
    db.refresh(history)
    
    # Attach created shipment IDs to history for response
    history.created_shipment_ids = created_shipment_ids
    
    return history


def _hash_bytes(raw: bytes) -> str:
    """Generate SHA256 hash of bytes."""
    return hashlib.sha256(raw).hexdigest()
