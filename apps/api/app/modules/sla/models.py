"""SLA models for BETA-013A."""

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class SlaRule(Base):
    """SLA rule for calculating shipment delivery deadlines."""

    __tablename__ = "sla_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    carrier_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("carriers.id"), nullable=True, index=True)
    destination_uf: Mapped[str | None] = mapped_column(String(2), nullable=True, index=True)
    transit_days: Mapped[int] = mapped_column(Integer, nullable=False)
    warning_threshold_days: Mapped[int] = mapped_column(Integer, nullable=False)
    critical_delay_days: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)
