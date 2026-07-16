from pathlib import Path

from infra.infra_checks import compose_services_summary


def test_c01_compose_has_db_api_and_healthchecks():
    compose_file = Path(__file__).resolve().parents[1] / "docker-compose.yml"
    summary = compose_services_summary(compose_file)

    assert "db" in summary
    assert "api" in summary
    assert summary["db"]["has_healthcheck"] is True
    assert summary["api"]["has_healthcheck"] is True


def test_c01_compose_api_build_targets_monorepo_paths():
    compose_file = Path(__file__).resolve().parents[1] / "docker-compose.yml"
    build = compose_build_config(compose_file)

    assert build["api"]["context"] == ".."
    assert build["api"]["dockerfile"] == "infra/docker/api/Dockerfile"


def test_c01_api_dockerfile_copies_monorepo_api_sources():
    dockerfile = Path(__file__).resolve().parents[1] / "docker" / "api" / "Dockerfile"
    copy_sources = dockerfile_copy_sources(dockerfile)

    assert "apps/api/pyproject.toml" in copy_sources
    assert "apps/api/app" in copy_sources
    assert "apps/api/migrations" in copy_sources
    assert "apps/api/alembic.ini" in copy_sources
    assert "infra/docker/api/api-entrypoint.sh" in copy_sources


def test_c01_api_dockerfile_normalizes_entrypoint_line_endings():
    dockerfile = Path(__file__).resolve().parents[1] / "docker" / "api" / "Dockerfile"
    text = dockerfile.read_text(encoding="utf-8")

    assert "sed -i 's/\\r$//' /usr/local/bin/api-entrypoint.sh" in text
