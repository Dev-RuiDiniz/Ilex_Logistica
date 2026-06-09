#!/usr/bin/env bash
# Secret scan - wrapper portátil que chama Python script
# Funciona em Windows/Git Bash e Linux CI

# Descobrir diretório do próprio script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Usar fallback baseado no diretório do script
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PY_SCRIPT="$SCRIPT_DIR/check_secrets.py"

# Localizar Python
if command -v python >/dev/null 2>&1; then
  PYTHON_CMD=(python)
elif command -v python3 >/dev/null 2>&1; then
  PYTHON_CMD=(python3)
elif command -v py >/dev/null 2>&1; then
  PYTHON_CMD=(py -3)
else
  echo "ERROR: Python not found"
  exit 1
fi

# Converter caminhos para Windows se cygpath estiver disponível
if command -v cygpath >/dev/null 2>&1; then
  PY_SCRIPT_FOR_PYTHON="$(cygpath -w "$PY_SCRIPT")"
  REPO_ROOT_FOR_PYTHON="$(cygpath -w "$REPO_ROOT")"
else
  PY_SCRIPT_FOR_PYTHON="$PY_SCRIPT"
  REPO_ROOT_FOR_PYTHON="$REPO_ROOT"
fi

# Executar script Python
"${PYTHON_CMD[@]}" "$PY_SCRIPT_FOR_PYTHON" --repo-root "$REPO_ROOT_FOR_PYTHON" "$@"
