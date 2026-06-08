#!/bin/bash
# Script de validação da API

set -e

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"
API_DIR="$PROJECT_ROOT/apps/api"

echo "🔍 Validando API..."

# Verificar se diretório da API existe
if [ ! -d "$API_DIR" ]; then
  echo "❌ ERRO: Diretório da API não encontrado: $API_DIR"
  exit 1
fi

cd "$API_DIR"

# Instalar dependências
echo "📦 Instalando dependências da API..."
if [ -f "pyproject.toml" ]; then
  pip install -e .[dev] --quiet
else
  echo "❌ ERRO: pyproject.toml não encontrado"
  exit 1
fi

# Rodar lint (ruff)
echo "🔧 Rodando lint (ruff)..."
python -m ruff check .

# Rodar testes (pytest)
echo "🧪 Rodando testes (pytest)..."
python -m pytest -q

# Validar migrations (se possível)
echo "🗄️  Validando migrations..."
if [ -d "migrations" ]; then
  alembic current
  echo "✅ Migrations válidas"
else
  echo "⚠️  Diretório de migrations não encontrado"
fi

echo "✅ Validação da API concluída com sucesso"
