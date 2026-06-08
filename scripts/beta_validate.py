#!/usr/bin/env python3
"""
Beta validation script - Python version (official)
Integrates validate_docs.py for documentation validation
"""

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

print("Starting beta validation...")
print(f"Project: {PROJECT_ROOT}")
print("")

# Detect Python
PYTHON_CMD = sys.executable

# Check required scripts
print("1. Checking required scripts")
validate_migrations = SCRIPT_DIR / "validate_migrations.py"
validate_docs = SCRIPT_DIR / "validate_docs.py"

if not validate_migrations.exists():
    print("ERROR: validate_migrations.py not found")
    sys.exit(1)
print("OK: validate_migrations.py exists")

if not validate_docs.exists():
    print("ERROR: validate_docs.py not found")
    sys.exit(1)
print("OK: validate_docs.py exists")

# Validate documentation
print("")
print("2. Validating documentation")
result = subprocess.run([PYTHON_CMD, str(validate_docs)])
if result.returncode != 0:
    print("ERROR: Documentation validation failed")
    sys.exit(1)

# Validate migrations (includes API tests)
print("")
print("3. Validating migrations (includes API tests)")
result = subprocess.run([PYTHON_CMD, str(validate_migrations)])
if result.returncode != 0:
    print("ERROR: Migration validation failed")
    sys.exit(1)

# Summary
print("")
print("==========================================")
print("BETA VALIDATION COMPLETED")
print("==========================================")
print("")
print("Validations passed:")
print("  OK: Documentation validation")
print("  OK: Migration validation (includes API tests)")
print("")
print("Project is ready for Beta!")
