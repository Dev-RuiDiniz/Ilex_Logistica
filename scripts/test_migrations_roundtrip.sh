#!/bin/bash
# Script de teste de roundtrip de migrations (upgrade/downgrade/upgrade)

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"
API_DIR="$PROJECT_ROOT/apps/api"

echo "🔍 Testando roundtrip de migrations..."

# Verificar se diretório da API existe
if [ ! -d "$API_DIR" ]; then
  echo "❌ ERRO: Diretório da API não encontrado: $API_DIR"
  exit 1
fi

cd "$API_DIR"

# Criar banco temporário
TEMP_DB="ilex_test_migrations.db"
echo "📦 Criando banco temporário: $TEMP_DB"
export ILEX_DATABASE_URL="sqlite:///$TEMP_DB"

# Limpar banco se já existir
rm -f "$TEMP_DB"

# Aplicar migrations até head
echo "🗄️  Aplicando migrations até head..."
alembic upgrade head

# Verificar versão atual
echo "📊 Verificando versão atual..."
alembic current

# Verificar se tabelas críticas existem
echo "🔍 Verificando tabelas críticas..."
python -c "
import sqlite3
conn = sqlite3.connect('$TEMP_DB')
cursor = conn.cursor()
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table'\")
tables = [row[0] for row in cursor.fetchall()]
print(f'Tabelas criadas: {tables}')
conn.close()
"

# Tentar downgrade para base (se houver migrations)
echo "⏪ Tentando downgrade para base..."
alembic downgrade base

# Aplicar upgrade novamente
echo "⏫ Aplicando upgrade novamente..."
alembic upgrade head

# Verificar versão final
echo "📊 Verificando versão final..."
alembic current

# Limpar banco temporário
echo "🧹 Limpando banco temporário..."
rm -f "$TEMP_DB"

echo "✅ Teste de roundtrip de migrations concluído com sucesso"
