#!/bin/bash
# Script de validação do Web

set -e

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"
WEB_DIR="$PROJECT_ROOT/apps/web"

echo "🔍 Validando Web..."

# Verificar se diretório do Web existe
if [ ! -d "$WEB_DIR" ]; then
  echo "❌ ERRO: Diretório do Web não encontrado: $WEB_DIR"
  exit 1
fi

cd "$WEB_DIR"

# Instalar dependências
echo "📦 Instalando dependências do Web..."
if [ -f "package.json" ]; then
  npm ci --silent
else
  echo "❌ ERRO: package.json não encontrado"
  exit 1
fi

# Rodar lint
echo "🔧 Rodando lint..."
npm run lint

# Rodar testes unitários
echo "🧪 Rodando testes unitários..."
npm run test

# Rodar build
echo "🏗️  Rodando build..."
npm run build

echo "✅ Validação do Web concluída com sucesso"
