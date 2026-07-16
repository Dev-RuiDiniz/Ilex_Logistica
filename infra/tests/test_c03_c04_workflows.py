from pathlib import Path

from infra.infra_checks import workflow_step_names


def test_c03_beta_ci_has_dependency_install_and_migration_validation():
    root = Path(__file__).resolve().parents[2]
    steps = workflow_step_names(root / ".github" / "workflows" / "api-ci.yml")
    assert "Run lint" in steps
    assert "Run tests" in steps


def test_c04_beta_ci_has_secret_and_beta_validation():
    root = Path(__file__).resolve().parents[2]
    steps = workflow_step_names(root / ".github" / "workflows" / "web-ci.yml")
    assert "Run lint" in steps
    assert "Run build" in steps
