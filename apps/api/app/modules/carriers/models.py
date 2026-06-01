from sqlalchemy import Boolean, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Carrier(Base):
    __tablename__ = "carriers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False, unique=True, index=True)
    external_code: Mapped[str | None] = mapped_column(String(80), nullable=True)
    integration_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
