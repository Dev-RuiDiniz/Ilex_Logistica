from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


DEV_JWT_SECRET = "ilex-dev-secret-key-with-at-least-32-bytes"


class Settings(BaseSettings):
    app_name: str = "Ilex API"
    environment: str = "dev"
    debug: bool = False
    database_url: str = "sqlite:///./ilex.db"
    jwt_secret: str = DEV_JWT_SECRET
    jwt_algorithm: str = "HS256"
    jwt_access_minutes: int = 15
    jwt_refresh_minutes: int = 60 * 24 * 7
    operational_timezone: str = "America/Sao_Paulo"
    alert_delivery_max_attempts: int = 3
    external_alert_channels_enabled: bool = False
    daily_report_hour: int = 6
    report_retention_days: int = 365
    audit_retention_days: int = 5 * 365
    cors_allowed_origins: str = "http://localhost:3000,http://127.0.0.1:3000"
    redis_url: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_prefix="ILEX_")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]

    @model_validator(mode="after")
    def validate_production(self) -> "Settings":
        if self.environment.lower() != "production":
            return self
        errors: list[str] = []
        if (
            self.jwt_secret == DEV_JWT_SECRET
            or len(self.jwt_secret.encode()) < 32
            or any(marker in self.jwt_secret.lower() for marker in ("change-me", "placeholder"))
        ):
            errors.append("ILEX_JWT_SECRET deve ter ao menos 32 bytes e nao usar o default")
        database = self.database_url.lower()
        if database.startswith("sqlite"):
            errors.append("SQLite nao e permitido em producao")
        if any(marker in database for marker in ("change-me", "placeholder", "ilex_local_password")):
            errors.append("senha PostgreSQL placeholder nao e permitida")
        origins = self.cors_origins
        if not origins or "*" in origins or any("localhost" in item or "127.0.0.1" in item for item in origins):
            errors.append("CORS de producao exige origens HTTPS explicitas")
        if any(not origin.startswith("https://") for origin in origins):
            errors.append("CORS de producao aceita somente HTTPS")
        if self.debug:
            errors.append("debug deve estar desabilitado em producao")
        if not self.redis_url:
            errors.append("ILEX_REDIS_URL e obrigatoria em producao")
        if errors:
            raise ValueError("; ".join(errors))
        return self


settings = Settings()
