import csv
import io
import json
from datetime import UTC, datetime
from typing import Any

from sqlalchemy import extract
from sqlalchemy.orm import Session

from app.modules.carriers.models import Carrier
from app.modules.shipments.models import ImportHistory, Shipment, ShipmentTreatment, calculate_freight_percentage
from app.modules.shipments.schemas import CSVRowError
from app.modules.sla.service import calculate_shipment_sla


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
    customer_name: str | None = None,
    destination_uf: str | None = None,
    month: int | None = None,
    year: int | None = None,
    search: str | None = None,
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
        # Calculate SLA on-demand
        sla_result = calculate_shipment_sla(db, item.id)
        
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
            # SLA fields (BETA-013A) - calculados on-demand
            "sla_due_date": sla_result.get("sla_due_date"),
            "sla_status": sla_result.get("sla_status"),
            "is_late": sla_result.get("is_late", False),
            "sla_rule_id": sla_result.get("sla_rule_id"),
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
    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    offset = (page - 1) * page_size
    items = query.offset(offset).limit(page_size).all()

    items_data = []
    for item in items:
        # Calculate SLA on-demand
        sla_result = calculate_shipment_sla(db, item.id)
        
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
            # SLA fields (BETA-013A) - calculados on-demand
            "sla_due_date": sla_result.get("sla_due_date"),
            "sla_status": sla_result.get("sla_status"),
            "is_late": sla_result.get("is_late", False),
            "sla_rule_id": sla_result.get("sla_rule_id"),
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        })

    return {
        "items": items_data,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


def get_shipment_detail(db: Session, shipment_id: int) -> dict[str, Any] | None:
    from app.modules.shipments.models import Shipment

    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        return None

    # Calculate SLA on-demand
    sla_result = calculate_shipment_sla(db, shipment.id)

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
        # SLA fields (BETA-013A) - calculados on-demand
        "sla_due_date": sla_result.get("sla_due_date"),
        "sla_status": sla_result.get("sla_status"),
        "is_late": sla_result.get("is_late", False),
        "sla_rule_id": sla_result.get("sla_rule_id"),
        "created_at": shipment.created_at,
        "updated_at": shipment.updated_at,
    }


def create_treatment(db: Session, shipment_id: int, status: str, comment: str, created_by: int) -> dict[str, Any]:
    from app.modules.shipments.models import ShipmentTreatment

    treatment = ShipmentTreatment(
        shipment_id=shipment_id,
        status=status,
        comment=comment,
        created_by=created_by,
    )
    db.add(treatment)
    db.commit()
    db.refresh(treatment)

    return {
        "id": treatment.id,
        "shipment_id": treatment.shipment_id,
        "status": treatment.status,
        "comment": treatment.comment,
        "created_by": treatment.created_by,
        "created_at": treatment.created_at,
    }


def list_treatments(db: Session, shipment_id: int) -> list[dict[str, Any]]:
    from app.modules.shipments.models import ShipmentTreatment

    treatments = db.query(ShipmentTreatment).filter(ShipmentTreatment.shipment_id == shipment_id).all()

    return [
        {
            "id": t.id,
            "shipment_id": t.shipment_id,
            "status": t.status,
            "comment": t.comment,
            "created_by": t.created_by,
            "created_at": t.created_at,
        }
        for t in treatments
    ]


def parse_csv_file(file_content: bytes) -> tuple[list[dict[str, Any]], list[CSVRowError]]:
    """Parse CSV file and return rows and errors."""
    content_str = file_content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(content_str))
    
    rows = []
    errors = []
    
    for row_num, row in enumerate(csv_reader, start=1):
        rows.append(row)
    
    return rows, errors


def process_import(
    db: Session,
    file_name: str,
    rows: list[dict[str, Any]],
    created_by: int,
    source: str = "generic",
) -> dict[str, Any]:
    """Process import rows and create import history."""
    from app.modules.imports.service_v2 import process_import_v2
    
    return process_import_v2(db, file_name, rows, created_by, source)


def build_daily_report(db: Session) -> dict[str, Any]:
    """Build daily report (placeholder for BETA-014)."""
    from app.modules.shipments.models import Shipment
    
    total_shipments = db.query(Shipment).count()
    delivered_shipments = db.query(Shipment).filter(Shipment.status == "delivered").count()
    in_transit_shipments = db.query(Shipment).filter(Shipment.status == "in_transit").count()
    pending_shipments = db.query(Shipment).filter(Shipment.status == "pending").count()
    
    return {
        "total_shipments": total_shipments,
        "delivered_shipments": delivered_shipments,
        "in_transit_shipments": in_transit_shipments,
        "pending_shipments": pending_shipments,
        "delivery_rate": (delivered_shipments / total_shipments * 100) if total_shipments > 0 else 0,
    }
