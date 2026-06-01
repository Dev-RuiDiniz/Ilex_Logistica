from pydantic import BaseModel, ConfigDict, Field


class CarrierBase(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    external_code: str | None = Field(default=None, max_length=80)
    integration_metadata: dict = Field(default_factory=dict)


class CarrierCreate(CarrierBase):
    pass


class CarrierUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=150)
    external_code: str | None = Field(default=None, max_length=80)
    integration_metadata: dict | None = None


class CarrierResponse(CarrierBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    is_active: bool
