from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.shipments.service import build_daily_report
from app.modules.users.models import User

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/daily")
def daily_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("admin", "logistica", "gestor", "auditoria")),
) -> dict:
    return build_daily_report(db)
