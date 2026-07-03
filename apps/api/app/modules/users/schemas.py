from pydantic import BaseModel, EmailStr, Field, field_validator


class UserCreateRequest(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=1)
    password: str = Field(min_length=12)
    roles: list[str] = Field(default_factory=list)

    @field_validator("password")
    @classmethod
    def validate_password_policy(cls, value: str) -> str:
        checks = (
            any(char.islower() for char in value),
            any(char.isupper() for char in value),
            any(char.isdigit() for char in value),
            any(not char.isalnum() for char in value),
        )
        if not all(checks):
            raise ValueError("a senha deve conter maiúscula, minúscula, número e símbolo")
        return value


class UserUpdateRequest(BaseModel):
    full_name: str | None = None
    roles: list[str] | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    roles: list[str]
