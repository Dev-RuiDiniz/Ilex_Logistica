from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Ilex API"
    environment: str = "dev"
    database_url: str = "sqlite:///./ilex.db"
    jwt_secret: str = "ilex-dev-secret-key-with-at-least-32-bytes"
    jwt_algorithm: str = "HS256"
    jwt_access_minutes: int = 30
    jwt_refresh_minutes: int = 60 * 24
    cors_allowed_origins: str = (
        "http://localhost:3000,"
        "http://localhost:3001,"
        "http://localhost:3002,"
        "http://127.0.0.1:3000,"
        "http://127.0.0.1:3001,"
        "http://127.0.0.1:3002"
    )

    model_config = SettingsConfigDict(env_file=".env", env_prefix="ILEX_")

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_allowed_origins.split(",") if origin.strip()]


settings = Settings()
