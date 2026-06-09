from datetime import UTC, date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

if TYPE_CHECKING:
    pass


class ImportHistory(Base):
    __tablename__ = "import_histories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(10), nullable=False)
    file_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    rows_received: Mapped[int] = mapped_column(Integer, nullable=False)
    duplicates_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    imported_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rejected_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="SUCCESS")
    # BETA-012A: Additional metadata fields
    source: Mapped[str | None] = mapped_column(String(50), nullable=True)
    import_metadata: Mapped[str | None] = mapped_column(String, nullable=True)  # JSON stored as text
    imported_by: Mapped[int | None] = mapped_column(Integer, nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), index=True
    )


class Delivery(Base):
    __tablename__ = "deliveries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nf: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    transportadora: Mapped[str] = mapped_column(String(255), nullable=False)
    data_coleta: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    valor_frete: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    percentual_frete: Mapped[float] = mapped_column(Numeric(5, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), index=True
    )
