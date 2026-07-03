from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Ilex API"
    environment: str = "dev"
    database_url: str = "sqlite:///./ilex.db"
    jwt_secret: str = "ilex-dev-secret-key-with-at-least-32-bytes"
    jwt_algorithm: str = "HS256"
    jwt_access_minutes: int = 15
    jwt_refresh_minutes: int = 60 * 24 * 7

    model_config = SettingsConfigDict(env_file=".env", env_prefix="ILEX_")


settings = Settings()
