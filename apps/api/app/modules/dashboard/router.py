"""Router do módulo dashboard para BETA-016A."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.dashboard.service import (
    calculate_dashboard_summary,
    calculate_dashboard_trend,
)
from app.modules.users.models import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    estimated_delivery_from: str | None = Query(None),
    estimated_delivery_to: str | None = Query(None),
    month: int | None = Query(None, ge=1, le=12),
    year: int | None = Query(None, ge=2020, le=2100),
    customer_name: str | None = Query(None),
    destination_uf: str | None = Query(None, min_length=2, max_length=2),
    carrier_id: int | None = Query(None),
    status: str | None = Query(None),
    criticality: str | None = Query(None),
    sla_status: str | None = Query(None),
    is_late: bool | None = Query(None),
    exception_type: str | None = Query(None),
) -> dict:
    """Endpoint de resumo do dashboard com KPIs operacionais.

    Reaproveita services existentes:
    - SLA service (BETA-013A)
    - Carrier efficiency (BETA-014A)
    - Exceptions panel (BETA-015A)

    Retorna:
        KPIs consolidados, top transportadoras e top exceções
    """
    return calculate_dashboard_summary(
        db,
        estimated_delivery_from=estimated_delivery_from,
        estimated_delivery_to=estimated_delivery_to,
        month=month,
        year=year,
        customer_name=customer_name,
        destination_uf=destination_uf,
        carrier_id=carrier_id,
        status=status,
        criticality=criticality,
        sla_status=sla_status,
        is_late=is_late,
        exception_type=exception_type,
    )


@router.get("/trend")
def dashboard_trend(
    db: Session = Depends(get_db),
    estimated_delivery_from: str | None = Query(None, description="Data inicial (ISO format)"),
    estimated_delivery_to: str | None = Query(None, description="Data final (ISO format)"),
    days: int = Query(30, ge=1, le=90, description="Número de dias para retrospectiva"),
) -> dict:
    """Endpoint de tendência diária dos KPIs para gráficos de séries temporais.

    Args:
        db: Database session
        estimated_delivery_from: Data inicial (ISO format)
        estimated_delivery_to: Data final (ISO format)
        days: Número de dias para retrospectiva (padrão 30, máx 90)

    Returns:
        Dados de tendência diária para gráficos de séries temporais
    """
    return calculate_dashboard_trend(
        db,
        estimated_delivery_from=estimated_delivery_from,
        estimated_delivery_to=estimated_delivery_to,
        days=days,
    )
