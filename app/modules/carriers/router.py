from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_roles
from app.modules.carriers.models import Carrier
from app.modules.carriers.schemas import CarrierCreate, CarrierResponse, CarrierUpdate
from app.modules.users.models import User

router = APIRouter(prefix="/carriers", tags=["carriers"])


@router.post("", response_model=CarrierResponse, status_code=status.HTTP_201_CREATED)
def create_carrier(
    payload: CarrierCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "logistica", "gestor")),
) -> Carrier:
    exists = db.query(Carrier).filter(Carrier.name == payload.name).first()
    if exists:
        raise HTTPException(status_code=409, detail="transportadora ja existe")
    carrier = Carrier(**payload.model_dump())
    db.add(carrier)
    db.flush()
    db.refresh(carrier)
    return carrier


@router.get("", response_model=list[CarrierResponse])
def list_carriers(
    include_inactive: bool = Query(default=False),
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "logistica", "gestor", "auditoria")),
) -> list[Carrier]:
    query = db.query(Carrier)
    if not include_inactive:
        query = query.filter(Carrier.is_active.is_(True))
    return query.order_by(Carrier.id.asc()).all()


@router.put("/{carrier_id}", response_model=CarrierResponse)
def update_carrier(
    carrier_id: int,
    payload: CarrierUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "logistica", "gestor")),
) -> Carrier:
    carrier = db.get(Carrier, carrier_id)
    if carrier is None:
        raise HTTPException(status_code=404, detail="transportadora nao encontrada")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(carrier, field, value)
    db.flush()
    db.refresh(carrier)
    return carrier


@router.post("/{carrier_id}/inactivate", response_model=CarrierResponse)
def inactivate_carrier(
    carrier_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("admin", "logistica", "gestor")),
) -> Carrier:
    carrier = db.get(Carrier, carrier_id)
    if carrier is None:
        raise HTTPException(status_code=404, detail="transportadora nao encontrada")
    carrier.is_active = False
    db.flush()
    db.refresh(carrier)
    return carrier
