import csv
import io
import json
from datetime import UTC, datetime
from typing import Any

from fastapi import HTTPException
from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.modules.carriers.models import Carrier
from app.modules.shipments.models import ImportHistory, Shipment, ShipmentTreatment, calculate_freight_percentage
from app.modules.shipments.schemas import CSVRowError


def calculate_delay_days(due_date: datetime | None, reference_date: datetime | None = None) -> int:
    if not due_date:
        return 0
    ref_date = reference_date or datetime.now(UTC)
    if ref_date.tzinfo is not None and due_date.tzinfo is None:
        due_date = due_date.replace(tzinfo=UTC)
    elif ref_date.tzinfo is None and due_date.tzinfo is not None:
        ref_date = ref_date.replace(tzinfo=UTC)
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
    invoice_key: str | None = None,
    fiscal_document: str | None = None,
    criticality: str | None = None,
    estimated_delivery_from: str | None = None,
    estimated_delivery_to: str | None = None,
    due_date_from: str | None = None,
    due_date_to: str | None = None,
    collection_departure_from: str | None = None,
    collection_departure_to: str | None = None,
    customer_name: str | None = None,
    destination_uf: str | None = None,
    month: int | None = None,
    year: int | None = None,
    search: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    # Filtros fiscais/financeiros (BETA-031)
    freight_value_min: float | None = None,
    freight_value_max: float | None = None,
    invoice_value_min: float | None = None,
    invoice_value_max: float | None = None,
    freight_percentage_min: float | None = None,
    freight_percentage_max: float | None = None,
    amount_min: float | None = None,
    amount_max: float | None = None,
    # Filtros SLA (BETA-1.1)
    sla_status: str | None = None,
    is_late: bool | None = None,
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
    
    if customer_name:
        query = query.filter(Shipment.customer_name.ilike(f"%{customer_name}%"))
    
    if destination_uf:
        query = query.filter(Shipment.destination_uf == destination_uf)
    
    if month:
        query = query.filter(extract('month', Shipment.estimated_delivery) == month)
    
    if year:
        query = query.filter(extract('year', Shipment.estimated_delivery) == year)

    # Filtros fiscais/financeiros (BETA-031)
    if invoice_key:
        query = query.filter(Shipment.invoice_key.ilike(f"%{invoice_key}%"))
    
    if collection_departure_from:
        try:
            from_date = datetime.fromisoformat(collection_departure_from.replace("Z", "+00:00"))
            query = query.filter(Shipment.collection_departure_date >= from_date)
        except (ValueError, AttributeError):
            pass
    
    if collection_departure_to:
        try:
            to_date = datetime.fromisoformat(collection_departure_to.replace("Z", "+00:00"))
            query = query.filter(Shipment.collection_departure_date <= to_date)
        except (ValueError, AttributeError):
            pass

    if freight_value_min is not None:
        query = query.filter(Shipment.freight_value >= freight_value_min)
    if freight_value_max is not None:
        query = query.filter(Shipment.freight_value <= freight_value_max)
    
    if invoice_value_min is not None:
        query = query.filter(Shipment.invoice_value >= invoice_value_min)
    if invoice_value_max is not None:
        query = query.filter(Shipment.invoice_value <= invoice_value_max)
    
    if freight_percentage_min is not None:
        query = query.filter(Shipment.freight_percentage >= freight_percentage_min)
    if freight_percentage_max is not None:
        query = query.filter(Shipment.freight_percentage <= freight_percentage_max)
    
    if amount_min is not None:
        query = query.filter(Shipment.amount >= amount_min)
    if amount_max is not None:
        query = query.filter(Shipment.amount <= amount_max)

    # Filtros SLA (BETA-1.1) - Calculados dinamicamente
    if sla_status or is_late is not None:
        from app.modules.sla.service import recalculate_shipment_sla
        
        # Buscar todos os registros (limitado a 1000 para performance)
        all_items = query.limit(1000).all()
        
        filtered_items = []
        for item in all_items:
            sla_result = recalculate_shipment_sla(db, item.id)
            item_sla_status = sla_result.get("sla_status")
            item_is_late = sla_result.get("is_late", False)
            
            # Aplicar filtros
            if sla_status and item_sla_status != sla_status:
                continue
            if is_late is not None and item_is_late != is_late:
                continue
            
            filtered_items.append(item)
        
        # Aplicar sorting manual na lista filtrada
        sort_column = getattr(Shipment, sort_by, Shipment.created_at)
        reverse = sort_order.lower() == "desc"
        filtered_items.sort(key=lambda x: getattr(x, sort_column.name), reverse=reverse)
        
        # Paginação manual
        total = len(filtered_items)
        offset = (page - 1) * page_size
        items = filtered_items[offset:offset + page_size]
    else:
        # Se não há filtros SLA, usar fluxo normal
        if search:
            from sqlalchemy import or_
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Shipment.tracking_code.ilike(search_pattern),
                    Shipment.invoice_number.ilike(search_pattern),
                    Shipment.invoice_key.ilike(search_pattern),
                    Shipment.fiscal_document.ilike(search_pattern),
                    Shipment.customer_name.ilike(search_pattern),
                    Shipment.destination_uf.ilike(search_pattern)
                )
            )

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
            "freight_value": float(item.freight_value) if item.freight_value else None,
            "invoice_value": float(item.invoice_value) if item.invoice_value else None,
            "freight_percentage": float(item.freight_percentage) if item.freight_percentage else None,
            "collection_departure_date": item.collection_departure_date,
            "customer_name": item.customer_name,
            "destination_uf": item.destination_uf,
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
    customer_name: str | None = None,
    destination_uf: str | None = None,
    month: int | None = None,
    year: int | None = None,
    search: str | None = None,
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
    
    if customer_name:
        query = query.filter(Shipment.customer_name.ilike(f"%{customer_name}%"))
    
    if destination_uf:
        query = query.filter(Shipment.destination_uf == destination_uf)
    
    if month:
        query = query.filter(extract('month', Shipment.estimated_delivery) == month)
    
    if year:
        query = query.filter(extract('year', Shipment.estimated_delivery) == year)
    
    if search:
        from sqlalchemy import or_
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Shipment.tracking_code.ilike(search_pattern),
                Shipment.invoice_number.ilike(search_pattern),
                Shipment.customer_name.ilike(search_pattern),
                Shipment.destination_uf.ilike(search_pattern)
            )
        )

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
                "freight_value": float(item.freight_value) if item.freight_value else None,
                "invoice_value": float(item.invoice_value) if item.invoice_value else None,
                "freight_percentage": float(item.freight_percentage) if item.freight_percentage else None,
                "collection_departure_date": item.collection_departure_date,
                "customer_name": item.customer_name,
                "destination_uf": item.destination_uf,
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
            
            # Parse new fiscal/financial fields (BETA-011A)
            freight_value = None
            if row.get("freight_value", "").strip():
                try:
                    freight_value = float(row.get("freight_value", "").replace(",", ".").strip())
                except (ValueError, AttributeError):
                    freight_value = None
            
            invoice_value = None
            if row.get("invoice_value", "").strip():
                try:
                    invoice_value = float(row.get("invoice_value", "").replace(",", ".").strip())
                except (ValueError, AttributeError):
                    invoice_value = None
            
            collection_departure_date = None
            if row.get("collection_departure_date", "").strip():
                try:
                    collection_departure_date = datetime.fromisoformat(row.get("collection_departure_date", "").replace("Z", "+00:00"))
                except (ValueError, AttributeError):
                    collection_departure_date = None
            
            customer_name = row.get("customer_name", "").strip() or None
            destination_uf = row.get("destination_uf", "").strip() or None
            
            # Calculate delay_days and criticality
            delay_days = calculate_delay_days(due_date)
            criticality = classify_criticality(delay_days, amount)
            
            # Calculate freight_percentage
            freight_percentage = calculate_freight_percentage(freight_value, invoice_value)
            
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
                freight_value=freight_value,
                invoice_value=invoice_value,
                freight_percentage=freight_percentage,
                collection_departure_date=collection_departure_date,
                customer_name=customer_name,
                destination_uf=destination_uf,
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


def create_shipment(db: Session, payload: dict[str, Any]) -> dict[str, Any]:
    """Create a single shipment from a validated ShipmentCreate payload."""
    carrier = db.get(Carrier, payload["carrier_id"])
    if carrier is None:
        raise HTTPException(status_code=404, detail="transportadora nao encontrada")

    estimated_delivery = datetime.fromisoformat(payload["estimated_delivery"].replace("Z", "+00:00"))

    due_date = None
    if payload.get("due_date"):
        due_date = datetime.fromisoformat(payload["due_date"].replace("Z", "+00:00"))

    collection_departure_date = None
    if payload.get("collection_departure_date"):
        collection_departure_date = datetime.fromisoformat(payload["collection_departure_date"].replace("Z", "+00:00"))

    delay_days = calculate_delay_days(due_date)
    criticality = payload.get("criticality") or classify_criticality(delay_days, payload.get("amount"))
    freight_value = payload.get("freight_value")
    invoice_value = payload.get("invoice_value")
    freight_percentage = calculate_freight_percentage(freight_value, invoice_value)

    shipment = Shipment(
        tracking_code=payload["tracking_code"],
        carrier_id=payload["carrier_id"],
        status=payload.get("status", "pending"),
        estimated_delivery=estimated_delivery,
        recipient_name=payload["recipient_name"],
        recipient_phone=payload["recipient_phone"],
        origin_address=payload["origin_address"],
        destination_address=payload["destination_address"],
        meta_data=json.dumps({}),
        is_active=True,
        invoice_number=payload.get("invoice_number"),
        invoice_key=payload.get("invoice_key"),
        fiscal_document=payload.get("fiscal_document"),
        amount=payload.get("amount"),
        due_date=due_date,
        delay_days=delay_days,
        criticality=criticality,
        freight_value=freight_value,
        invoice_value=invoice_value,
        freight_percentage=freight_percentage,
        collection_departure_date=collection_departure_date,
        customer_name=payload.get("customer_name"),
        destination_uf=payload.get("destination_uf"),
    )
    db.add(shipment)
    db.commit()
    db.refresh(shipment)

    return {
        "id": shipment.id,
        "tracking_code": shipment.tracking_code,
        "carrier_id": shipment.carrier_id,
        "status": shipment.status,
        "estimated_delivery": shipment.estimated_delivery,
        "actual_delivery": shipment.actual_delivery,
        "recipient_name": shipment.recipient_name,
        "recipient_phone": shipment.recipient_phone,
        "origin_address": shipment.origin_address,
        "destination_address": shipment.destination_address,
        "meta_data": {},
        "is_active": shipment.is_active,
        "created_at": shipment.created_at,
        "updated_at": shipment.updated_at,
        "invoice_number": shipment.invoice_number,
        "invoice_key": shipment.invoice_key,
        "fiscal_document": shipment.fiscal_document,
        "amount": float(shipment.amount) if shipment.amount else None,
        "due_date": shipment.due_date,
        "delay_days": shipment.delay_days,
        "criticality": shipment.criticality,
        "freight_value": float(shipment.freight_value) if shipment.freight_value else None,
        "invoice_value": float(shipment.invoice_value) if shipment.invoice_value else None,
        "freight_percentage": float(shipment.freight_percentage) if shipment.freight_percentage else None,
        "collection_departure_date": shipment.collection_departure_date,
        "customer_name": shipment.customer_name,
        "destination_uf": shipment.destination_uf,
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
        "freight_value": float(item.freight_value) if item.freight_value is not None else None,
        "invoice_value": float(item.invoice_value) if item.invoice_value is not None else None,
        "freight_percentage": float(item.freight_percentage) if item.freight_percentage is not None else None,
        "collection_departure_date": item.collection_departure_date,
        "customer_name": item.customer_name,
        "destination_uf": item.destination_uf,
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
