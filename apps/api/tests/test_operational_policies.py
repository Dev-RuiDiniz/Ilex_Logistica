from app.core.config import Settings


def test_politicas_operacionais_possuem_defaults_homologados():
    settings = Settings()
    assert settings.operational_timezone == "America/Sao_Paulo"
    assert settings.alert_delivery_max_attempts == 3
    assert settings.daily_report_hour == 6
    assert settings.report_retention_days == 365
    assert settings.audit_retention_days == 5 * 365
    assert settings.external_alert_channels_enabled is False
