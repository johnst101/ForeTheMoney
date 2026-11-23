import sys
import types
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app import config


def test_get_settings_uses_local_defaults(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("ALGORITHM", raising=False)
    monkeypatch.delenv("ACCESS_TOKEN_EXPIRE_DAYS", raising=False)

    settings = config.get_settings()

    assert settings.app_env == "local"
    assert settings.database_url.endswith("forethemoney_dev")
    assert settings.secret_key == "change-me-in-production"
    assert settings.algorithm == "HS256"
    assert settings.access_token_expire_days == 7


def test_get_settings_reads_ssm_when_not_local(monkeypatch):
    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.delenv("ALGORITHM", raising=False)
    monkeypatch.delenv("ACCESS_TOKEN_EXPIRE_DAYS", raising=False)
    monkeypatch.setenv("AWS_REGION", "us-east-2")

    values = {
        "/forethemoney/prod/DATABASE_URL": "postgresql+psycopg2://prod-db:secret@db.example.com:5432/forethemoney_prod",
        "/forethemoney/prod/SECRET_KEY": "prod-secret",
        "/forethemoney/prod/ALGORITHM": "HS512",
        "/forethemoney/prod/ACCESS_TOKEN_EXPIRE_DAYS": "30",
    }

    class FakeSSMClient:
        def get_parameter(self, Name, WithDecryption):
            return {"Parameter": {"Value": values[Name]}}

    monkeypatch.setattr(
        config,
        "boto3",
        types.SimpleNamespace(client=lambda service, region_name=None: FakeSSMClient()),
        raising=False,
    )

    settings = config.get_settings()

    assert settings.app_env == "prod"
    assert settings.database_url == values["/forethemoney/prod/DATABASE_URL"]
    assert settings.secret_key == values["/forethemoney/prod/SECRET_KEY"]
    assert settings.algorithm == values["/forethemoney/prod/ALGORITHM"]
    assert settings.access_token_expire_days == 30


def _clear_settings_env(monkeypatch):
    """Unset every env var that get_settings() reads for setting values."""
    for name in ("DATABASE_URL", "SECRET_KEY", "ALGORITHM", "ACCESS_TOKEN_EXPIRE_DAYS"):
        monkeypatch.delenv(name, raising=False)


def _use_failing_ssm(monkeypatch):
    """Install a fake boto3 whose SSM client fails every lookup."""
    class FailingSSMClient:
        def get_parameter(self, Name, WithDecryption):
            raise RuntimeError("AccessDenied")

    monkeypatch.setattr(
        config,
        "boto3",
        types.SimpleNamespace(client=lambda service, region_name=None: FailingSSMClient()),
        raising=False,
    )


def test_get_settings_fails_when_secret_key_unresolved_in_prod(monkeypatch):
    database_url = "postgresql+psycopg2://u:db-password@db.example.com:5432/forethemoney_prod"
    _clear_settings_env(monkeypatch)
    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.setenv("DATABASE_URL", database_url)
    _use_failing_ssm(monkeypatch)

    with pytest.raises(config.MissingRequiredSettingError, match="/forethemoney/prod/SECRET_KEY") as exc_info:
        config.get_settings()

    assert database_url not in str(exc_info.value)


def test_get_settings_fails_when_database_url_unresolved_in_stage(monkeypatch):
    _clear_settings_env(monkeypatch)
    monkeypatch.setenv("APP_ENV", "stage")
    monkeypatch.setenv("SECRET_KEY", "stage-secret")
    _use_failing_ssm(monkeypatch)

    with pytest.raises(config.MissingRequiredSettingError, match="/forethemoney/stage/DATABASE_URL"):
        config.get_settings()


def test_get_settings_fails_when_boto3_unavailable_in_prod(monkeypatch):
    _clear_settings_env(monkeypatch)
    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.setattr(config, "boto3", None, raising=False)

    with pytest.raises(config.MissingRequiredSettingError, match="/forethemoney/prod/"):
        config.get_settings()


def test_get_settings_prefers_env_and_defaults_optional_settings_when_ssm_fails(monkeypatch):
    database_url = "postgresql+psycopg2://u:p@db.example.com:5432/forethemoney_prod"
    _clear_settings_env(monkeypatch)
    monkeypatch.setenv("APP_ENV", "prod")
    monkeypatch.setenv("DATABASE_URL", database_url)
    monkeypatch.setenv("SECRET_KEY", "prod-secret")
    _use_failing_ssm(monkeypatch)

    settings = config.get_settings()

    assert settings.database_url == database_url
    assert settings.secret_key == "prod-secret"
    assert settings.algorithm == "HS256"
    assert settings.access_token_expire_days == 7
