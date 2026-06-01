from pathlib import Path

from infra_checks import workflow_step_names


def test_c03_api_ci_has_lint_and_tests():
    root = Path(__file__).resolve().parents[2]
    steps = workflow_step_names(root / "Api" / ".github" / "workflows" / "api-ci.yml")
    assert "Run lint" in steps
    assert "Run tests" in steps


def test_c04_web_ci_has_lint_and_build():
    root = Path(__file__).resolve().parents[2]
    steps = workflow_step_names(root / "Web" / ".github" / "workflows" / "web-ci.yml")
    assert "Run lint" in steps
    assert "Run build" in steps
