#!/bin/bash
# Script raiz de validação beta - orquestra todas as validações

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"

echo "Starting beta validation..."
echo "Project: $PROJECT_ROOT"
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para imprimir sucesso
print_success() {
  echo -e "${GREEN}OK: $1${NC}"
}

# Função para imprimir erro
print_error() {
  echo -e "${RED}ERROR: $1${NC}"
}

# Função para imprimir aviso
print_warning() {
  echo -e "${YELLOW}WARNING: $1${NC}"
}

# Função para imprimir seção
print_section() {
  echo ""
  echo "=========================================="
  echo "$1"
  echo "=========================================="
}

# Verificar scripts obrigatórios
print_section "1. Checking required scripts"
if [ -f "$SCRIPTS_DIR/validate_api.sh" ]; then
  print_success "validate_api.sh exists"
else
  print_error "validate_api.sh not found"
  exit 1
fi

if [ -f "$SCRIPTS_DIR/validate_web.sh" ]; then
  print_success "validate_web.sh exists"
else
  print_error "validate_web.sh not found"
  exit 1
fi

# Validar API
print_section "2. Validating API"
cd "$PROJECT_ROOT/apps/api"
python -m pytest tests/test_migrations.py -v || {
  print_error "Migration tests failed"
  exit 1
}
print_success "Migration tests passed"

# Validar Web
print_section "3. Validating Web"
cd "$PROJECT_ROOT/apps/web"
npm test || {
  print_error "Web tests failed"
  exit 1
}
print_success "Web tests passed"

# Resumo final
print_section "BETA VALIDATION COMPLETED"
echo ""
echo "All validations passed:"
echo "  OK: Migration tests"
echo "  OK: Web tests"
echo ""
echo "Project is ready for Beta!"
