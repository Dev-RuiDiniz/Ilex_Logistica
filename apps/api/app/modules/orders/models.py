from datetime import UTC, date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        UniqueConstraint("source", "external_number", name="uq_orders_source_external_number"),
        Index("ix_orders_status_order_date", "status", "order_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(50), nullable=False)
    external_number: Mapped[str] = mapped_column(String(100), nullable=False)
    order_date: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    customer_name: Mapped[str] = mapped_column(String(255), nullable=False)
    origin_zip: Mapped[str] = mapped_column(String(8), nullable=False)
    origin_uf: Mapped[str] = mapped_column(String(2), nullable=False)
    destination_zip: Mapped[str] = mapped_column(String(8), nullable=False)
    destination_uf: Mapped[str] = mapped_column(String(2), nullable=False)
    weight_kg: Mapped[Decimal] = mapped_column(Numeric(12, 3), nullable=False)
    volume_count: Mapped[int] = mapped_column(Integer, nullable=False)
    goods_value: Mapped[Decimal] = mapped_column(Numeric(14, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="BRL")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="active", index=True)
    import_history_id: Mapped[int] = mapped_column(
        ForeignKey("import_histories.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )


class QuoteRound(Base):
    __tablename__ = "quote_rounds"
    __table_args__ = (
        UniqueConstraint("order_id", "sequence", name="uq_quote_rounds_order_sequence"),
        Index("ix_quote_rounds_status_expires_at", "status", "expires_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"), nullable=False, index=True)
    sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="open", index=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    recommended_quote_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "freight_quotes.id", name="fk_quote_rounds_recommended_quote_id", ondelete="SET NULL", use_alter=True
        ),
        nullable=True,
    )
    selected_quote_id: Mapped[int | None] = mapped_column(
        ForeignKey("freight_quotes.id", name="fk_quote_rounds_selected_quote_id", ondelete="SET NULL", use_alter=True),
        nullable=True,
    )
    selection_mode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    selection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    selected_by: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )


class FreightQuote(Base):
    __tablename__ = "freight_quotes"
    __table_args__ = (
        UniqueConstraint("round_id", "carrier_id", name="uq_freight_quotes_round_carrier"),
        Index("ix_freight_quotes_status_valid_until", "status", "valid_until"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    round_id: Mapped[int] = mapped_column(
        ForeignKey("quote_rounds.id", ondelete="CASCADE"), nullable=False, index=True
    )
    carrier_id: Mapped[int] = mapped_column(ForeignKey("carriers.id", ondelete="RESTRICT"), nullable=False, index=True)
    amount: Mapped[Decimal | None] = mapped_column(Numeric(14, 2), nullable=True)
    transit_days: Mapped[int | None] = mapped_column(Integer, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending", index=True)
    message: Mapped[str | None] = mapped_column(Text, nullable=True)
    source: Mapped[str] = mapped_column(String(20), nullable=False, default="web")
    valid_until: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC)
    )
