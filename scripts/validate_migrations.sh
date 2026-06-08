#!/usr/bin/env bash
# Script de validação de migrations

set -euo pipefail

# Resolver raiz do repo
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
API_DIR="$PROJECT_ROOT/apps/api"

echo "Validating migrations..."

# Verificar se diretório da API existe
if [ ! -d "$API_DIR" ]; then
  echo "ERROR: API directory not found: $API_DIR"
  exit 1
fi

cd "$API_DIR"

# Verificar se Alembic está configurado
if [ ! -f "alembic.ini" ] && [ ! -d "migrations" ]; then
  echo "ERROR: Alembic not configured"
  exit 1
fi

# Detectar Python de forma portátil
PYTHON_CMD=()
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

# Executar testes de migrations
echo "Running migration tests..."
"${PYTHON_CMD[@]}" -m pytest tests/test_migrations.py -v || {
  echo "ERROR: Migration tests failed"
  exit 1
}

echo "OK: Migration validation passed"
