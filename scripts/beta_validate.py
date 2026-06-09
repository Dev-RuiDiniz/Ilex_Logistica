#!/usr/bin/env python3
"""
Beta validation script - Python version (official)
"""

import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

print("Starting beta validation...")
print("")

# Call validate_migrations.py
result = subprocess.run([sys.executable, str(SCRIPT_DIR / "validate_migrations.py")])
sys.exit(result.returncode)
