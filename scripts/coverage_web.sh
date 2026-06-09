#!/bin/bash
# Script de geração de relatório de cobertura do Web

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"
WEB_DIR="$PROJECT_ROOT/apps/web"

echo "🔍 Gerando relatório de cobertura do Web..."

# Verificar se diretório do Web existe
if [ ! -d "$WEB_DIR" ]; then
  echo "❌ ERRO: Diretório do Web não encontrado: $WEB_DIR"
  exit 1
fi

cd "$WEB_DIR"

# Instalar dependências
echo "📦 Instalando dependências do Web..."
npm ci --silent

# Gerar relatório de cobertura
echo "📊 Gerando relatório de cobertura..."
npm run test:coverage

echo "✅ Relatório de cobertura gerado"
echo "   Terminal: exibido acima"
echo "   HTML: coverage/index.html"
