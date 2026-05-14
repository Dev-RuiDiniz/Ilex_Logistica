from __future__ import annotations

from pathlib import Path


def compose_services_summary(path: Path) -> dict[str, dict[str, bool]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    in_services = False
    current_service: str | None = None
    out: dict[str, dict[str, bool]] = {}

    for raw in lines:
        line = raw.rstrip("\n")
        stripped = line.strip()
        if stripped == "services:":
            in_services = True
            continue

        if in_services and line and not line.startswith(" "):
            break

        if not in_services:
            continue

        if line.startswith("  ") and stripped.endswith(":") and not line.startswith("    "):
            current_service = stripped[:-1]
            out[current_service] = {"has_healthcheck": False}
            continue

        if current_service and "healthcheck:" in stripped:
            out[current_service]["has_healthcheck"] = True

    return out
