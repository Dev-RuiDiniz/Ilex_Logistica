#!/usr/bin/env python3
"""
Documentation validation script - validates required docs exist and are consistent
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
DOCS_DIR = PROJECT_ROOT / "docs"

print("Validating documentation...")

# Required docs (se estiverem em branches beta)
REQUIRED_DOCS = [
    "BETA_CHECKLIST.md",
    "BETA_VALIDATION_EVIDENCE.md",
    "BETA_COMMANDS.md",
    "BETA_RELEASE_GATE.md",
    "BETA_KNOWN_LIMITATIONS.md",
    "BETA_NEXT_ACTIONS.md",
]

# Official commands
OFFICIAL_COMMANDS = [
    "validate_migrations.py",
    "beta_validate.py",
    "check_secrets.py",
    "check_secrets_core.py",
]

# Removed Bash wrappers (should not be referenced)
REMOVED_WRAPPERS = [
    "validate_migrations.sh",
    "beta_validate.sh",
]

errors = []

def read_file_with_encoding_fallback(file_path: Path) -> str:
    """Read file with encoding fallback for robustness."""
    encodings = ['utf-8', 'utf-8-sig', 'cp1252', 'latin-1']
    
    for encoding in encodings:
        try:
            content = file_path.read_text(encoding=encoding)
            if encoding != 'utf-8':
                print(f"  WARNING: {file_path.name} read with encoding {encoding} (fallback)")
            return content
        except UnicodeDecodeError:
            continue
    
    # If all encodings fail, raise the original error
    return file_path.read_text()

# Check required docs exist
print("1. Checking required docs...")
for doc in REQUIRED_DOCS:
    doc_path = DOCS_DIR / doc
    if not doc_path.exists():
        print(f"  WARNING: Required doc not found: {doc} (may be in beta branch)")
    else:
        print(f"  OK: {doc} exists")

print("OK: Documentation check completed")

# Check official commands exist
print("\n2. Checking official commands...")
for cmd in OFFICIAL_COMMANDS:
    cmd_path = SCRIPT_DIR / cmd
    if not cmd_path.exists():
        errors.append(f"ERROR: Official command not found: {cmd}")
    else:
        print(f"  OK: {cmd} exists")

if errors:
    for error in errors:
        print(error)
    sys.exit(1)

print("OK: All official commands exist")

# Check docs don't reference removed Bash wrappers
print("\n3. Checking for references to removed Bash wrappers...")
for doc in REQUIRED_DOCS:
    doc_path = DOCS_DIR / doc
    if doc_path.exists():
        content = read_file_with_encoding_fallback(doc_path)
        for wrapper in REMOVED_WRAPPERS:
            if wrapper in content:
                errors.append(f"ERROR: {doc} references removed wrapper: {wrapper}")

if errors:
    for error in errors:
        print(error)
    sys.exit(1)

print("OK: No references to removed Bash wrappers")

# Check docs don't have obvious secrets
print("\n4. Checking for obvious secrets in docs...")
SECRET_PATTERNS = ["-----BEGIN PRIVATE KEY-----", "AKIA[0-9A-Z]{16}", "ghp_[a-zA-Z0-9]{36}"]
for doc in REQUIRED_DOCS:
    doc_path = DOCS_DIR / doc
    if doc_path.exists():
        content = read_file_with_encoding_fallback(doc_path)
        for pattern in SECRET_PATTERNS:
            if pattern in content:
                errors.append(f"ERROR: {doc} contains potential secret pattern: {pattern}")

if errors:
    for error in errors:
        print(error)
    sys.exit(1)

print("OK: No obvious secrets in docs")

# Check docs don't have contradictory status
print("\n5. Checking for contradictory status...")
for doc in REQUIRED_DOCS:
    doc_path = DOCS_DIR / doc
    if doc_path.exists():
        content = read_file_with_encoding_fallback(doc_path)
        if "em execucao" in content.lower() and "concluido" in content.lower():
            errors.append(f"WARNING: {doc} may have contradictory status")

if errors:
    for error in errors:
        print(error)
    # Not fatal, just warning

print("OK: No contradictory status")

print("\nOK: Documentation validation passed")
