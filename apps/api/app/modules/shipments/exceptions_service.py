"""Service de exceções operacionais com SLA para BETA-015A."""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy.orm import Session

from app.modules.carriers.models import Carrier
from app.modules.shipments.models import Shipment
from app.modules.sla.service import calculate_shipment_sla


def classify_exception_type(
    sla_status: str | None,
    criticality: str | None,
    is_late: bool | None,
) -> str | None:
    """Classifica o tipo de exceção baseado em SLA e criticidade.

    Args:
        sla_status: Status do SLA (on_time, warning, late, critical, unknown)
        criticality: Criticidade (normal, baixa, media, alta)
        is_late: Se está atrasado

    Returns:
        Tipo de exceção ou None se não for exceção
    """
    if sla_status is None or sla_status == "unknown":
        return "unknown_sla"
    if sla_status == "critical":
        return "critical"
    elif sla_status == "late":
        return "late"
    elif sla_status == "warning":
        return "warning"
    elif sla_status == "on_time" and criticality == "normal":
        return None
    elif criticality in ("media", "alta"):
        return "late"
    elif criticality == "baixa":
        return "warning"
    else:
        return None


def calculate_exception_priority(
    exception_type: str | None,
    delay_days: int,
    estimated_delivery: datetime | None,
    id: int,
) -> int:
    """Calcula prioridade da exceção para ordenação.

    Prioridade:
    1. critical (mais urgente)
    2. late
    3. warning
    4. unknown_sla (menos urgente)

    Empates:
    - Maior delay_days primeiro
    - Data mais antiga primeiro
    - ID menor primeiro

    Args:
        exception_type: Tipo de exceção
        delay_days: Dias de atraso
        estimated_delivery: Data estimada de entrega
        id: ID do shipment

    Returns:
        Prioridade numérica (menor = mais urgente)
    """
    if exception_type == "critical":
        base_priority = 1
    elif exception_type == "late":
        base_priority = 2
    elif exception_type == "warning":
        base_priority = 3
    elif exception_type == "unknown_sla":
        base_priority = 4
    else:
        base_priority = 999

    # Empate por maior delay_days (inverter para maior delay ter menor priority)
    delay_priority = -delay_days

    return base_priority * 10000 + delay_priority


def calculate_exception_summary(items: list[dict[str, Any]]) -> dict[str, int]:
    """Calcula resumo operacional das exceções.

    Args:
        items: Lista de exceções

    Returns:
        Dicionário com contagens por tipo
    """
    summary = {
        "total_exceptions": len(items),
        "critical_count": 0,
        "late_count": 0,
        "warning_count": 0,
        "unknown_sla_count": 0,
    }

    for item in items:
        exception_type = item.get("exception_type")
        if exception_type == "critical":
            summary["critical_count"] += 1
        elif exception_type == "late":
            summary["late_count"] += 1
        elif exception_type == "warning":
            summary["warning_count"] += 1
        elif exception_type == "unknown_sla":
            summary["unknown_sla_count"] += 1

    return summary


def get_exception_items(
    db: Session,
    estimated_delivery_from: str | None = None,
    estimated_delivery_to: str | None = None,
    month: int | None = None,
    year: int | None = None,
    customer_name: str | None = None,
    destination_uf: str | None = None,
    carrier_id: int | None = None,
    status: str | None = None,
    criticality: str | None = None,
    sla_status: str | None = None,
    is_late: bool | None = None,
    exception_type: str | None = None,
) -> list[dict[str, Any]]:
    """Retorna lista de exceções com filtros aplicados.

    Args:
        db: Database session
        estimated_delivery_from: Data estimada inicial
        estimated_delivery_to: Data estimada final
        month: Mês
        year: Ano
        customer_name: Nome do cliente
        destination_uf: UF de destino
        carrier_id: ID da transportadora
        status: Status
        criticality: Criticidade
        sla_status: Status do SLA
        is_late: Se está atrasado
        exception_type: Tipo de exceção

    Returns:
        Lista de exceções com payload estável
    """
    from sqlalchemy import extract

    query = db.query(Shipment)

    # Aplicar filtros
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

    if month:
        query = query.filter(extract('month', Shipment.estimated_delivery) == month)

    if year:
        query = query.filter(extract('year', Shipment.estimated_delivery) == year)

    if customer_name:
        query = query.filter(Shipment.customer_name.ilike(f"%{customer_name}%"))

    if destination_uf:
        query = query.filter(Shipment.destination_uf == destination_uf)

    if carrier_id:
        query = query.filter(Shipment.carrier_id == carrier_id)

    if status:
        query = query.filter(Shipment.status == status)

    if criticality:
        query = query.filter(Shipment.criticality == criticality)

    items = query.all()

    # Calcular SLA e classificar exceções
    exception_items = []
    for item in items:
        sla_result = calculate_shipment_sla(db, item.id)
        shipment_sla_status = sla_result.get("sla_status")
        shipment_is_late = sla_result.get("is_late", False)

        # Classificar tipo de exceção
        exc_type = classify_exception_type(shipment_sla_status, item.criticality, shipment_is_late)

        # Filtrar por exception_type se especificado
        if exception_type and exc_type != exception_type:
            continue

        # Filtrar por sla_status se especificado
        if sla_status and shipment_sla_status != sla_status:
            continue
        if is_late is not None and shipment_is_late != is_late:
            continue

        # Se não for exceção, não incluir
        if exc_type is None:
            continue

        carrier = db.query(Carrier).filter(Carrier.id == item.carrier_id).first()
        carrier_name = carrier.name if carrier else None

        delay_days = sla_result.get("delay_days", item.delay_days)

        exception_items.append({
            "shipment_id": item.id,
            "tracking_code": item.tracking_code,
            "invoice_number": item.invoice_number,
            "carrier_id": item.carrier_id,
            "carrier_name": carrier_name,
            "customer_name": item.customer_name,
            "destination_uf": item.destination_uf,
            "status": item.status,
            "sla_status": shipment_sla_status,
            "criticality": item.criticality,
            "delay_days": delay_days,
            "sla_due_date": sla_result.get("sla_due_date"),
            "exception_type": exc_type,
            "exception_reason": _get_exception_reason(exc_type, delay_days, shipment_sla_status),
            "priority": calculate_exception_priority(
                exc_type,
                delay_days,
                item.estimated_delivery,
                item.id,
            ),
            "last_update_at": item.updated_at,
        })

    # Ordenar por prioridade
    exception_items.sort(key=lambda x: x["priority"])

    return exception_items


def _get_exception_reason(
    exception_type: str | None,
    delay_days: int,
    sla_status: str | None,
) -> str:
    """Retorna razão da exceção em formato legível."""
    if exception_type == "critical":
        return f"Atraso crítico de {delay_days} dias"
    elif exception_type == "late":
        return f"Atraso de {delay_days} dias"
    elif exception_type == "warning":
        return "Atenção: próximo ao prazo"
    elif exception_type == "unknown_sla":
        return "Sem SLA definido"
    else:
        return "Exceção não classificada"


def get_exceptions_panel(
    db: Session,
    estimated_delivery_from: str | None = None,
    estimated_delivery_to: str | None = None,
    month: int | None = None,
    year: int | None = None,
    customer_name: str | None = None,
    destination_uf: str | None = None,
    carrier_id: int | None = None,
    status: str | None = None,
    criticality: str | None = None,
    sla_status: str | None = None,
    is_late: bool | None = None,
    exception_type: str | None = None,
) -> dict[str, Any]:
    """Retorna painel de exceções com resumo e lista.

    Args:
        db: Database session
        estimated_delivery_from: Data estimada inicial
        estimated_delivery_to: Data estimada final
        month: Mês
        year: Ano
        customer_name: Nome do cliente
        destination_uf: UF de destino
        carrier_id: ID da transportadora
        status: Status
        criticality: Criticidade
        sla_status: Status do SLA
        is_late: Se está atrasado
        exception_type: Tipo de exceção

    Returns:
        Dicionário com summary, items, filters_applied e generated_at
    """
    items = get_exception_items(
        db=db,
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

    summary = calculate_exception_summary(items)

    filters_applied = {
        "estimated_delivery_from": estimated_delivery_from,
        "estimated_delivery_to": estimated_delivery_to,
        "month": month,
        "year": year,
        "customer_name": customer_name,
        "destination_uf": destination_uf,
        "carrier_id": carrier_id,
        "status": status,
        "criticality": criticality,
        "sla_status": sla_status,
        "is_late": is_late,
        "exception_type": exception_type,
    }

    return {
        "summary": summary,
        "items": items,
        "filters_applied": filters_applied,
        "generated_at": datetime.now(UTC).isoformat(),
    }
