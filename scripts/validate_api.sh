#!/bin/bash
# Script de validação da API

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"
API_DIR="$PROJECT_ROOT/apps/api"

echo "Validating API..."

cd "$API_DIR"

# Executar testes
python -m pytest -q || {
  echo "ERROR: API tests failed"
  exit 1
}

echo "OK: API validation passed"
