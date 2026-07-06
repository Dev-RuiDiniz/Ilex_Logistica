#!/usr/bin/env python3
"""Fail closed until external P4/P5 evidence explicitly authorizes a release."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def blockers(root: Path = ROOT) -> list[str]:
    required_markers = {
        root / "docs/uat/RESULTADO.md": "Conclusão: APROVADA",
        root / "docs/release/GO_LIVE_DECISION.md": "Decisão: GO",
        root / "docs/release/P4_EVIDENCE.md": "Estado: APROVADO",
    }
    missing = []
    for path, marker in required_markers.items():
        content = path.read_text(encoding="utf-8") if path.exists() else ""
        if marker not in {line.strip() for line in content.splitlines()}:
            missing.append(f"{path.relative_to(root)} sem marcador '{marker}'")
    return missing


def main() -> int:
    pending = blockers()
    print(json.dumps({"release_allowed": not pending, "blockers": pending}, indent=2, ensure_ascii=False))
    return int(bool(pending))


if __name__ == "__main__":
    raise SystemExit(main())
