"""OperationalAuditLog model for BETA-019A."""

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class OperationalAuditLog(Base):
    """Operational audit log model for tracking system events."""

    __tablename__ = "operational_audit_logs"

    # Identificação
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Evento
    event_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=True, index=True)
    action: Mapped[str] = mapped_column(String(20), nullable=False, index=True)

    # Ator (usuário)
    actor_user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True, index=True
    )
    actor_email: Mapped[str] = mapped_column(String(255), nullable=True, index=True)

    # Contexto
    source: Mapped[str] = mapped_column(String(50), nullable=True)
    severity: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    # Dados de mudança (JSON)
    before_json: Mapped[str] = mapped_column(Text, nullable=True)
    after_json: Mapped[str] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[str] = mapped_column(Text, nullable=True)

    # Metadados de requisição
    request_id: Mapped[str] = mapped_column(String(100), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[str] = mapped_column(Text, nullable=True)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(UTC), nullable=False, index=True
    )
