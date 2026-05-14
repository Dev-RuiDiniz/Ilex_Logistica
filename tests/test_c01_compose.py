from pathlib import Path

from infra_checks import compose_services_summary


def test_c01_compose_has_db_api_and_healthchecks():
    compose_file = Path(__file__).resolve().parents[1] / "docker-compose.yml"
    summary = compose_services_summary(compose_file)

    assert "db" in summary
    assert "api" in summary
    assert summary["db"]["has_healthcheck"] is True
    assert summary["api"]["has_healthcheck"] is True
