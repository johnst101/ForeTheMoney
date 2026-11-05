import sys
import types
from pathlib import Path

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
