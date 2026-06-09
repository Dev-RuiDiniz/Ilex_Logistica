#!/bin/bash
# Script de geração de relatório de cobertura da API

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"
API_DIR="$PROJECT_ROOT/apps/api"

echo "🔍 Gerando relatório de cobertura da API..."

# Verificar se diretório da API existe
if [ ! -d "$API_DIR" ]; then
  echo "❌ ERRO: Diretório da API não encontrado: $API_DIR"
  exit 1
fi

cd "$API_DIR"

# Instalar dependências com coverage
echo "📦 Instalando dependências da API com coverage..."
pip install -e .[dev] --quiet

# Gerar relatório de cobertura
echo "📊 Gerando relatório de cobertura..."
pytest --cov=app --cov-report=term --cov-report=xml --cov-report=html --cov-fail-under=0 -q

echo "✅ Relatório de cobertura gerado"
echo "   Terminal: exibido acima"
echo "   XML: coverage.xml"
echo "   HTML: htmlcov/index.html"
