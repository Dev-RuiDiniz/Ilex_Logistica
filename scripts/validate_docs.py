#!/usr/bin/env python3
"""Validate the current governance documents and SDD specification catalog."""

import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
SPECS_DIR = PROJECT_ROOT / "docs" / "specs"

ROOT_DOCS = [
    "AGENTS.md",
    "ARQUITETURA.md",
    "BANCO_DADOS.md",
    "CONTEXTO.md",
    "ESCOPO.md",
    "RELATORIO.md",
    "ROADMAP.md",
    "ESCOPO_PROJETO_ILEX_LOGISTICA_APENDICE_1.md",
]
SPEC_DOCS = [
    "README.md",
    "01-autenticacao-usuarios-rbac.md",
    "02-transportadoras.md",
    "03-importacoes-braspress.md",
    "04-entregas-monitoradas.md",
    "05-sla-atrasos-criticidade.md",
    "06-tratativas-excecoes.md",
    "07-eficiencia-transportadoras.md",
    "08-dashboard-indicadores.md",
    "09-alertas-notificacoes.md",
    "10-relatorios-exportacoes.md",
    "11-auditoria-historico.md",
    "12-pedidos-cotacao-frete.md",
]
OFFICIAL_COMMANDS = [
    "validate_migrations.py",
    "beta_validate.py",
    "check_secrets.py",
    "check_secrets_core.py",
]
REMOVED_WRAPPERS = ["validate_migrations.sh", "beta_validate.sh"]
SECRET_PATTERNS = [
    re.compile(r"-----BEGIN PRIVATE KEY-----"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"ghp_[a-zA-Z0-9]{36}"),
]


def fail(errors: list[str]) -> None:
    for error in errors:
        print(f"ERROR: {error}")
    sys.exit(1)


print("Validating documentation...")
errors: list[str] = []
documents: list[Path] = []

print("1. Checking required governance documents...")
for name in ROOT_DOCS:
    path = PROJECT_ROOT / name
    if not path.is_file():
        errors.append(f"required root document not found: {name}")
    else:
        documents.append(path)

for name in SPEC_DOCS:
    path = SPECS_DIR / name
    if not path.is_file():
        errors.append(f"required SDD specification not found: docs/specs/{name}")
    else:
        documents.append(path)

if errors:
    fail(errors)
print(f"  OK: {len(documents)} required documents found")

print("2. Checking official validation commands...")
for command in OFFICIAL_COMMANDS:
    if not (SCRIPT_DIR / command).is_file():
        errors.append(f"official command not found: scripts/{command}")
if errors:
    fail(errors)
print(f"  OK: {len(OFFICIAL_COMMANDS)} commands found")

print("3. Checking document content...")
for path in documents:
    content = path.read_text(encoding="utf-8")
    is_source_appendix = path.name == "ESCOPO_PROJETO_ILEX_LOGISTICA_APENDICE_1.md"
    if not is_source_appendix and not content.startswith("# "):
        errors.append(f"document must start with an H1 heading: {path.relative_to(PROJECT_ROOT)}")
    for wrapper in REMOVED_WRAPPERS:
        if wrapper in content:
            errors.append(f"removed wrapper referenced in {path.relative_to(PROJECT_ROOT)}: {wrapper}")
    for pattern in SECRET_PATTERNS:
        if pattern.search(content):
            errors.append(f"potential secret in {path.relative_to(PROJECT_ROOT)}")

if errors:
    fail(errors)
print("  OK: headings, command references and secret patterns")

print("4. Checking LOG-027 through LOG-041 traceability...")
index = (SPECS_DIR / "README.md").read_text(encoding="utf-8")
all_specs = "\n".join(path.read_text(encoding="utf-8") for path in SPECS_DIR.glob("*.md"))
for number in range(27, 42):
    log_id = f"LOG-{number:03d}"
    if log_id not in index:
        errors.append(f"{log_id} missing from docs/specs/README.md")
    if log_id not in all_specs:
        errors.append(f"{log_id} missing from specification catalog")
if errors:
    fail(errors)
print("  OK: LOG-027 through LOG-041 are indexed and specified")

print("OK: Documentation validation passed")
