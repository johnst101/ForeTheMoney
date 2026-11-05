import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_env: str = "local"
    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/forethemoney_dev"
    secret_key: str = "change-me-in-production"
    algorithm: str = "HS256"
    access_token_expire_days: int = 7


def _get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default

    try:
        return int(value)
    except ValueError:
        return default


def get_settings() -> Settings:
    return Settings(
        app_env=os.getenv("APP_ENV", "local"),
        database_url=os.getenv(
            "DATABASE_URL",
            "postgresql+psycopg2://postgres:postgres@localhost:5432/forethemoney_dev",
        ),
        secret_key=os.getenv("SECRET_KEY", "change-me-in-production"),
        algorithm=os.getenv("ALGORITHM", "HS256"),
        access_token_expire_days=_get_int_env("ACCESS_TOKEN_EXPIRE_DAYS", 7),
    )


settings = get_settings()
