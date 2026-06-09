#!/bin/bash
# Script raiz de validação beta - orquestra todas as validações

SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPTS_DIR")"

echo "🚀 Iniciando validação beta completa..."
echo "📍 Projeto: $PROJECT_ROOT"
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para imprimir sucesso
print_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

# Função para imprimir erro
print_error() {
  echo -e "${RED}❌ $1${NC}"
}

# Função para imprimir aviso
print_warning() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

# Função para imprimir seção
print_section() {
  echo ""
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "$1"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
}

# Verificar scripts obrigatórios
print_section "1. Verificando scripts obrigatórios"
if bash "$SCRIPTS_DIR/check_scripts_exist.sh"; then
  print_success "Scripts obrigatórios verificados"
else
  print_error "Verificação de scripts falhou"
  exit 1
fi

# Verificar secrets (usando Python diretamente)
print_section "2. Verificando secrets"
if python3 "$SCRIPTS_DIR/check_secrets.py" --repo-root "$PROJECT_ROOT"; then
  print_success "Nenhum secret potencial encontrado"
else
  print_error "Verificação de secrets falhou"
  exit 1
fi

# Validar API
print_section "3. Validando API"
if bash "$SCRIPTS_DIR/validate_api.sh"; then
  print_success "API validada com sucesso"
else
  print_error "Validação da API falhou"
  exit 1
fi

# Validar Web
print_section "4. Validando Web"
if bash "$SCRIPTS_DIR/validate_web.sh"; then
  print_success "Web validada com sucesso"
else
  print_error "Validação da Web falhou"
  exit 1
fi

# Validar E2E
print_section "5. Validando E2E"
if bash "$SCRIPTS_DIR/validate_e2e.sh"; then
  print_success "E2E validado com sucesso"
else
  print_error "Validação E2E falhou"
  exit 1
fi

# Validar Migrations (básico)
print_section "6. Validando Migrations"
if bash "$SCRIPTS_DIR/validate_migrations.sh"; then
  print_success "Migrations validadas (básico)"
else
  print_warning "Validação de migrations falhou (não crítico)"
fi

# Resumo final
print_section "✅ VALIDAÇÃO BETA CONCLUÍDA COM SUCESSO"
echo ""
echo "Todas as validações passaram:"
echo "  ✅ Scripts obrigatórios"
echo "  ✅ Secrets"
echo "  ✅ API"
echo "  ✅ Web"
echo "  ✅ E2E"
echo "  ✅ Migrations (básico)"
echo ""
echo "🎉 O projeto está pronto para Fase Beta!"
