#!/usr/bin/env python3
"""
Validation script for migrations - Python version (official)
"""

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
API_DIR = PROJECT_ROOT / "apps/api"

print("Validating migrations...")

# Check if API directory exists
if not API_DIR.exists():
    print("ERROR: API directory not found")
    sys.exit(1)

# Check Alembic configuration
alembic_ini = API_DIR / "alembic.ini"
if not alembic_ini.exists() and not (API_DIR / "migrations").exists():
    print("ERROR: Alembic not configured")
    sys.exit(1)

# Check heads
print("Checking Alembic heads...")
result = subprocess.run(["alembic", "heads"], cwd=API_DIR, capture_output=True, text=True)
if result.returncode != 0:
    print(f"ERROR: Failed to check heads: {result.stderr}")
    sys.exit(1)

heads_count = result.stdout.count("(head)")
if heads_count != 1:
    print(f"ERROR: Expected 1 head, found {heads_count}")
    sys.exit(1)
print("OK: Exactly 1 head found")

# Check history
print("Checking Alembic history...")
result = subprocess.run(["alembic", "history"], cwd=API_DIR, capture_output=True, text=True)
if result.returncode != 0:
    print(f"ERROR: Failed to check history: {result.stderr}")
    sys.exit(1)
print("OK: History check passed")

# Run migration tests
print("Running migration tests...")
result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests/test_migrations.py", "-v"],
    cwd=API_DIR,
    capture_output=True,
    text=True
)
print(result.stdout)
if result.returncode != 0:
    print("ERROR: Migration tests failed")
    sys.exit(1)

print("OK: Migration validation passed")
