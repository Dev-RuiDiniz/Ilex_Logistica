from pathlib import Path

from infra.infra_checks import observability_has_minimum_sections


def test_c05_observability_doc_has_health_logs_and_failure_playbook():
    doc = Path(__file__).resolve().parents[1] / "OBSERVABILITY.md"
    assert observability_has_minimum_sections(doc) is True
