"""Service de geração de relatório diário para BETA-018A / BETA-028."""

import csv
import json
import logging
from datetime import UTC, datetime
from io import StringIO

from sqlalchemy.orm import Session

from app.modules.dashboard.service import calculate_dashboard_summary
from app.modules.alerts.service import get_active_alerts_count
from app.modules.reports.models import DailyReport
from app.modules.audit.service import AuditLogService
from app.modules.audit.schemas import AuditLogCreateRequest

logger = logging.getLogger(__name__)


def generate_daily_report(
    db: Session,
    report_date: datetime,
    period_start: datetime | None = None,
    period_end: datetime | None = None,
    generated_by_user_id: int | None = None,
) -> DailyReport:
    """Gera relatório diário consolidando dados dos serviços existentes.

    Fontes:
    - dashboard summary (BETA-016A)
    - alerts service (BETA-017A)
    - carrier efficiency (BETA-014A)
    - exceptions service (BETA-015A)
    - ImportHistory (BETA-012A)

    Args:
        db: Database session
        report_date: Data do relatório
        period_start: Início do período (opcional)
        period_end: Fim do período (opcional)
        generated_by_user_id: ID do usuário que gerou (opcional)

    Returns:
        DailyReport criado/atualizado
    """
    # Consolidar dados do dashboard summary
    dashboard_data = calculate_dashboard_summary(
        db,
        estimated_delivery_from=period_start.isoformat() if period_start else None,
        estimated_delivery_to=period_end.isoformat() if period_end else None,
    )

    # Obter contagem de alertas ativos
    active_alerts_count = get_active_alerts_count(db)

    # Construir JSONs para armazenamento
    summary_json = {
        "total_shipments": dashboard_data.get("total_shipments", 0),
        "on_time_count": dashboard_data.get("on_time_count", 0),
        "late_count": dashboard_data.get("late_count", 0),
        "critical_count": dashboard_data.get("critical_count", 0),
        "warning_count": dashboard_data.get("warning_count", 0),
        "unknown_sla_count": dashboard_data.get("unknown_sla_count", 0),
        "exceptions_count": dashboard_data.get("exceptions_count", 0),
        "import_failure_count": dashboard_data.get("import_failure_count", 0),
        "carriers_count": dashboard_data.get("carriers_count", 0),
    }

    kpis_json = {
        "active_alerts_count": active_alerts_count,
        "delivery_rate": (
            (dashboard_data.get("on_time_count", 0) / dashboard_data.get("total_shipments", 1) * 100)
            if dashboard_data.get("total_shipments", 0) > 0
            else 0
        ),
    }

    exceptions_json = json.dumps(dashboard_data.get("top_exceptions", []), default=str)

    alerts_json = []  # Top alertas podem ser derivados do alerts service se necessário

    carrier_efficiency_json = json.dumps(dashboard_data.get("top_carriers_by_efficiency", []), default=str)

    import_failures_json = {
        "rejected_count": dashboard_data.get("import_failure_count", 0),
    }

    # Verificar se já existe relatório para a data (upsert)
    existing_report = (
        db.query(DailyReport)
        .filter(DailyReport.report_date == report_date)
        .first()
    )

    if existing_report:
        # Atualizar relatório existente
        existing_report.status = "generated"
        existing_report.generated_at = datetime.now(UTC)
        existing_report.generated_by_user_id = generated_by_user_id
        existing_report.period_start = period_start
        existing_report.period_end = period_end
        existing_report.summary_json = json.dumps(summary_json)
        existing_report.kpis_json = json.dumps(kpis_json)
        existing_report.exceptions_json = exceptions_json
        existing_report.alerts_json = json.dumps(alerts_json)
        existing_report.carrier_efficiency_json = carrier_efficiency_json
        existing_report.import_failures_json = json.dumps(import_failures_json)
        db.commit()
        db.refresh(existing_report)
        
        # Audit log
        try:
            audit_log = AuditLogCreateRequest(
                event_type="daily_report_generated",
                entity_type="daily_report",
                entity_id=existing_report.id if existing_report else None,
                action="create",
                source="system",
                severity="info",
                status="success",
                message=f"Relatório diário gerado para {report_date}",
                metadata_json=f'{{"report_date": "{report_date}"}}',
            )
            AuditLogService.create_log(db, audit_log)
        except Exception as e:
            logger.error(f"Failed to create audit log for daily report: {e}")
        
        return existing_report
    else:
        # Criar novo relatório
        report = DailyReport(
            report_date=report_date,
            status="generated",
            generated_at=datetime.now(UTC),
            generated_by_user_id=generated_by_user_id,
            period_start=period_start,
            period_end=period_end,
            summary_json=json.dumps(summary_json),
            kpis_json=json.dumps(kpis_json),
            exceptions_json=exceptions_json,
            alerts_json=json.dumps(alerts_json),
            carrier_efficiency_json=carrier_efficiency_json,
            import_failures_json=json.dumps(import_failures_json),
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        
        # Audit log
        try:
            audit_log = AuditLogCreateRequest(
                event_type="daily_report_generated",
                entity_type="daily_report",
                entity_id=report.id if report else None,
                action="create",
                source="system",
                severity="info",
                status="success",
                message=f"Relatório diário gerado para {report_date}",
                metadata_json=f'{{"report_date": "{report_date}"}}',
            )
            AuditLogService.create_log(db, audit_log)
        except Exception as e:
            logger.error(f"Failed to create audit log for daily report: {e}")
        
        return report


def get_daily_report_by_date(db: Session, report_date: datetime) -> DailyReport | None:
    """Busca relatório diário por data.

    Args:
        db: Database session
        report_date: Data do relatório

    Returns:
        DailyReport ou None se não encontrado
    """
    return (
        db.query(DailyReport)
        .filter(DailyReport.report_date == report_date)
        .first()
    )


def list_daily_reports(
    db: Session,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    status: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> list[DailyReport]:
    """Lista relatórios diários com filtros.

    Args:
        db: Database session
        date_from: Data inicial do período
        date_to: Data final do período
        status: Status do relatório
        limit: Limite de resultados
        offset: Offset para paginação

    Returns:
        Lista de DailyReport
    """
    query = db.query(DailyReport)

    if date_from:
        query = query.filter(DailyReport.report_date >= date_from)

    if date_to:
        query = query.filter(DailyReport.report_date <= date_to)

    if status:
        query = query.filter(DailyReport.status == status)

    return (
        query.order_by(DailyReport.report_date.desc())
        .limit(limit)
        .offset(offset)
        .all()
    )


def count_daily_reports(
    db: Session,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    status: str | None = None,
) -> int:
    """Conta total de relatórios diários com filtros.

    Args:
        db: Database session
        date_from: Data inicial do período
        date_to: Data final do período
        status: Status do relatório

    Returns:
        Total count
    """
    query = db.query(DailyReport)

    if date_from:
        query = query.filter(DailyReport.report_date >= date_from)

    if date_to:
        query = query.filter(DailyReport.report_date <= date_to)

    if status:
        query = query.filter(DailyReport.status == status)

    return query.count()


def export_daily_reports(
    db: Session,
    format: str,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    status: str | None = None,
) -> tuple[str, str, str]:
    """Exporta relatórios diários para CSV ou JSON.

    Args:
        db: Database session
        format: Formato de exportação ('csv' ou 'json')
        date_from: Data inicial do período
        date_to: Data final do período
        status: Status do relatório

    Returns:
        Tupla (content, filename, media_type)
    """
    reports = list_daily_reports(db, date_from, date_to, status, limit=10000, offset=0)

    if format.lower() == "csv":
        return _export_csv(reports)
    elif format.lower() == "json":
        return _export_json(reports)
    else:
        raise ValueError(f"Formato não suportado: {format}. Use 'csv' ou 'json'.")


def _export_csv(reports: list[DailyReport]) -> tuple[str, str, str]:
    """Exporta relatórios para CSV."""
    output = StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "id",
        "report_date",
        "status",
        "generated_at",
        "generated_by_user_id",
        "period_start",
        "period_end",
        "total_shipments",
        "on_time_count",
        "late_count",
        "critical_count",
        "warning_count",
        "unknown_sla_count",
        "exceptions_count",
        "import_failure_count",
        "carriers_count",
        "active_alerts_count",
        "delivery_rate",
        "notes",
        "created_at",
        "updated_at",
    ])

    for report in reports:
        summary = json.loads(report.summary_json) if report.summary_json else {}
        kpis = json.loads(report.kpis_json) if report.kpis_json else {}

        writer.writerow([
            report.id,
            report.report_date.isoformat() if report.report_date else "",
            report.status,
            report.generated_at.isoformat() if report.generated_at else "",
            report.generated_by_user_id or "",
            report.period_start.isoformat() if report.period_start else "",
            report.period_end.isoformat() if report.period_end else "",
            summary.get("total_shipments", 0),
            summary.get("on_time_count", 0),
            summary.get("late_count", 0),
            summary.get("critical_count", 0),
            summary.get("warning_count", 0),
            summary.get("unknown_sla_count", 0),
            summary.get("exceptions_count", 0),
            summary.get("import_failure_count", 0),
            summary.get("carriers_count", 0),
            kpis.get("active_alerts_count", 0),
            kpis.get("delivery_rate", 0),
            report.notes or "",
            report.created_at.isoformat() if report.created_at else "",
            report.updated_at.isoformat() if report.updated_at else "",
        ])

    filename = f"daily_reports_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.csv"
    return output.getvalue(), filename, "text/csv; charset=utf-8"


def _export_json(reports: list[DailyReport]) -> tuple[str, str, str]:
    """Exporta relatórios para JSON."""
    data = []
    for report in reports:
        data.append({
            "id": report.id,
            "report_date": report.report_date.isoformat() if report.report_date else None,
            "status": report.status,
            "generated_at": report.generated_at.isoformat() if report.generated_at else None,
            "generated_by_user_id": report.generated_by_user_id,
            "period_start": report.period_start.isoformat() if report.period_start else None,
            "period_end": report.period_end.isoformat() if report.period_end else None,
            "summary": json.loads(report.summary_json) if report.summary_json else {},
            "kpis": json.loads(report.kpis_json) if report.kpis_json else {},
            "exceptions": json.loads(report.exceptions_json) if report.exceptions_json else [],
            "alerts": json.loads(report.alerts_json) if report.alerts_json else [],
            "carrier_efficiency": json.loads(report.carrier_efficiency_json) if report.carrier_efficiency_json else [],
            "import_failures": json.loads(report.import_failures_json) if report.import_failures_json else {},
            "notes": report.notes,
            "created_at": report.created_at.isoformat() if report.created_at else None,
            "updated_at": report.updated_at.isoformat() if report.updated_at else None,
        })

    json_str = json.dumps(data, indent=2, ensure_ascii=False, default=str)
    filename = f"daily_reports_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.json"
    return json_str, filename, "application/json; charset=utf-8"
