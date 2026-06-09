"""Daily Report model for BETA-018A."""

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class DailyReport(Base):
    """Daily Report model for operational daily reports."""

    __tablename__ = "daily_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, unique=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="generated", nullable=False, index=True)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False, index=True)
    generated_by_user_id: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    period_start: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    period_end: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    summary_json: Mapped[str] = mapped_column(Text, nullable=True)
    kpis_json: Mapped[str] = mapped_column(Text, nullable=True)
    exceptions_json: Mapped[str] = mapped_column(Text, nullable=True)
    alerts_json: Mapped[str] = mapped_column(Text, nullable=True)
    carrier_efficiency_json: Mapped[str] = mapped_column(Text, nullable=True)
    import_failures_json: Mapped[str] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)
