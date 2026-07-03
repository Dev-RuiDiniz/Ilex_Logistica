from pathlib import Path

from scripts.release_gate import blockers


def test_release_gate_fails_closed_without_external_approvals(tmp_path: Path) -> None:
    (tmp_path / "docs/uat").mkdir(parents=True)
    (tmp_path / "docs/release").mkdir(parents=True)
    (tmp_path / "docs/uat/RESULTADO.md").write_text("Conclusão: BLOQUEADA", encoding="utf-8")
    (tmp_path / "docs/release/GO_LIVE_DECISION.md").write_text("Decisão: PENDENTE", encoding="utf-8")
    (tmp_path / "docs/release/P4_EVIDENCE.md").write_text("Estado: BLOQUEADO", encoding="utf-8")
    assert len(blockers(tmp_path)) == 3


def test_release_gate_accepts_only_all_required_markers(tmp_path: Path) -> None:
    (tmp_path / "docs/uat").mkdir(parents=True)
    (tmp_path / "docs/release").mkdir(parents=True)
    (tmp_path / "docs/uat/RESULTADO.md").write_text("Conclusão: APROVADA", encoding="utf-8")
    (tmp_path / "docs/release/GO_LIVE_DECISION.md").write_text("Decisão: GO", encoding="utf-8")
    (tmp_path / "docs/release/P4_EVIDENCE.md").write_text("Estado: APROVADO", encoding="utf-8")
    assert blockers(tmp_path) == []
