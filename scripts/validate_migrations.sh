#!/bin/bash
# Script de validação de migrations

set -e

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"
API_DIR="$PROJECT_ROOT/apps/api"

echo "🔍 Validando migrations..."

# Verificar se diretório da API existe
if [ ! -d "$API_DIR" ]; then
  echo "❌ ERRO: Diretório da API não encontrado: $API_DIR"
  exit 1
fi

cd "$API_DIR"

# Verificar se Alembic está configurado
if [ ! -f "alembic.ini" ] && [ ! -d "migrations" ]; then
  echo "❌ ERRO: Alembic não está configurado"
  exit 1
fi

# Verificar se migrations podem ser importadas
echo "📦 Verificando importação de migrations..."
python -c "from alembic.config import main; main()" 2>/dev/null || {
  echo "❌ ERRO: Não foi possível importar configuração do Alembic"
  exit 1
}

# Verificar versão atual
echo "🗄️  Verificando versão atual das migrations..."
alembic current

# NOTA: Teste de rollback completo não é viável neste PR
# Será implementado no BETA-004 com ambiente de teste isolado
echo "⚠️  Teste de rollback completo será implementado no BETA-004"
echo "✅ Validação básica de migrations concluída"
