from pathlib import Path

from infra_checks import workflow_step_names


def test_c03_beta_ci_has_dependency_install_and_migration_validation():
    root = Path(__file__).resolve().parents[2]
    steps = workflow_step_names(root / ".github" / "workflows" / "beta-ci.yml")
    assert "Install dependencies" in steps
    assert "Validate migrations" in steps


def test_c04_beta_ci_has_secret_and_beta_validation():
    root = Path(__file__).resolve().parents[2]
    steps = workflow_step_names(root / ".github" / "workflows" / "beta-ci.yml")
    assert "Secret scan" in steps
    assert "Beta validation" in steps
