# BETA Operational Runbook

## Como Preparar Ambiente Local/Teste

### Pré-requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Git

### Clonar Repositório

```bash
git clone https://github.com/Dev-RuiDiniz/Ilex_Logistica.git
cd Ilex_Logistica
```

### Configurar Variáveis de Ambiente

**Backend (apps/api):**
- `DATABASE_URL` — URL de conexão PostgreSQL (sem valor real)
- `SECRET_KEY` — Chave secreta do FastAPI (sem valor real)
- `ALGORITHM` — Algoritmo de JWT (ex: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES` — Expiração do token (ex: 30)

**Frontend (apps/web):**
- `NEXT_PUBLIC_API_URL` — URL da API backend (ex: http://localhost:8000)
- `NEXT_PUBLIC_APP_NAME` — Nome da aplicação (ex: Ilex Logística)

### Instalar Dependências

**Backend:**
```bash
cd apps/api
pip install -r requirements.txt
```

**Frontend:**
```bash
cd apps/web
npm install
```

## Como Rodar Migrations

### Upgrades

```bash
cd apps/api
alembic upgrade head
```

### Downgrades

```bash
cd apps/api
alembic downgrade -1
```

### Criar Nova Migration

```bash
cd apps/api
alembic revision --autogenerate -m "descricao_da_migration"
```

## Como Rodar Backend

### Desenvolvimento

```bash
cd apps/api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Produção

```bash
cd apps/api
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## Como Rodar Frontend

### Desenvolvimento

```bash
cd apps/web
npm run dev
```

### Produção

```bash
cd apps/web
npm run build
npm start
```

## Como Executar Validações Oficiais

### Check Secrets

```bash
python scripts/check_secrets.py --repo-root .
python scripts/check_secrets.py --repo-root . --self-test
```

### Validate Migrations

```bash
python scripts/validate_migrations.py
```

### Validate Docs

```bash
python scripts/validate_docs.py
```

### Beta Validate

```bash
python scripts/beta_validate.py
```

## Como Executar Homologação Sintética

### Backend E2E

```bash
cd apps/api
python -m pytest tests/test_beta_e2e_homologation_flow.py -v -rs
```

### Importação Realista

```bash
cd apps/api
python -m pytest tests/test_realistic_import_e2e.py -v -rs
```

### Relatório Diário

```bash
cd apps/api
python -m pytest tests/test_daily_report_api_e2e.py -v -rs
```

### Auditoria

```bash
cd apps/api
python -m pytest tests/test_audit_log_api_e2e.py -v -rs
```

### Contratos Frontend/Backend

```bash
cd apps/api
python -m pytest tests/test_frontend_backend_contract.py -v -rs
```

## Como Interpretar Falhas

### Testes Backend

- **AssertionError** — Validação falhou, verificar assertion message
- **ImportError** — Dependência faltando, instalar com pip
- **SQLAlchemyError** — Problema de banco, verificar migrations
- **HTTPException** — Problema de API, verificar endpoint

### Testes Frontend

- **AssertionError** — Validação falhou, verificar assertion message
- **TypeError** — Problema de tipo, verificar tipos TypeScript
- **NetworkError** — Problema de rede, verificar API backend
- **BuildError** — Problema de build, verificar dependências

### Gates Oficiais

- **check_secrets** — Falso positivo documentado em validate_docs.py:92
- **validate_migrations** — Verificar se migrations estão aplicadas
- **validate_docs** — Verificar documentação obrigatória
- **beta_validate** — Verificar validações consolidadas

## Como Validar Logs/Auditoria

### Backend Logs

Logs do backend são escritos em stdout/stderr e podem ser visualizados em tempo real.

### Audit Logs

Audit logs são registrados no banco de dados e podem ser consultados via API:

```bash
GET /api/v1/audit
```

Filtros disponíveis:
- `event_type` — Tipo de evento
- `entity_type` — Tipo de entidade
- `entity_id` — ID da entidade
- `action` — Ação executada
- `actor_user_id` — ID do usuário
- `severity` — Severidade (info, warning, error, critical)
- `status` — Status (success, failed, skipped)

## Como Validar RBAC

### Backend

Testar endpoints com diferentes papéis:

```bash
cd apps/api
python -m pytest tests/test_rbac_permissions.py -v -rs
python -m pytest tests/test_rbac_audit_api.py -v -rs
python -m pytest tests/test_rbac_reports_api.py -v -rs
python -m pytest tests/test_rbac_alerts_api.py -v -rs
python -m pytest tests/test_rbac_sla_api.py -v -rs
python -m pytest tests/test_rbac_shipments_api.py -v -rs
python -m pytest tests/test_rbac_imports_api.py -v -rs
python -m pytest tests/test_rbac_carriers_api.py -v -rs
python -m pytest tests/test_rbac_users_api.py -v -rs
```

### Frontend

Testar páginas com diferentes permissões:

- Dashboard — Permissão `dashboard:read`
- Importações — Permissão `imports:read`/`imports:write`
- Shipments — Permissão `shipments:read`/`shipments:write`
- Exceções — Permissão `exceptions:read`
- Alertas — Permissão `alerts:read`/`alerts:write`
- Relatório Diário — Permissão `reports:read`/`reports:write`
- Auditoria — Permissão `audit:read`
- Users/RBAC — Permissão `users:read`/`users:write`

## Como Validar Relatórios

### Backend

```bash
cd apps/api
python -m pytest tests/test_daily_report_model.py -v -rs
python -m pytest tests/test_daily_report_generation.py -v -rs
python -m pytest tests/test_daily_report_api.py -v -rs
python -m pytest tests/test_daily_report_integration.py -v -rs
```

### Frontend

Validar página de relatório diário:
- KPIs são exibidos corretamente
- Eficiência por transportadora é calculada
- Alertas ativos são listados
- Falhas de importação são reportadas

## Como Validar Alertas

### Backend

```bash
cd apps/api
python -m pytest tests/test_alerts_model.py -v -rs
python -m pytest tests/test_alerts_generation.py -v -rs
python -m pytest tests/test_alerts_api.py -v -rs
```

### Frontend

Validar página de alertas:
- Alertas são listados corretamente
- Filtros funcionam
- Marcar como lido funciona
- Marcar como resolvido funciona

## Como Validar Importação

### Backend

```bash
cd apps/api
python -m pytest tests/test_braspress_assisted_import.py -v -rs
python -m pytest tests/test_realistic_import_e2e.py -v -rs
```

### Frontend

Validar página de importação:
- Upload de arquivo funciona
- Preview é exibido
- Confirmação funciona
- Erros são reportados

## Como Executar Rollback Técnico

### Rollback de Migrations

```bash
cd apps/api
alembic downgrade -1
```

### Rollback de Código

```bash
git revert <commit>
git push
```

### Rollback de Frontend

```bash
git revert <commit>
cd apps/web
rm -rf .next
npm run build
```

### Validação Pós-Rollback

```bash
cd apps/api
python -m pytest tests/test_beta_e2e_homologation_flow.py -v -rs
python -m pytest tests/test_realistic_import_e2e.py -v -rs
python -m pytest tests/test_daily_report_api_e2e.py -v -rs
python -m pytest tests/test_audit_log_api_e2e.py -v -rs
python -m pytest tests/test_frontend_backend_contract.py -v -rs
```

## Como Registrar Evidências

### Testes

Salvar output de testes:

```bash
cd apps/api
python -m pytest tests/test_beta_e2e_homologation_flow.py -v -rs > evidence_e2e.txt
```

### Gates

Salvar output de gates:

```bash
python scripts/check_secrets.py --repo-root . > evidence_secrets.txt
python scripts/validate_migrations.py > evidence_migrations.txt
python scripts/validate_docs.py > evidence_docs.txt
python scripts/beta_validate.py > evidence_beta_validate.txt
```

### Frontend

Salvar output de build:

```bash
cd apps/web
npm run build > evidence_build.txt
```

## Troubleshooting

### Backend não inicia

- Verificar DATABASE_URL
- Verificar se PostgreSQL está rodando
- Verificar migrations aplicadas

### Frontend não inicia

- Verificar NEXT_PUBLIC_API_URL
- Verificar se backend está rodando
- Verificar dependências instaladas

### Testes falham

- Verificar se banco de teste está configurado
- Verificar se migrations estão aplicadas
- Verificar se fixtures estão disponíveis

### Gates falham

- check_secrets: verificar falso positivo em validate_docs.py:92
- validate_migrations: verificar se migrations estão aplicadas
- validate_docs: verificar documentação obrigatória
- beta_validate: verificar validações consolidadas
