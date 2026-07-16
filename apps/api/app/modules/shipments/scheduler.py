"""Agendamento recorrente da rotina de cobrança de remessas atrasadas.

Executa `run_cobranca` em intervalo configurável (cron) quando
`ILEX_COBRANCA_SCHEDULER_ENABLED=true`. O scheduler é iniciado/parado
no lifespan da aplicação (ver app/main.py).
"""

from __future__ import annotations

import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import settings
from app.database.session import SessionLocal
from app.modules.shipments.cobranca_service import run_cobranca

logger = logging.getLogger("ilex.cobranca.scheduler")

_scheduler: BackgroundScheduler | None = None


def _job() -> None:
    """Executa a rotina de cobrança com os parâmetros padrão do agendamento."""
    try:
        db = SessionLocal()
        try:
            result = run_cobranca(
                db,
                carrier_id=None,
                destination_uf=None,
                dias_min=settings.cobranca_dias_min,
                dias_max=settings.cobranca_dias_max,
            )
            logger.info(
                "cobranca_agendada_concluida",
                extra={
                    "enviadas": result["enviadas"],
                    "puladas_sem_whatsapp": result["puladas_sem_whatsapp"],
                    "falhas": result["falhas"],
                    "critico_escalonado": result["critico_escalonado"],
                },
            )
        finally:
            db.close()
    except Exception as exc:  # noqa: BLE001 - loga e mantém o scheduler vivo
        logger.exception("cobranca_agendada_falhou: %s", exc)


def start_cobranca_scheduler() -> BackgroundScheduler | None:
    """Inicia o scheduler de cobrança se habilitado nas configurações."""
    global _scheduler
    if not settings.cobranca_scheduler_enabled:
        logger.info("cobranca_scheduler_desabilitado")
        return None
    if _scheduler is not None and _scheduler.running:
        return _scheduler
    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        _job,
        "cron",
        **_parse_cron(settings.cobranca_cron),
        id="cobranca_run",
        replace_existing=True,
    )
    _scheduler.start()
    logger.info("cobranca_scheduler_iniciado", extra={"cron": settings.cobranca_cron})
    return _scheduler


def shutdown_cobranca_scheduler() -> None:
    """Encerra o scheduler de cobrança se estiver ativo."""
    global _scheduler
    if _scheduler is not None and _scheduler.running:
        _scheduler.shutdown(wait=False)
    _scheduler = None


def _parse_cron(expr: str) -> dict[str, int | str]:
    """Converte expressão cron de 5 campos em kwargs do APScheduler."""
    parts = expr.strip().split()
    if len(parts) != 5:
        raise ValueError("ILEX_COBRANCA_CRON deve ter 5 campos (minuto hora dia mes dia_semana)")
    minute, hour, day, month, day_of_week = parts
    return {
        "minute": minute,
        "hour": hour,
        "day": day,
        "month": month,
        "day_of_week": day_of_week,
    }
