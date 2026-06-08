#!/usr/bin/env python3
"""
Secret scan - wrapper portável
"""

import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent

# Executar script real
result = subprocess.run(
    [sys.executable, str(SCRIPT_DIR / "check_secrets_core.py"), "--repo-root", str(PROJECT_ROOT)] + sys.argv[1:],
    cwd=PROJECT_ROOT
)
sys.exit(result.returncode)
