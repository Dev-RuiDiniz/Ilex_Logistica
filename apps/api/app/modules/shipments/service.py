import csv
import io
import json
from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from app.modules.carriers.models import Carrier
from app.modules.shipments.models import ImportHistory, Shipment, ShipmentTreatment
from app.modules.shipments.schemas import CSVRowError


def calculate_delay_days(due_date: datetime | None, reference_date: datetime | None = None) -> int:
    if not due_date:
        return 0
    ref_date = reference_date or datetime.now(UTC)
    delta = ref_date - due_date
    return max(0, delta.days)


def classify_criticality(delay_days: int, amount: float | None = None) -> str:
    if delay_days == 0:
        return "normal"
    elif delay_days <= 7:
        return "baixa"
    elif delay_days <= 30:
        return "media"
    else:
        return "alta"


def list_shipments(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    carrier_id: int | None = None,
    tracking_code: str | None = None,
    invoice_number: str | None = None,
    fiscal_document: str | None = None,
    criticality: str | None = None,
    estimated_delivery_from: str | None = None,
    estimated_delivery_to: str | None = None,
    due_date_from: str | None = None,
    due_date_to: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
) -> dict[str, Any]:
    """List shipments with pagination, filtering and sorting."""
    from app.modules.shipments.models import Shipment

    # Build query
    query = db.query(Shipment)

    # Apply filters
    if status:
        query = query.filter(Shipment.status == status)
    if carrier_id:
        query = query.filter(Shipment.carrier_id == carrier_id)
    if tracking_code:
        query = query.filter(Shipment.tracking_code.ilike(f"%{tracking_code}%"))
    if invoice_number:
        query = query.filter(Shipment.invoice_number.ilike(f"%{invoice_number}%"))
    if fiscal_document:
        query = query.filter(Shipment.fiscal_document.ilike(f"%{fiscal_document}%"))
    if criticality:
        query = query.filter(Shipment.criticality == criticality)
    
    if estimated_delivery_from:
        try:
            from_date = datetime.fromisoformat(estimated_delivery_from.replace("Z", "+00:00"))
            query = query.filter(Shipment.estimated_delivery >= from_date)
        except (ValueError, AttributeError):
            pass
    
    if estimated_delivery_to:
        try:
            to_date = datetime.fromisoformat(estimated_delivery_to.replace("Z", "+00:00"))
            query = query.filter(Shipment.estimated_delivery <= to_date)
        except (ValueError, AttributeError):
            pass
    
    if due_date_from:
        try:
            from_date = datetime.fromisoformat(due_date_from.replace("Z", "+00:00"))
            query = query.filter(Shipment.due_date >= from_date)
        except (ValueError, AttributeError):
            pass
    
    if due_date_to:
        try:
            to_date = datetime.fromisoformat(due_date_to.replace("Z", "+00:00"))
            query = query.filter(Shipment.due_date <= to_date)
        except (ValueError, AttributeError):
            pass

    # Get total count
    total = query.count()

    # Apply sorting
    sort_column = getattr(Shipment, sort_by, Shipment.created_at)
    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    # Apply pagination
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()

    # Convert to dict format
    items_data = []
    for item in items:
        items_data.append({
            "id": item.id,
            "tracking_code": item.tracking_code,
            "carrier_id": item.carrier_id,
            "status": item.status,
            "estimated_delivery": item.estimated_delivery,
            "recipient_name": item.recipient_name,
            "recipient_phone": item.recipient_phone,
            "origin_address": item.origin_address,
            "destination_address": item.destination_address,
            "invoice_number": item.invoice_number,
            "invoice_key": item.invoice_key,
            "fiscal_document": item.fiscal_document,
            "amount": float(item.amount) if item.amount else None,
            "due_date": item.due_date,
            "delay_days": item.delay_days,
            "criticality": item.criticality,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        })

    return {
        "items": items_data,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


def list_exception_shipments(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    criticality: str | None = None,
    estimated_delivery_from: str | None = None,
    estimated_delivery_to: str | None = None,
    due_date_from: str | None = None,
    due_date_to: str | None = None,
    sort_by: str = "delay_days",
    sort_order: str = "desc",
) -> dict[str, Any]:
    from app.modules.shipments.models import Shipment

    query = db.query(Shipment).filter((Shipment.delay_days > 0) | (Shipment.criticality != "normal"))

    if status:
        query = query.filter(Shipment.status == status)
    if criticality:
        query = query.filter(Shipment.criticality == criticality)
    if estimated_delivery_from:
        try:
            from_date = datetime.fromisoformat(estimated_delivery_from.replace("Z", "+00:00"))
            query = query.filter(Shipment.estimated_delivery >= from_date)
        except (ValueError, AttributeError):
            pass
    if estimated_delivery_to:
        try:
            to_date = datetime.fromisoformat(estimated_delivery_to.replace("Z", "+00:00"))
            query = query.filter(Shipment.estimated_delivery <= to_date)
        except (ValueError, AttributeError):
            pass
    if due_date_from:
        try:
            from_date = datetime.fromisoformat(due_date_from.replace("Z", "+00:00"))
            query = query.filter(Shipment.due_date >= from_date)
        except (ValueError, AttributeError):
            pass
    if due_date_to:
        try:
            to_date = datetime.fromisoformat(due_date_to.replace("Z", "+00:00"))
            query = query.filter(Shipment.due_date <= to_date)
        except (ValueError, AttributeError):
            pass

    total = query.count()
    sort_column = getattr(Shipment, sort_by, Shipment.delay_days)
    query = query.order_by(sort_column.desc() if sort_order.lower() == "desc" else sort_column.asc())
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()

    return {
        "items": [
            {
                "id": item.id,
                "tracking_code": item.tracking_code,
                "carrier_id": item.carrier_id,
                "status": item.status,
                "estimated_delivery": item.estimated_delivery,
                "recipient_name": item.recipient_name,
                "recipient_phone": item.recipient_phone,
                "origin_address": item.origin_address,
                "destination_address": item.destination_address,
                "invoice_number": item.invoice_number,
                "invoice_key": item.invoice_key,
                "fiscal_document": item.fiscal_document,
                "amount": float(item.amount) if item.amount else None,
                "due_date": item.due_date,
                "delay_days": item.delay_days,
                "criticality": item.criticality,
                "created_at": item.created_at,
                "updated_at": item.updated_at,
            }
            for item in items
        ],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


REQUIRED_COLUMNS = [
    "tracking_code",
    "carrier_name",
    "estimated_delivery",
    "recipient_name",
    "recipient_phone",
    "origin_address",
    "destination_address",
]


def parse_csv_file(
    file_content: bytes,
    db: Session,
    user_id: int,
    filename: str,
) -> dict[str, Any]:
    """Parse CSV file and validate rows."""
    errors: list[CSVRowError] = []
    valid_rows: list[dict[str, Any]] = []
    total_rows = 0

    try:
        csv_file = io.TextIOWrapper(io.BytesIO(file_content), encoding="utf-8")
        reader = csv.DictReader(csv_file)

        # Validate required columns
        missing_columns = set(REQUIRED_COLUMNS) - set(reader.fieldnames or [])
        if missing_columns:
            return {
                "status": "failed",
                "total_rows": 0,
                "valid_rows": 0,
                "invalid_rows": 0,
                "errors": [
                    CSVRowError(
                        row_number=0,
                        field="columns",
                        message=f"colunas obrigatorias faltando: {', '.join(missing_columns)}",
                    )
                ],
            }

        # Validate each row
        for row_number, row in enumerate(reader, start=1):
            total_rows += 1
            row_errors = []

            # Check required fields
            for col in REQUIRED_COLUMNS:
                value = row.get(col, "")
                if not value or not str(value).strip():
                    row_errors.append(
                        CSVRowError(
                            row_number=row_number,
                            field=col,
                            message="campo obrigatorio vazio",
                            value=value,
                        )
                    )

            # Validate carrier exists
            carrier_name = row.get("carrier_name", "").strip()
            if carrier_name:
                carrier = db.query(Carrier).filter(Carrier.name == carrier_name).first()
                if not carrier:
                    row_errors.append(
                        CSVRowError(
                            row_number=row_number,
                            field="carrier_name",
                            message="transportadora nao encontrada",
                            value=carrier_name,
                        )
                    )

            # Validate date format manually
            estimated_delivery = row.get("estimated_delivery", "")
            if estimated_delivery and estimated_delivery.strip():
                try:
                    datetime.fromisoformat(estimated_delivery.replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    row_errors.append(
                        CSVRowError(
                            row_number=row_number,
                            field="estimated_delivery",
                            message="formato de data invalido, use ISO 8601 (YYYY-MM-DD)",
                            value=estimated_delivery,
                        )
                    )

            if row_errors:
                errors.extend(row_errors)
            else:
                valid_rows.append(row)

        # Create import history
        try:
            import_history = ImportHistory(
                file_name=filename,
                status="validated",
                total_rows=total_rows,
                valid_rows=len(valid_rows),
                invalid_rows=len(errors),
                imported_count=0,
                rejected_count=0,
                error_details=json.dumps({
                    "errors": [err.model_dump() for err in errors],
                    "valid_rows": valid_rows,
                }),
                created_by=user_id,
            )
            db.add(import_history)
            db.commit()
            db.refresh(import_history)

            return {
                "import_id": import_history.id,
                "status": "validated",
                "total_rows": total_rows,
                "valid_rows": len(valid_rows),
                "invalid_rows": len(errors),
                "errors": errors,
            }
        except Exception:
            db.rollback()
            # Return without import_id if database fails
            return {
                "import_id": None,
                "status": "validated",
                "total_rows": total_rows,
                "valid_rows": len(valid_rows),
                "invalid_rows": len(errors),
                "errors": errors,
            }

    except Exception as e:
        return {
            "import_id": None,
            "status": "failed",
            "total_rows": 0,
            "valid_rows": 0,
            "invalid_rows": 0,
            "errors": [
                CSVRowError(
                    row_number=0,
                    field="file",
                    message=f"erro ao processar arquivo: {str(e)}",
                )
            ],
        }


def process_import(
    import_id: int,
    db: Session,
) -> dict[str, Any]:
    """Process import and persist valid shipments."""
    import_history = db.get(ImportHistory, import_id)
    if not import_history:
        return {
            "import_id": import_id,
            "status": "failed",
            "total_rows": 0,
            "valid_rows": 0,
            "invalid_rows": 0,
            "imported_count": 0,
            "rejected_count": 0,
            "errors": [
                CSVRowError(
                    row_number=0,
                    field="import_id",
                    message="historico de importacao nao encontrado",
                )
            ],
        }

    if import_history.status != "validated":
        return {
            "import_id": import_id,
            "status": "failed",
            "total_rows": import_history.total_rows,
            "valid_rows": import_history.valid_rows,
            "invalid_rows": import_history.invalid_rows,
            "imported_count": 0,
            "rejected_count": 0,
            "errors": [
                CSVRowError(
                    row_number=0,
                    field="status",
                    message="importacao ja processada ou em estado invalido",
                )
            ],
        }

    # Recover valid rows from error_details
    try:
        error_details = json.loads(import_history.error_details) if isinstance(import_history.error_details, str) else import_history.error_details
        valid_rows = error_details.get("valid_rows", [])
    except Exception:
        valid_rows = []

    if not valid_rows:
        return {
            "import_id": import_id,
            "status": "completed",
            "total_rows": import_history.total_rows,
            "valid_rows": import_history.valid_rows,
            "invalid_rows": import_history.invalid_rows,
            "imported_count": 0,
            "rejected_count": 0,
            "errors": [],
        }

    # Process valid rows, checking for duplicates during processing
    tracking_codes_in_file = {}
    errors: list[CSVRowError] = []
    imported_count = 0
    rejected_count = 0

    for idx, row in enumerate(valid_rows):
        tracking_code = row.get("tracking_code", "").strip()
        if not tracking_code:
            continue

        # Check duplicate in database
        existing = db.query(Shipment).filter(Shipment.tracking_code == tracking_code).first()
        if existing:
            errors.append(
                CSVRowError(
                    row_number=idx + 1,
                    field="tracking_code",
                    message="tracking_code ja existe no banco",
                    value=tracking_code,
                )
            )
            rejected_count += 1
            continue

        # Check duplicate within file (only mark subsequent occurrences as errors)
        if tracking_code in tracking_codes_in_file:
            errors.append(
                CSVRowError(
                    row_number=idx + 1,
                    field="tracking_code",
                    message="tracking_code duplicado no arquivo",
                    value=tracking_code,
                )
            )
            rejected_count += 1
            continue

        # Mark this tracking_code as seen
        tracking_codes_in_file[tracking_code] = idx + 1

        # Process the row
        carrier_name = row.get("carrier_name", "").strip()
        carrier = db.query(Carrier).filter(Carrier.name == carrier_name).first()
        if not carrier:
            errors.append(
                CSVRowError(
                    row_number=idx + 1,
                    field="carrier_name",
                    message="transportadora nao encontrada",
                    value=carrier_name,
                )
            )
            rejected_count += 1
            continue

        # Create shipment
        try:
            estimated_delivery = datetime.fromisoformat(row.get("estimated_delivery", "").replace("Z", "+00:00"))
            
            # Parse fiscal/financial fields
            invoice_number = row.get("invoice_number", "").strip() or None
            invoice_key = row.get("invoice_key", "").strip() or None
            fiscal_document = row.get("fiscal_document", "").strip() or None
            amount = None
            if row.get("amount", "").strip():
                try:
                    amount = float(row.get("amount", "").replace(",", ".").strip())
                except (ValueError, AttributeError):
                    amount = None
            
            due_date = None
            if row.get("due_date", "").strip():
                try:
                    due_date = datetime.fromisoformat(row.get("due_date", "").replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    due_date = None
            
            # Calculate delay_days and criticality
            delay_days = calculate_delay_days(due_date)
            criticality = classify_criticality(delay_days, amount)
            
            shipment = Shipment(
                tracking_code=tracking_code,
                carrier_id=carrier.id,
                status="pending",
                estimated_delivery=estimated_delivery,
                recipient_name=row.get("recipient_name", ""),
                recipient_phone=row.get("recipient_phone", ""),
                origin_address=row.get("origin_address", ""),
                destination_address=row.get("destination_address", ""),
                meta_data=json.dumps({}),
                is_active=True,
                invoice_number=invoice_number,
                invoice_key=invoice_key,
                fiscal_document=fiscal_document,
                amount=amount,
                due_date=due_date,
                delay_days=delay_days,
                criticality=criticality,
            )
            db.add(shipment)
            imported_count += 1
        except Exception as e:
            errors.append(
                CSVRowError(
                    row_number=idx + 1,
                    field="shipment",
                    message=f"erro ao criar shipment: {str(e)}",
                    value=tracking_code,
                )
            )
            rejected_count += 1

    # Update import history
    import_history.status = "completed"
    import_history.imported_count = imported_count
    import_history.rejected_count = rejected_count
    import_history.error_details = json.dumps({
        "errors": [err.model_dump() for err in errors],
        "valid_rows": valid_rows,
    })

    try:
        db.commit()
    except Exception:
        db.rollback()
        return {
            "import_id": import_id,
            "status": "failed",
            "total_rows": import_history.total_rows,
            "valid_rows": import_history.valid_rows,
            "invalid_rows": import_history.invalid_rows,
            "imported_count": 0,
            "rejected_count": 0,
            "errors": [
                CSVRowError(
                    row_number=0,
                    field="database",
                    message="erro ao persistir importacao",
                )
            ],
        }

    return {
        "import_id": import_id,
        "status": "completed",
        "total_rows": import_history.total_rows,
        "valid_rows": import_history.valid_rows,
        "invalid_rows": import_history.invalid_rows,
        "imported_count": imported_count,
        "rejected_count": rejected_count,
        "errors": errors,
    }


def get_shipment_detail(db: Session, shipment_id: int) -> dict[str, Any] | None:
    item = db.get(Shipment, shipment_id)
    if item is None:
        return None
    return {
        "id": item.id,
        "tracking_code": item.tracking_code,
        "carrier_id": item.carrier_id,
        "status": item.status,
        "estimated_delivery": item.estimated_delivery,
        "recipient_name": item.recipient_name,
        "recipient_phone": item.recipient_phone,
        "origin_address": item.origin_address,
        "destination_address": item.destination_address,
        "invoice_number": item.invoice_number,
        "invoice_key": item.invoice_key,
        "fiscal_document": item.fiscal_document,
        "amount": float(item.amount) if item.amount else None,
        "due_date": item.due_date,
        "delay_days": item.delay_days,
        "criticality": item.criticality,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
    }


def list_treatments(db: Session, shipment_id: int) -> list[dict[str, Any]]:
    rows = (
        db.query(ShipmentTreatment)
        .filter(ShipmentTreatment.shipment_id == shipment_id)
        .order_by(ShipmentTreatment.created_at.desc())
        .all()
    )
    return [
        {
            "id": row.id,
            "shipment_id": row.shipment_id,
            "status": row.status,
            "comment": row.comment,
            "created_by": row.created_by,
            "created_at": row.created_at,
        }
        for row in rows
    ]


def create_treatment(db: Session, shipment_id: int, created_by: int, status: str, comment: str) -> dict[str, Any] | None:
    shipment = db.get(Shipment, shipment_id)
    if shipment is None:
        return None
    row = ShipmentTreatment(
        shipment_id=shipment_id,
        status=status,
        comment=comment,
        created_by=created_by,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return {
        "id": row.id,
        "shipment_id": row.shipment_id,
        "status": row.status,
        "comment": row.comment,
        "created_by": row.created_by,
        "created_at": row.created_at,
    }


def build_daily_report(db: Session) -> dict[str, Any]:
    shipments = db.query(Shipment).all()
    total = len(shipments)
    total_exceptions = len([s for s in shipments if s.delay_days > 0 or s.criticality != "normal"])
    by_criticality: dict[str, int] = {"normal": 0, "baixa": 0, "media": 0, "alta": 0}
    by_carrier: dict[int, int] = {}
    for row in shipments:
        by_criticality[row.criticality] = by_criticality.get(row.criticality, 0) + 1
        by_carrier[row.carrier_id] = by_carrier.get(row.carrier_id, 0) + 1
    return {
        "report_date": datetime.now(UTC).date().isoformat(),
        "total_shipments": total,
        "total_exceptions": total_exceptions,
        "by_criticality": by_criticality,
        "by_carrier": [{"carrier_id": k, "count": v} for k, v in sorted(by_carrier.items())],
    }
