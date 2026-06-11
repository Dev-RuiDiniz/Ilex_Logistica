# BETA Technical Freeze Plan

## O que Fica Congelado

### Escopo Funcional Beta
- Importação com preview e validação
- SLA com cálculo de atraso e criticidade
- Exceções com painel e tratativas
- Alertas automáticos
- Relatório diário consolidado
- Auditoria operacional completa
- RBAC completo

### API Contracts
- Endpoints de importação
- Endpoints de SLA
- Endpoints de exceções
- Endpoints de alertas
- Endpoints de relatório diário
- Endpoints de auditoria
- Endpoints de RBAC
- Schemas Pydantic
- Request/Response models

### Database Schema
- Tabelas de shipments
- Tabelas de importações
- Tabelas de SLA
- Tabelas de exceções
- Tabelas de alertas
- Tabelas de relatórios
- Tabelas de auditoria
- Tabelas de usuários/papéis
- Tabelas de permissões
- Migrations versionadas

### Frontend Components
- Dashboard
- Importações
- Shipments
- Exceções
- Alertas
- Relatório diário
- Auditoria
- Users/RBAC
- AccessDenied
- SlaBadge
- SlaFilters
- AppShell
- Navigation

### Testes Críticos
- test_realistic_import_e2e.py
- test_daily_report_api_e2e.py
- test_audit_log_api_e2e.py
- test_frontend_backend_contract.py
- test_beta_e2e_homologation_flow.py
- Suítes RBAC
- Suítes auditoria
- Suítes relatório diário
- Suítes alertas
- Suítes SLA
- Suítes Braspress/importação

### Gates Oficiais
- check_secrets
- validate_migrations
- validate_docs
- beta_validate

### Documentação Operacional
- Runbook operacional
- Checklist de homologação assistida
- Matriz go/no-go
- Notas de versão
- Manifesto RC
- Índice de evidências
- Plano de congelamento técnico

## O que Pode Mudar Após RC

### Correções de Bugs Críticos
- Bugs que impedem operação
- Bugs que causam data loss
- Bugs que causam security issues

### Hotfixes de Segurança
- Vulnerabilidades de segurança
- Exposição de dados sensíveis
- Falhas de autenticação/autorização

### Ajustes de Configuração
- Ajustes de variáveis de ambiente
- Ajustes de timeouts
- Ajustes de limits

### Melhorias de Performance
- Otimizações de queries
- Otimizações de cache
- Otimizações de build

## Quais Mudanças Exigem Novo Ciclo de Validação

### Mudanças de API
- Adição de novos endpoints
- Mudança de schemas Pydantic
- Mudança de request/response models
- Mudança de autenticação/autorização

### Mudanças de Schema
- Adição de novas tabelas
- Mudança de colunas existentes
- Mudança de migrations
- Mudança de constraints

### Mudanças de Funcionalidade
- Adição de novas features
- Mudança de fluxos existentes
- Mudança de regras de negócio

### Mudanças de Segurança/RBAC
- Adição de novos papéis
- Mudança de permissões
- Mudança de endpoints protegidos
- Mudança de helpers de permissão

## Critérios para Abrir Hotfix

### Bug Crítico que Impede Operação
- Sistema não funciona
- Dados não são persistidos
- Usuários não conseguem acessar

### Vulnerabilidade de Segurança
- Exposição de dados sensíveis
- Falha de autenticação
- Falha de autorização
- SQL injection
- XSS

### Degradação de Performance Severa
- Sistema não responde
- Timeout em operações críticas
- Memory leaks

## Critérios para Rejeitar Hotfix

### Melhoria de Funcionalidade
- Nova feature não planejada
- Melhoria de UX não crítica
- Refactoring não essencial

### Otimização Não Essencial
- Melhoria de performance não crítica
- Refactoring de código
- Melhoria de test coverage

## Validações Obrigatórias Antes de Qualquer Integração

### Gates Oficiais
- check_secrets --repo-root . (1 falso positivo aceito)
- check_secrets --repo-root . --self-test (OK)
- validate_migrations (OK)
- validate_docs (OK)
- beta_validate (OK)

### Backend Crítico
- test_realistic_import_e2e.py (1/1)
- test_daily_report_api_e2e.py (1/1)
- test_audit_log_api_e2e.py (1/1)
- test_frontend_backend_contract.py (2/2)
- test_beta_e2e_homologation_flow.py (1/1)
- Suítes RBAC (76/76)
- Suítes auditoria (54/54)
- Suítes relatório diário (46/46)
- Suítes alertas (24/24)
- Suítes SLA (46/46)
- Suítes Braspress/importação (29/29)

### Frontend
- npm run lint (0 errors)
- npm run test (331/331)
- npm run build (OK)

## Validações Obrigatórias Após Integração Sequencial

### Rodar Testes Críticos
- Backend crítico (281/281)
- Frontend (331/331)

### Validar Migrations
- validate_migrations (OK)
- Testes de migrations (4/4)

### Validar Gates
- check_secrets (1 falso positivo aceito)
- validate_docs (OK)
- beta_validate (OK)

### Validar Rollback
- Testar rollback de migrations
- Testar rollback de código
- Testar rollback de frontend

## Proibição de Merge Direto Sem Gates

### Nenhum Merge Direto Sem Gates Verdes
- Todos os gates oficiais devem estar verdes
- check_secrets pode ter 1 falso positivo aceito
- validate_migrations deve estar OK
- validate_docs deve estar OK
- beta_validate deve estar OK

### Nenhum Merge Direto Sem Testes Críticos
- Backend crítico deve estar verde (281/281)
- Frontend deve estar verde (331/331)
- Lint deve ter 0 errors
- Build deve estar OK

### Nenhum Merge Direto Sem Validação de Rollback
- Rollback de migrations deve funcionar
- Rollback de código deve funcionar
- Rollback de frontend deve funcionar

## Processo de Hotfix

### 1. Abertura de Hotfix
- Identificar bug crítico/vulnerabilidade
- Documentar severidade e impacto
- Justificar necessidade de hotfix

### 2. Desenvolvimento
- Criar branch de hotfix
- Implementar correção mínima
- Não alterar funcionalidade não relacionada

### 3. Validação
- Rodar gates oficiais
- Rodar testes críticos
- Validar rollback
- Documentar mudanças

### 4. Integração
- Criar PR de hotfix
- Revisar mudanças
- Merge apenas após validação completa
- Atualizar documentação

### 5. Pós-Integração
- Monitorar produção
- Coletar feedback
- Documentar aprendizados

## Processo de Rejeição de Hotfix

### 1. Avaliação
- Avaliar severidade e impacto
- Verificar se atende critérios de hotfix
- Verificar se pode esperar próximo release

### 2. Comunicação
- Comunicar rejeição
- Justificar com critérios
- Sugerir alternativa

### 3. Documentação
- Documentar rejeição
- Documentar justificativa
- Documentar alternativa

## Critérios de Descongelamento

### Descongelamento Parcial
- Hotfix aprovado
- Validação completa
- Gates verdes
- Testes críticos verdes

### Descongelamento Total
- Novo ciclo de release
- Novo roadmap
- Novas features
- Validação completa

## Governança

- **Branch:** feature/beta-023b-release-candidate-manifest-freeze
- **Base:** feature/beta-023a-beta-delivery-runbook-handoff
- **Status:** Concluído
- **Merge:** Não realizado
- **Auto-merge:** Não habilitado
- **Force push:** Não utilizado
- **Ação manual:** Não transferida ao usuário
