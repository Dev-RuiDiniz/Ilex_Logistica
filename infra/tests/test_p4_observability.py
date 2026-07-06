from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_prometheus_and_exporters_are_private_and_configured() -> None:
    compose = (ROOT / "docker-compose.prod.yml").read_text(encoding="utf-8")
    prometheus = (ROOT / "prometheus.yml").read_text(encoding="utf-8")
    assert "prometheus:" in compose
    assert "postgres-exporter:" in compose
    assert "redis-exporter:" in compose
    assert "node-exporter:" in compose
    assert "monitoring:" in compose and "internal: true" in compose
    assert "api:8000" in prometheus


def test_alert_rules_and_runbooks_cover_required_failures() -> None:
    rules = (ROOT / "prometheus-rules.yml").read_text(encoding="utf-8")
    runbooks = (ROOT / "RUNBOOKS.md").read_text(encoding="utf-8").lower()
    for alert in (
        "IlexApiUnavailable",
        "IlexHigh5xxRate",
        "IlexPostgresUnavailable",
        "IlexRedisUnavailable",
        "IlexPendingQuotesBacklog",
        "IlexBackupStale",
    ):
        assert alert in rules
    for topic in ("api indisponível", "postgresql indisponível", "redis indisponível", "migration falhou", "import travado", "backup falhou", "rollback"):
        assert topic in runbooks
