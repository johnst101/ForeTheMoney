import os
from dataclasses import dataclass

try:
    import boto3
except ImportError:  # pragma: no cover - boto3 is optional in local development
    boto3 = None


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


def _fetch_ssm_parameter(name: str) -> str:
    if boto3 is None:
        raise RuntimeError("boto3 is required to read AWS SSM parameters")

    region = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or "us-east-2"
    client = boto3.client("ssm", region_name=region)
    response = client.get_parameter(Name=name, WithDecryption=True)
    return response["Parameter"]["Value"]


def _resolve_runtime_value(name: str, default: str, env_name: str) -> str:
    value = os.getenv(env_name)
    if value is not None:
        return value

    app_env = os.getenv("APP_ENV", "local")
    if app_env in {"stage", "prod"}:
        parameter_path = f"/forethemoney/{app_env}/{name}"
        try:
            return _fetch_ssm_parameter(parameter_path)
        except Exception:
            return default

    return default


def get_settings() -> Settings:
    app_env = os.getenv("APP_ENV", "local")
    return Settings(
        app_env=app_env,
        database_url=_resolve_runtime_value("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/forethemoney_dev", "DATABASE_URL"),
        secret_key=_resolve_runtime_value("SECRET_KEY", "change-me-in-production", "SECRET_KEY"),
        algorithm=_resolve_runtime_value("ALGORITHM", "HS256", "ALGORITHM"),
        access_token_expire_days=_get_int_env(
            "ACCESS_TOKEN_EXPIRE_DAYS",
            int(_resolve_runtime_value("ACCESS_TOKEN_EXPIRE_DAYS", "7", "ACCESS_TOKEN_EXPIRE_DAYS")),
        ),
    )


settings = get_settings()
