#!/bin/bash
# Verificação mínima que falha quando scripts obrigatórios não existem (TDD Red)

set -e

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"

echo "🔍 Verificando scripts obrigatórios..."

# Verificar script raiz
if [ ! -f "$SCRIPTS_DIR/beta_validate.sh" ]; then
  echo "❌ ERRO: Script obrigatório não encontrado: scripts/beta_validate.sh"
  exit 1
fi

# Verificar scripts auxiliares
REQUIRED_SCRIPTS=(
  "validate_api.sh"
  "validate_web.sh"
  "validate_e2e.sh"
  "check_secrets.sh"
)

for script in "${REQUIRED_SCRIPTS[@]}"; do
  if [ ! -f "$SCRIPTS_DIR/$script" ]; then
    echo "❌ ERRO: Script obrigatório não encontrado: scripts/$script"
    exit 1
  fi
done

# Verificar comando test:e2e no package.json
if [ ! -f "$PROJECT_ROOT/apps/web/package.json" ]; then
  echo "❌ ERRO: package.json não encontrado em apps/web"
  exit 1
fi

if ! grep -q '"test:e2e"' "$PROJECT_ROOT/apps/web/package.json"; then
  echo "❌ ERRO: script test:e2e não encontrado em apps/web/package.json"
  exit 1
fi

echo "✅ Todos os scripts obrigatórios existem"
echo "✅ Comando test:e2e está configurado"
