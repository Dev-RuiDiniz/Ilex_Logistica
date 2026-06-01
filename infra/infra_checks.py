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


def _read_env_keys(path: Path) -> set[str]:
    keys: set[str] = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key = line.split("=", 1)[0].strip()
        if key:
            keys.add(key)
    return keys


def env_template_keys(root_env: Path, api_env: Path, web_env: Path) -> dict[str, set[str]]:
    return {
        "root": _read_env_keys(root_env),
        "api": _read_env_keys(api_env),
        "web": _read_env_keys(web_env),
    }


def workflow_step_names(path: Path) -> list[str]:
    steps: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("- name:"):
            steps.append(line.split(":", 1)[1].strip())
    return steps


def observability_has_minimum_sections(path: Path) -> bool:
    text = path.read_text(encoding="utf-8").lower()
    required = [
        "healthcheck da api",
        "logs em comando",
        "simular falha do db",
    ]
    return all(item in text for item in required)
