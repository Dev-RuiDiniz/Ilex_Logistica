"""SLA service for BETA-013A."""

import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy.orm import Session

from app.modules.sla.models import SlaRule
from app.modules.shipments.models import Shipment
from app.modules.audit.service import AuditLogService
from app.modules.audit.schemas import AuditLogCreateRequest

logger = logging.getLogger(__name__)


def get_applicable_sla_rule(
    db: Session,
    carrier_id: int | None = None,
    destination_uf: str | None = None,
) -> SlaRule | None:
    """Get the most specific applicable SLA rule for a shipment.

    Priority:
    1. carrier_id + destination_uf (most specific)
    2. carrier_id only
    3. global/default (fallback)

    Args:
        db: Database session
        carrier_id: Carrier ID (optional)
        destination_uf: Destination UF (optional)

    Returns:
        SlaRule if found, None otherwise
    """
    # Try carrier_id + destination_uf (most specific)
    if carrier_id and destination_uf:
        rule = (
            db.query(SlaRule)
            .filter(
                SlaRule.carrier_id == carrier_id,
                SlaRule.destination_uf == destination_uf.upper(),
                SlaRule.is_active.is_(True),
            )
            .first()
        )
        if rule:
            return rule

    # Try carrier_id only
    if carrier_id:
        rule = (
            db.query(SlaRule)
            .filter(
                SlaRule.carrier_id == carrier_id,
                SlaRule.destination_uf.is_(None),
                SlaRule.is_active.is_(True),
            )
            .first()
        )
        if rule:
            return rule

    # Fallback to global rule
    rule = (
        db.query(SlaRule)
        .filter(
            SlaRule.carrier_id.is_(None),
            SlaRule.destination_uf.is_(None),
            SlaRule.is_active.is_(True),
        )
        .first()
    )
    return rule


def calculate_sla_due_date(
    collection_departure_date: datetime | None,
    transit_days: int,
    expected_delivery: datetime | None = None,
) -> datetime | None:
    """Calculate SLA due date.

    If expected_delivery is provided, use it directly.
    Otherwise, calculate from collection_departure_date + transit_days.

    Args:
        collection_departure_date: Collection/departure date
        transit_days: Transit days from SLA rule
        expected_delivery: Expected delivery date (optional)

    Returns:
        SLA due date or None if no data available
    """
    if expected_delivery:
        return expected_delivery

    if collection_departure_date and transit_days:
        # Ensure timezone-aware
        if collection_departure_date.tzinfo is None:
            collection_departure_date = collection_departure_date.replace(tzinfo=UTC)
        return collection_departure_date + timedelta(days=transit_days)

    return None


def calculate_delay_days_sla(
    sla_due_date: datetime | None,
    delivered_at: datetime | None = None,
    today: datetime | None = None,
) -> int:
    """Calculate delay days for SLA.

    Args:
        sla_due_date: SLA due date
        delivered_at: Actual delivery date (if delivered)
        today: Current date (injectable for tests)

    Returns:
        Delay days (never negative)
    """
    if not sla_due_date:
        return 0

    reference_date = delivered_at or today or datetime.now(UTC)
    
    # Ensure both dates are timezone-aware
    if reference_date.tzinfo is None:
        reference_date = reference_date.replace(tzinfo=UTC)
    if sla_due_date.tzinfo is None:
        sla_due_date = sla_due_date.replace(tzinfo=UTC)
    
    delta = reference_date - sla_due_date
    return max(0, delta.days)


def calculate_sla_status(
    delay_days: int | None,
    warning_threshold_days: int,
    critical_delay_days: int,
) -> str:
    """Calculate SLA status based on delay days.

    Args:
        delay_days: Delay days
        warning_threshold_days: Warning threshold
        critical_delay_days: Critical threshold

    Returns:
        SLA status: "on_time", "warning", "late", "critical", "unknown"
    """
    if delay_days is None:
        return "unknown"

    if delay_days == 0:
        return "on_time"
    elif delay_days < warning_threshold_days:
        return "warning"
    elif delay_days < critical_delay_days:
        return "late"
    else:
        return "critical"


def calculate_criticality_sla(
    delay_days: int | None,
    critical_delay_days: int,
) -> str:
    """Calculate criticality based on delay days.

    Maps to existing criticality values: "normal", "baixa", "media", "alta"

    Args:
        delay_days: Delay days
        critical_delay_days: Critical threshold

    Returns:
        Criticality: "normal", "baixa", "media", "alta"
    """
    if delay_days is None or delay_days == 0:
        return "normal"
    elif delay_days < critical_delay_days:
        return "baixa"
    else:
        return "alta"


def calculate_shipment_sla(
    db: Session,
    shipment_id: int,
    today: datetime | None = None,
    use_expected_delivery: bool = True,
) -> dict[str, Any]:
    """Calculate SLA for a single shipment.

    Args:
        db: Database session
        shipment_id: Shipment ID
        today: Current date (injectable for tests)
        use_expected_delivery: Whether to use expected_delivery if available

    Returns:
        Dictionary with SLA calculation results
    """
    shipment = db.query(Shipment).filter(Shipment.id == shipment_id).first()
    if not shipment:
        return {
            "success": False,
            "error": "shipment_not_found",
            "sla_status": "unknown",
            "delay_days": 0,
            "is_late": False,
            "criticality": "normal",
        }

    # Get applicable SLA rule
    rule = get_applicable_sla_rule(db, shipment.carrier_id, shipment.destination_uf)

    if not rule:
        return {
            "success": True,
            "shipment_id": shipment_id,
            "sla_due_date": None,
            "sla_status": "unknown",
            "delay_days": 0,
            "is_late": False,
            "sla_rule_id": None,
            "criticality": "normal",  # Default when no rule
        }

    # Calculate SLA due date
    expected_delivery = shipment.estimated_delivery if use_expected_delivery else None
    sla_due_date = calculate_sla_due_date(
        shipment.collection_departure_date,
        rule.transit_days,
        expected_delivery,
    )

    if not sla_due_date:
        return {
            "success": True,
            "shipment_id": shipment_id,
            "sla_due_date": None,
            "sla_status": "unknown",
            "delay_days": 0,
            "is_late": False,
            "sla_rule_id": rule.id,
            "criticality": "normal",  # Default when no due date
        }

    # Calculate delay days
    delay_days = calculate_delay_days_sla(sla_due_date, shipment.actual_delivery, today)

    # Calculate SLA status
    sla_status = calculate_sla_status(
        delay_days,
        rule.warning_threshold_days,
        rule.critical_delay_days,
    )

    # Calculate criticality
    criticality = calculate_criticality_sla(delay_days, rule.critical_delay_days)

    return {
        "success": True,
        "shipment_id": shipment_id,
        "sla_due_date": sla_due_date,
        "sla_status": sla_status,
        "delay_days": delay_days,
        "is_late": delay_days > 0,
        "sla_rule_id": rule.id,
        "criticality": criticality,
    }


def recalculate_shipment_sla(
    db: Session,
    shipment_id: int,
    today: datetime | None = None,
) -> dict[str, Any]:
    """Calculate SLA for a single shipment (on-demand, no persistence).

    Args:
        db: Database session
        shipment_id: Shipment ID
        today: Current date (injectable for tests)

    Returns:
        Dictionary with SLA calculation results
    """
    return calculate_shipment_sla(db, shipment_id, today)


def recalculate_all_shipments_sla(
    db: Session,
    carrier_id: int | None = None,
    destination_uf: str | None = None,
    today: datetime | None = None,
) -> dict[str, int]:
    """Calculate SLA for all shipments with optional filters (on-demand, no persistence).

    Args:
        db: Database session
        carrier_id: Filter by carrier ID (optional)
        destination_uf: Filter by destination UF (optional)
        today: Current date (injectable for tests)

    Returns:
        Dictionary with counters: processed_count, updated_count, skipped_count, error_count
    """
    query = db.query(Shipment)

    if carrier_id:
        query = query.filter(Shipment.carrier_id == carrier_id)
    if destination_uf:
        query = query.filter(Shipment.destination_uf == destination_uf.upper())

    shipments = query.all()

    processed_count = 0
    updated_count = 0
    skipped_count = 0
    error_count = 0

    for shipment in shipments:
        processed_count += 1
        try:
            result = recalculate_shipment_sla(db, shipment.id, today)
            if result["success"] and result["sla_status"] != "unknown":
                updated_count += 1
            else:
                skipped_count += 1
        except Exception:
            error_count += 1

    # Audit log
    try:
        audit_log = AuditLogCreateRequest(
            event_type="sla_recalculated",
            entity_type="shipment",
            action="update",
            source="system",
            severity="info",
            status="success",
            message=f"SLA recalculado para {updated_count} shipments",
            metadata_json=f'{{"recalculated_count": {updated_count}}}',
        )
        AuditLogService.create_log(db, audit_log)
    except Exception as e:
        logger.error(f"Failed to create audit log for SLA recalculation: {e}")

    return {
        "processed_count": processed_count,
        "updated_count": updated_count,
        "skipped_count": skipped_count,
        "error_count": error_count,
    }
