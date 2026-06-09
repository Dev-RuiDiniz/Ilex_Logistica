#!/bin/bash
# Script de validação do Web

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"
WEB_DIR="$PROJECT_ROOT/apps/web"

echo "Validating Web..."

cd "$WEB_DIR"

# Executar testes
npm test || {
  echo "ERROR: Web tests failed"
  exit 1
}

echo "OK: Web validation passed"
