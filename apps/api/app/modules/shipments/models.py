from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, event
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


def calculate_freight_percentage(freight_value: float | None, invoice_value: float | None) -> float | None:
    """Calcula percentual do frete.
    
    freight_percentage = freight_value / invoice_value * 100
    
    Retorna None quando:
    - invoice_value é zero
    - invoice_value é None
    - freight_value é None
    """
    if invoice_value is None or freight_value is None:
        return None
    
    if invoice_value == 0:
        return None
    
    try:
        return float(freight_value) / float(invoice_value) * 100
    except (ZeroDivisionError, TypeError):
        return None


class Shipment(Base):
    __tablename__ = "shipments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tracking_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    carrier_id: Mapped[int] = mapped_column(Integer, ForeignKey("carriers.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False, index=True)
    estimated_delivery: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    actual_delivery: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    recipient_name: Mapped[str] = mapped_column(String(255), nullable=False)
    recipient_phone: Mapped[str] = mapped_column(String(50), nullable=False)
    origin_address: Mapped[str] = mapped_column(Text, nullable=False)
    destination_address: Mapped[str] = mapped_column(Text, nullable=False)
    meta_data: Mapped[str] = mapped_column(Text, default="{}", nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), onupdate=lambda: datetime.now(UTC), nullable=False)
    
    # Fiscal/financial fields existentes
    invoice_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    invoice_key: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fiscal_document: Mapped[str | None] = mapped_column(String(50), nullable=True)
    amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    delay_days: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    criticality: Mapped[str] = mapped_column(String(20), default="normal", nullable=False)
    
    # Novos campos fiscais/financeiros (BETA-011A)
    freight_value: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    invoice_value: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    freight_percentage: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    collection_departure_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    customer_name: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    destination_uf: Mapped[str | None] = mapped_column(String(2), nullable=True, index=True)


@event.listens_for(Shipment, 'before_insert')
@event.listens_for(Shipment, 'before_update')
def calculate_freight_percentage_on_save(mapper, connection, target):
    if target.freight_value is not None and target.invoice_value is not None:
        target.freight_percentage = calculate_freight_percentage(target.freight_value, target.invoice_value)
    else:
        target.freight_percentage = None


class ImportHistory(Base):
    __tablename__ = "import_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    total_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    valid_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    invalid_rows: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    imported_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    rejected_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    error_details: Mapped[dict] = mapped_column(Text, default=lambda: "{}")
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)


class ShipmentTreatment(Base):
    __tablename__ = "shipment_treatments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    shipment_id: Mapped[int] = mapped_column(Integer, ForeignKey("shipments.id"), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC), nullable=False)
