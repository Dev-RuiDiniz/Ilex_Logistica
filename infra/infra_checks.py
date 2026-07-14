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


def compose_build_config(path: Path) -> dict[str, dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    in_services = False
    current_service: str | None = None
    in_build = False
    out: dict[str, dict[str, str]] = {}

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
            in_build = False
            continue

        if current_service is None:
            continue

        if line.startswith("    build:"):
            out[current_service] = {}
            in_build = True
            continue

        if in_build and line.startswith("    ") and not line.startswith("      "):
            in_build = False

        if not in_build:
            continue

        if line.startswith("      ") and ":" in stripped:
            key, value = stripped.split(":", 1)
            out[current_service][key.strip()] = value.strip()

    return out


def dockerfile_copy_sources(path: Path) -> list[str]:
    sources: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        stripped = raw.strip()
        if not stripped.startswith("COPY "):
            continue
        parts = stripped.split()
        if len(parts) >= 3:
            sources.append(parts[1])
    return sources


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
