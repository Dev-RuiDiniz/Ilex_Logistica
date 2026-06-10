from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_permission
from app.modules.reports.service import generate_daily_report, get_daily_report_by_date, list_daily_reports
from app.modules.reports.schemas import (
    DailyReportGenerateRequest,
    DailyReportResponse,
    DailyReportListResponse,
)

router = APIRouter(prefix="/reports", tags=["reports"])


@router.post("/daily/generate", response_model=DailyReportResponse)
def generate_report(
    request: DailyReportGenerateRequest,
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("reports:write")),
) -> DailyReportResponse:
    """Generate or regenerate a daily report for a specific date.

    Args:
        request: Report generation request
        db: Database session

    Returns:
        Generated daily report
    """
    report = generate_daily_report(
        db,
        request.report_date,
        request.period_start,
        request.period_end,
        request.generated_by_user_id,
    )
    return DailyReportResponse.model_validate(report)


@router.get("/daily", response_model=DailyReportListResponse)
def list_reports(
    date_from: datetime | None = Query(None, description="Filter by date from"),
    date_to: datetime | None = Query(None, description="Filter by date to"),
    status: str | None = Query(None, description="Filter by status"),
    limit: int = Query(100, ge=1, le=1000, description="Limit results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("reports:read")),
) -> DailyReportListResponse:
    """List daily reports with filters.

    Args:
        date_from: Filter by date from
        date_to: Filter by date to
        status: Filter by status
        limit: Limit results
        offset: Offset for pagination
        db: Database session

    Returns:
        List of daily reports
    """
    reports = list_daily_reports(db, date_from, date_to, status, limit, offset)
    total = len(reports)  # For simplicity, actual count query could be added
    
    return DailyReportListResponse(
        reports=[DailyReportResponse.model_validate(r) for r in reports],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/daily/by-date/{report_date}", response_model=DailyReportResponse)
def get_report_by_date(
    report_date: str,
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("reports:read")),
) -> DailyReportResponse:
    """Get daily report by date.

    Args:
        report_date: Report date in ISO format
        db: Database session

    Returns:
        Daily report
    """
    try:
        date_obj = datetime.fromisoformat(report_date.replace("Z", "+00:00"))
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    
    report = get_daily_report_by_date(db, date_obj)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return DailyReportResponse.model_validate(report)


@router.get("/daily/{report_id}", response_model=DailyReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    _user: object = Depends(require_permission("reports:read")),
) -> DailyReportResponse:
    """Get daily report by ID.

    Args:
        report_id: Report ID
        db: Database session

    Returns:
        Daily report
    """
    from app.modules.reports.models import DailyReport
    
    report = db.query(DailyReport).filter(DailyReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    return DailyReportResponse.model_validate(report)
