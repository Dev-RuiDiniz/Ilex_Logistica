"""SLA router for BETA-013A."""

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_roles, require_permission
from app.modules.sla.service import (
    recalculate_all_shipments_sla,
    recalculate_shipment_sla,
)
from app.modules.sla.models import SlaRule

router = APIRouter(prefix="/sla", tags=["sla"])


class SlaRuleCreate(BaseModel):
    carrier_id: int | None = None
    destination_uf: str | None = Field(None, max_length=2)
    transit_days: int = Field(..., gt=0)
    warning_threshold_days: int = Field(..., gt=0)
    critical_delay_days: int = Field(..., gt=0)
    is_active: bool = True


class SlaRuleUpdate(BaseModel):
    carrier_id: int | None = None
    destination_uf: str | None = Field(None, max_length=2)
    transit_days: int | None = Field(None, gt=0)
    warning_threshold_days: int | None = Field(None, gt=0)
    critical_delay_days: int | None = Field(None, gt=0)
    is_active: bool | None = None


@router.post("/recalculate")
def recalculate_sla_endpoint(
    carrier_id: Annotated[int | None, Query()] = None,
    destination_uf: Annotated[str | None, Query()] = None,
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("sla:write")),
):
    """Recalculate SLA for all shipments with optional filters."""
    result = recalculate_all_shipments_sla(db, carrier_id, destination_uf)
    return result


@router.post("/recalculate/{shipment_id}")
def recalculate_shipment_sla_endpoint(
    shipment_id: int,
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("sla:write")),
):
    """Recalculate SLA for a single shipment."""
    result = recalculate_shipment_sla(db, shipment_id)
    return result


@router.get("/rules")
def list_sla_rules(
    carrier_id: Annotated[int | None, Query()] = None,
    destination_uf: Annotated[str | None, Query()] = None,
    is_active: Annotated[bool | None, Query()] = None,
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("sla:read")),
):
    """List SLA rules with optional filters."""
    query = db.query(SlaRule)
    
    if carrier_id:
        query = query.filter(SlaRule.carrier_id == carrier_id)
    if destination_uf:
        query = query.filter(SlaRule.destination_uf == destination_uf.upper())
    if is_active is not None:
        query = query.filter(SlaRule.is_active == is_active)
    
    rules = query.all()
    
    return [
        {
            "id": rule.id,
            "carrier_id": rule.carrier_id,
            "destination_uf": rule.destination_uf,
            "transit_days": rule.transit_days,
            "warning_threshold_days": rule.warning_threshold_days,
            "critical_delay_days": rule.critical_delay_days,
            "is_active": rule.is_active,
            "created_at": rule.created_at,
            "updated_at": rule.updated_at,
        }
        for rule in rules
    ]


@router.post("/rules")
def create_sla_rule(
    rule_data: SlaRuleCreate,
    db: Session = Depends(get_db),
    _user: object = Depends(require_roles(["admin"])),
):
    """Create a new SLA rule (admin only)."""
    rule = SlaRule(
        carrier_id=rule_data.carrier_id,
        destination_uf=rule_data.destination_uf.upper() if rule_data.destination_uf else None,
        transit_days=rule_data.transit_days,
        warning_threshold_days=rule_data.warning_threshold_days,
        critical_delay_days=rule_data.critical_delay_days,
        is_active=rule_data.is_active,
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    
    return {
        "id": rule.id,
        "carrier_id": rule.carrier_id,
        "destination_uf": rule.destination_uf,
        "transit_days": rule.transit_days,
        "warning_threshold_days": rule.warning_threshold_days,
        "critical_delay_days": rule.critical_delay_days,
        "is_active": rule.is_active,
        "created_at": rule.created_at,
        "updated_at": rule.updated_at,
    }


@router.put("/rules/{rule_id}")
def update_sla_rule(
    rule_id: int,
    rule_data: SlaRuleUpdate,
    db: Session = Depends(get_db),
    _user: object = Depends(require_roles(["admin"])),
):
    """Update an existing SLA rule (admin only)."""
    rule = db.query(SlaRule).filter(SlaRule.id == rule_id).first()
    if not rule:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="SLA rule not found")
    
    if rule_data.carrier_id is not None:
        rule.carrier_id = rule_data.carrier_id
    if rule_data.destination_uf is not None:
        rule.destination_uf = rule_data.destination_uf.upper() if rule_data.destination_uf else None
    if rule_data.transit_days is not None:
        rule.transit_days = rule_data.transit_days
    if rule_data.warning_threshold_days is not None:
        rule.warning_threshold_days = rule.warning_threshold_days
    if rule_data.critical_delay_days is not None:
        rule.critical_delay_days = rule.critical_delay_days
    if rule_data.is_active is not None:
        rule.is_active = rule_data.is_active
    
    db.commit()
    db.refresh(rule)
    
    return {
        "id": rule.id,
        "carrier_id": rule.carrier_id,
        "destination_uf": rule.destination_uf,
        "transit_days": rule.transit_days,
        "warning_threshold_days": rule.warning_threshold_days,
        "critical_delay_days": rule.critical_delay_days,
        "is_active": rule.is_active,
        "created_at": rule.created_at,
        "updated_at": rule.updated_at,
    }
