#!/bin/bash
# Script de validação E2E

set -e

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"
WEB_DIR="$PROJECT_ROOT/apps/web"

echo "🔍 Validando E2E..."

# Verificar se diretório do Web existe
if [ ! -d "$WEB_DIR" ]; then
  echo "❌ ERRO: Diretório do Web não encontrado: $WEB_DIR"
  exit 1
fi

cd "$WEB_DIR"

# Verificar se Playwright está instalado
if ! npx playwright --version > /dev/null 2>&1; then
  echo "❌ ERRO: Playwright não está instalado"
  echo "Execute: npm install"
  exit 1
fi

# Verificar se browsers estão instalados
if ! npx playwright install chromium --dry-run > /dev/null 2>&1; then
  echo "📦 Instalando browsers Playwright..."
  npx playwright install --with-deps chromium
fi

# Rodar testes E2E
echo "🧪 Rodando testes E2E (Playwright)..."
npm run test:e2e

echo "✅ Validação E2E concluída com sucesso"
