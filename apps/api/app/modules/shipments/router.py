from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.modules.auth.dependencies import require_permission
from app.modules.users.models import User
from app.modules.shipments.schemas import (
    CobrancaRunRequest,
    CobrancaRunResult,
    ImportConfirmRequest,
    ImportConfirmResponse,
    ShipmentCreate,
    ShipmentDetailResponse,
    ShipmentListResponse,
    ShipmentTreatmentCreate,
    ShipmentTreatmentResponse,
    UploadResponse,
)
from app.modules.shipments.analytics_schemas import CarrierEfficiencyResponse, ExceptionsPanelResponse
from app.modules.shipments.cobranca_service import run_cobranca
from app.modules.shipments.service import (
    create_shipment,
    create_treatment,
    get_shipment_detail,
    list_exception_shipments,
    list_shipments,
    list_treatments,
    parse_csv_file,
    process_import,
)

from app.modules.shipments.analytics_service import calculate_carrier_efficiency
from app.modules.shipments.exceptions_service import get_exceptions_panel

router = APIRouter(prefix="/shipments", tags=["shipments"])


@router.get("", response_model=ShipmentListResponse)
def list_shipments_endpoint(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    status: Annotated[str | None, Query()] = None,
    carrier_id: Annotated[int | None, Query()] = None,
    tracking_code: Annotated[str | None, Query()] = None,
    invoice_number: Annotated[str | None, Query()] = None,
    invoice_key: Annotated[str | None, Query()] = None,
    fiscal_document: Annotated[str | None, Query()] = None,
    criticality: Annotated[str | None, Query()] = None,
    estimated_delivery_from: Annotated[str | None, Query()] = None,
    estimated_delivery_to: Annotated[str | None, Query()] = None,
    due_date_from: Annotated[str | None, Query()] = None,
    due_date_to: Annotated[str | None, Query()] = None,
    collection_departure_from: Annotated[str | None, Query()] = None,
    collection_departure_to: Annotated[str | None, Query()] = None,
    customer_name: Annotated[str | None, Query()] = None,
    destination_uf: Annotated[str | None, Query()] = None,
    month: Annotated[int | None, Query(ge=1, le=12)] = None,
    year: Annotated[int | None, Query()] = None,
    search: Annotated[str | None, Query()] = None,
    sort_by: Annotated[str, Query()] = "created_at",
    sort_order: Annotated[str, Query()] = "desc",
    # Filtros fiscais/financeiros (BETA-031)
    freight_value_min: Annotated[float | None, Query()] = None,
    freight_value_max: Annotated[float | None, Query()] = None,
    invoice_value_min: Annotated[float | None, Query()] = None,
    invoice_value_max: Annotated[float | None, Query()] = None,
    freight_percentage_min: Annotated[float | None, Query()] = None,
    freight_percentage_max: Annotated[float | None, Query()] = None,
    amount_min: Annotated[float | None, Query()] = None,
    amount_max: Annotated[float | None, Query()] = None,
    # Filtros SLA (BETA-1.1)
    sla_status: Annotated[str | None, Query()] = None,
    is_late: Annotated[bool | None, Query()] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipments:read")),
    ) -> ShipmentListResponse:
    # Validar sla_status
    if sla_status and sla_status not in ["critical", "warning", "normal", "unknown"]:
        raise HTTPException(
            status_code=422,
            detail="sla_status inválido. Valores válidos: critical, warning, normal, unknown"
        )
    
    return list_shipments(
        db=db,
        page=page,
        page_size=page_size,
        status=status,
        carrier_id=carrier_id,
        tracking_code=tracking_code,
        invoice_number=invoice_number,
        invoice_key=invoice_key,
        fiscal_document=fiscal_document,
        criticality=criticality,
        estimated_delivery_from=estimated_delivery_from,
        estimated_delivery_to=estimated_delivery_to,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        collection_departure_from=collection_departure_from,
        collection_departure_to=collection_departure_to,
        customer_name=customer_name,
        destination_uf=destination_uf,
        month=month,
        year=year,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
        # Filtros fiscais/financeiros (BETA-031)
        freight_value_min=freight_value_min,
        freight_value_max=freight_value_max,
        invoice_value_min=invoice_value_min,
        invoice_value_max=invoice_value_max,
        freight_percentage_min=freight_percentage_min,
        freight_percentage_max=freight_percentage_max,
        amount_min=amount_min,
        amount_max=amount_max,
        # Filtros SLA (BETA-1.1)
        sla_status=sla_status,
        is_late=is_late,
    )


@router.get("/exceptions", response_model=ShipmentListResponse)
def list_exceptions_endpoint(
    page: Annotated[int, Query(ge=1)] = 1,
    page_size: Annotated[int, Query(ge=1, le=100)] = 20,
    status: Annotated[str | None, Query()] = None,
    criticality: Annotated[str | None, Query()] = None,
    estimated_delivery_from: Annotated[str | None, Query()] = None,
    estimated_delivery_to: Annotated[str | None, Query()] = None,
    due_date_from: Annotated[str | None, Query()] = None,
    due_date_to: Annotated[str | None, Query()] = None,
    customer_name: Annotated[str | None, Query()] = None,
    destination_uf: Annotated[str | None, Query()] = None,
    month: Annotated[int | None, Query()] = None,
    year: Annotated[int | None, Query()] = None,
    search: Annotated[str | None, Query()] = None,
    sort_by: Annotated[str, Query()] = "delay_days",
    sort_order: Annotated[str, Query()] = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipments:read")),
) -> ShipmentListResponse:
    return list_exception_shipments(
        db=db,
        page=page,
        page_size=page_size,
        status=status,
        criticality=criticality,
        estimated_delivery_from=estimated_delivery_from,
        estimated_delivery_to=estimated_delivery_to,
        due_date_from=due_date_from,
        due_date_to=due_date_to,
        customer_name=customer_name,
        destination_uf=destination_uf,
        month=month,
        year=year,
        search=search,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_201_CREATED)
def upload_csv(
    file: UploadFile,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipments:write")),
) -> UploadResponse:
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="arquivo deve ser CSV")

    try:
        file_content = file.file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="erro ao ler arquivo")

    result = parse_csv_file(file_content, db, current_user.id, file.filename)

    return UploadResponse(**result)


@router.post("/import")
def confirm_import(
    payload: ImportConfirmRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipments:write")),
) -> ImportConfirmResponse:
    if not payload.confirm:
        raise HTTPException(status_code=400, detail="confirm deve ser true")

    result = process_import(payload.import_id, db)

    if result["status"] == "failed":
        raise HTTPException(status_code=400, detail=result["errors"][0].message if result["errors"] else "erro ao processar importacao")

    return ImportConfirmResponse(**result)


@router.get("/analytics/carrier-efficiency", response_model=CarrierEfficiencyResponse)
def get_carrier_efficiency(
    estimated_delivery_from: Annotated[str | None, Query()] = None,
    estimated_delivery_to: Annotated[str | None, Query()] = None,
    month: Annotated[int | None, Query()] = None,
    year: Annotated[int | None, Query()] = None,
    customer_name: Annotated[str | None, Query()] = None,
    destination_uf: Annotated[str | None, Query()] = None,
    carrier_id: Annotated[int | None, Query()] = None,
    status: Annotated[str | None, Query()] = None,
    criticality: Annotated[str | None, Query()] = None,
    sla_status: Annotated[str | None, Query()] = None,
    is_late: Annotated[bool | None, Query()] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipments:read")),
) -> CarrierEfficiencyResponse:
    result = calculate_carrier_efficiency(
        db=db,
        estimated_delivery_from=estimated_delivery_from,
        estimated_delivery_to=estimated_delivery_to,
        month=month,
        year=year,
        customer_name=customer_name,
        destination_uf=destination_uf,
        carrier_id=carrier_id,
        status=status,
        criticality=criticality,
        sla_status=sla_status,
        is_late=is_late,
    )
    return CarrierEfficiencyResponse(**result)


@router.get("/analytics/exceptions", response_model=ExceptionsPanelResponse)
def get_exceptions_analytics(
    estimated_delivery_from: Annotated[str | None, Query()] = None,
    estimated_delivery_to: Annotated[str | None, Query()] = None,
    month: Annotated[int | None, Query()] = None,
    year: Annotated[int | None, Query()] = None,
    customer_name: Annotated[str | None, Query()] = None,
    destination_uf: Annotated[str | None, Query()] = None,
    carrier_id: Annotated[int | None, Query()] = None,
    status: Annotated[str | None, Query()] = None,
    criticality: Annotated[str | None, Query()] = None,
    sla_status: Annotated[str | None, Query()] = None,
    is_late: Annotated[bool | None, Query()] = None,
    exception_type: Annotated[str | None, Query()] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipments:read")),
) -> ExceptionsPanelResponse:
    result = get_exceptions_panel(
        db=db,
        estimated_delivery_from=estimated_delivery_from,
        estimated_delivery_to=estimated_delivery_to,
        month=month,
        year=year,
        customer_name=customer_name,
        destination_uf=destination_uf,
        carrier_id=carrier_id,
        status=status,
        criticality=criticality,
        sla_status=sla_status,
        is_late=is_late,
        exception_type=exception_type,
    )
    return ExceptionsPanelResponse(**result)



@router.post("", response_model=ShipmentDetailResponse, status_code=status.HTTP_201_CREATED)
def create_shipment_endpoint(
    payload: ShipmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipments:write")),
) -> ShipmentDetailResponse:
    created = create_shipment(db, payload.model_dump())
    return ShipmentDetailResponse(**created)


@router.get("/{shipment_id}", response_model=ShipmentDetailResponse)
def get_shipment_detail_endpoint(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipments:read")),
) -> ShipmentDetailResponse:
    detail = get_shipment_detail(db, shipment_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="shipment nao encontrado")
    return ShipmentDetailResponse(**detail)


@router.get("/{shipment_id}/treatments", response_model=list[ShipmentTreatmentResponse])
def list_shipment_treatments(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipments:read")),
) -> list[ShipmentTreatmentResponse]:
    return [ShipmentTreatmentResponse(**item) for item in list_treatments(db, shipment_id)]


@router.post("/cobranca/run", response_model=CobrancaRunResult, status_code=status.HTTP_200_OK)
def run_cobranca_endpoint(
    payload: CobrancaRunRequest,
    db: Session = Depends(get_db),
    _read: User = Depends(require_permission("shipments:read")),
    _write: User = Depends(require_permission("shipments:write")),
) -> CobrancaRunResult:
    if payload.dias_max < payload.dias_min:
        raise HTTPException(status_code=422, detail="dias_max deve ser maior ou igual a dias_min")
    result = run_cobranca(
        db,
        carrier_id=payload.carrier_id,
        destination_uf=payload.destination_uf,
        dias_min=payload.dias_min,
        dias_max=payload.dias_max,
    )
    return CobrancaRunResult(**result)


@router.post("/{shipment_id}/treatments", response_model=ShipmentTreatmentResponse, status_code=status.HTTP_201_CREATED)
def create_shipment_treatment(
    shipment_id: int,
    payload: ShipmentTreatmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_permission("shipments:write")),
) -> ShipmentTreatmentResponse:
    created = create_treatment(db, shipment_id, current_user.id, payload.status, payload.comment)
    if created is None:
        raise HTTPException(status_code=404, detail="shipment nao encontrado")
    return ShipmentTreatmentResponse(**created)
