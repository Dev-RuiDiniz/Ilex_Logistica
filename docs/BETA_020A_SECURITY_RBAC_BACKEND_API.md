# BETA-020A: Segurança e RBAC Backend/API

## Visão Geral

BETA-020A implementa o backend do sistema de Role-Based Access Control (RBAC) para o Épico 9 — Segurança, usuários, permissões e RBAC. Este PR consolida a autenticação/autorização, define papéis e permissões para a fase beta, e aplica proteção em endpoints críticos.

## Base

- **Branch Base:** `feature/beta-019b-operational-audit-logs-frontend`
- **Branch Atual:** `feature/beta-020a-security-rbac-backend-api`

## Escopo

### 1. Diagnóstico Inicial

#### Estado Atual da Autenticação

**Modelos Existentes:**
- `User`: email, full_name, password_hash, is_active, roles (many-to-many)
- `Role`: name, users (many-to-many)
- `user_roles`: tabela de associação

**Autenticação Atual:**
- JWT-based authentication em `app/modules/auth/`
- `get_current_user()` dependency para obter usuário autenticado
- `require_roles()` dependency para verificar roles específicas
- Token com roles incluído no payload

**Endpoints Protegidos Antes do BETA-020A:**
- SLA rules: `require_roles(["admin"])` para create/update
- Outros endpoints: autenticação básica ou sem proteção

**Gaps Identificados:**
- Sem modelo de Permission granular
- Sem mapeamento de role → permissions
- Endpoints críticos sem proteção (audit, reports, alerts)
- Falta de validação de permissões por resource/action

### 2. Correção da Falha W10

**Falha Original:**
- Teste: `test_w10_daily_report` em `test_shipment_detail_treatments_report_users.py`
- Erro: `KeyError: 'total_shipments'`
- Causa: Teste chamava endpoint `/api/v1/reports/daily` que retorna lista, mas esperava summary direto

**Correção Aplicada:**
1. Atualizado teste para gerar relatório primeiro via `/api/v1/reports/daily/generate`
2. Buscar relatório por data via `/api/v1/reports/daily/by-date/{report_date}`
3. Extrair `total_shipments` de `summary_json` (JSON string)
4. Corrigido `reports/service.py` para serializar datetime com `default=str`

**Resultado:** Teste passando (1/1)

### 3. Matriz RBAC Beta

#### Papéis Definidos

| Papel | Descrição | Permissões |
|-------|-----------|------------|
| **admin** | Administrador do sistema | Todas as permissões |
| **manager** | Gerente operacional | shipments:read, imports:read, sla:read, alerts:read/write, reports:read/write, audit:read |
| **operator** | Operador de logística | shipments:read/write, imports:read/write, alerts:read/write |
| **viewer** | Visualizador | shipments:read, imports:read, sla:read, alerts:read, reports:read |
| **logistica** | Equipe de logística (legado) | shipments:read/write, imports:read/write |
| **gestor** | Gestor (legado) | shipments:read, imports:read, sla:read, alerts:read, reports:read |
| **auditoria** | Auditor (legado) | audit:read, shipments:read, imports:read |

#### Permissões Definidas

| Permissão | Resource | Action | Descrição |
|-----------|----------|--------|-----------|
| shipments:read | shipments | read | Ler shipments |
| shipments:write | shipments | write | Escrever shipments |
| imports:read | imports | read | Ler imports |
| imports:write | imports | write | Escrever imports |
| sla:read | sla | read | Ler regras SLA |
| sla:write | sla | write | Escrever regras SLA |
| alerts:read | alerts | read | Ler alertas |
| alerts:write | alerts | write | Escrever alertas |
| reports:read | reports | read | Ler relatórios |
| reports:write | reports | write | Escrever relatórios |
| audit:read | audit | read | Ler logs de auditoria |
| users:read | users | read | Ler usuários |
| users:write | users | write | Escrever usuários |

#### Regras Beta

- **admin**: Acesso total a todos os recursos
- **manager**: Leitura geral + escrita operacional (alerts, reports)
- **operator**: Operação limitada a shipments/imports/alerts
- **viewer**: Somente leitura
- **audit:read**: Restrito a admin/manager/auditoria
- **sla:write**: Restrito a admin (regras de SLA são sensíveis)

### 4. Implementação de Dependências Backend

#### Novo Modelo: Permission

```python
class Permission(Base):
    __tablename__ = "permissions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resource: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)
    roles: Mapped[list[Role]] = relationship("Role", secondary=role_permissions, back_populates="permissions")
```

#### Nova Tabela: role_permissions

```python
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("permission_id", ForeignKey("permissions.id"), primary_key=True),
)
```

#### Novos Helpers em `auth/dependencies.py`

**`require_permission(permission)`**
- Verifica se usuário tem permissão específica (formato "resource:action")
- Admin tem todas as permissões automaticamente
- Retorna 403 se permissão não encontrada

**`require_any_permission(*permissions)`**
- Verifica se usuário tem qualquer uma das permissões listadas
- Admin tem todas as permissões automaticamente
- Retorna 403 se nenhuma permissão encontrada

**Comportamento:**
- 401 quando não autenticado (herdado de `get_current_user`)
- 403 quando autenticado sem permissão
- Não vaza detalhes sensíveis
- Compatível com testes existentes

### 5. Aplicação de RBAC em Endpoints Críticos

#### Audit Logs

**Endpoints Protegidos:**
- `GET /api/v1/audit` → `require_permission("audit:read")`
- `GET /api/v1/audit/summary` → `require_permission("audit:read")`
- `GET /api/v1/audit/{log_id}` → `require_permission("audit:read")`
- `POST /api/v1/audit` → Público (sistema interno)

**Justificativa:** Audit logs são sensíveis, acesso restrito a admin/manager/auditoria

#### Daily Reports

**Endpoints Protegidos:**
- `POST /api/v1/reports/daily/generate` → `require_permission("reports:write")`
- `GET /api/v1/reports/daily` → `require_permission("reports:read")`
- `GET /api/v1/reports/daily/by-date/{report_date}` → `require_permission("reports:read")`
- `GET /api/v1/reports/daily/{report_id}` → `require_permission("reports:read")`

**Justificativa:** Reports contêm dados operacionais sensíveis

#### Alerts

**Endpoints Protegidos:**
- `GET /api/v1/alerts` → `require_permission("alerts:read")`
- `GET /api/v1/alerts/summary` → `require_permission("alerts:read")`
- `POST /api/v1/alerts/generate` → `require_permission("alerts:write")`
- `PATCH /api/v1/alerts/{alert_id}/read` → `require_permission("alerts:write")`
- `PATCH /api/v1/alerts/{alert_id}/resolve` → `require_permission("alerts:write")`

**Justificativa:** Alerts são operacionais, leitura para todos, escrita para operadores

#### SLA

**Endpoints Protegidos:**
- `POST /api/v1/sla/recalculate` → `require_permission("sla:write")`
- `POST /api/v1/sla/recalculate/{shipment_id}` → `require_permission("sla:write")`
- `GET /api/v1/sla/rules` → `require_permission("sla:read")`
- `POST /api/v1/sla/rules` → `require_roles(["admin"])`
- `PUT /api/v1/sla/rules/{rule_id}` → `require_roles(["admin"])`

**Justificativa:** SLA rules são configuração sensível, restrito a admin

### 6. Testes Obrigatórios

#### Arquivo: `tests/test_rbac_permissions.py`

**Cenários Testados (8/8 passando):**

1. **test_unauthenticated_user_receives_401_on_protected_endpoints**
   - Usuário não autenticado recebe 401 em endpoints protegidos
   - Testa: audit, reports, alerts, sla

2. **test_user_without_permission_receives_403**
   - Usuário sem permissão recebe 403
   - Testa: viewer tentando acessar audit, reports:write

3. **test_admin_can_access_all_endpoints**
   - Admin pode acessar todos os endpoints
   - Testa: audit, reports, alerts, sla

4. **test_manager_can_access_audit_reports_alerts_sla**
   - Manager pode acessar audit, reports, alerts, SLA
   - Testa: leitura conforme matriz

5. **test_operator_cannot_access_audit**
   - Operator não pode acessar audit logs
   - Testa: 403 em /api/v1/audit

6. **test_viewer_can_read_but_not_write**
   - Viewer pode ler mas não escrever
   - Testa: reports:read OK, reports:write 403, alerts:write 403

7. **test_unknown_role_fails_safely**
   - Role desconhecida falha de forma segura
   - Testa: 403 em endpoints protegidos

8. **test_public_endpoints_still_work**
   - Endpoints públicos continuam funcionando
   - Testa: health check, login

### 7. Regressão Backend

#### Audit (BETA-019A)
- Model: 16 passed
- Service: 14 passed
- API: 10 passed
- Integrações: 14 passed
- **Total: 54/54 passed**

#### Reports (BETA-018A)
- Model: 10 passed
- Generation: 19 passed
- API: 11 passed
- **Total: 40/40 passed**

#### Alerts (BETA-017A)
- Model: 9 passed
- Generation: 7 passed
- API: 8 passed
- **Total: 24/24 passed**

#### SLA (BETA-013A)
- Calculation: 14 passed
- Rules: 27 passed
- API: 5 passed
- **Total: 46/46 passed**

#### Imports (BETA-012A)
- Braspress Assisted: 29 passed
- **Total: 29/29 passed**

#### W10 Específico
- `test_w10_daily_report`: 1 passed (corrigido)

**Total Backend: 193/193 passed**

### 8. Regressão Frontend

- **Lint:** 0 errors, 12 warnings (preexistentes, não relacionados a BETA-020A)
- **Testes:** 310 passed (29 test files)
- **Build:** OK (18 static pages, 2 dynamic pages)

### 9. Gates Oficiais

- ✅ **Secret scan:** OK: No potential secrets found
- ✅ **Secret scan self-test:** Self-test completed successfully
- ✅ **Migration validation:** OK (4/4 tests)
- ✅ **Documentation validation:** OK
- ✅ **Beta validate:** OK

### 10. Migração

**Arquivo:** `migrations/versions/20260623_01_add_permissions.py`

**Alterações:**
- Cria tabela `permissions`
- Cria tabela `role_permissions`
- Insere 13 permissões padrão

**Seed:** `app/modules/users/seed_permissions.py`
- Cria permissões se não existirem
- Mapeia permissions para roles conforme matriz

### 11. Limitações

1. **Endpoints Ainda Não Protegidos:**
   - Shipments endpoints (serão protegidos em BETA-020B ou PR específico)
   - Imports endpoints (serão protegidos em BETA-020B ou PR específico)
   - Carriers endpoints (serão protegidos em PR específico)
   - Users endpoints (serão protegidos em BETA-020B)

2. **Motivo Técnico:**
   - Impacto amplo em endpoints existentes
   - Necessário validar compatibilidade com frontend
   - Priorização de endpoints críticos (audit, reports, alerts, SLA)

3. **Frontend:**
   - Não implementado neste PR (backend-first)
   - Será implementado em BETA-020B

### 12. Próximos Passos (BETA-020B)

1. Implementar frontend de RBAC:
   - Página de gestão de usuários
   - Página de gestão de roles
   - Página de gestão de permissões
   - UI para atribuir permissions a roles

2. Proteger endpoints restantes:
   - Shipments (read/write)
   - Imports (read/write)
   - Carriers (read/write)
   - Users (read/write)

3. Implementar redesign de login (se necessário)

4. Considerar SSO/OAuth externo (fase pós-beta)

## Validações Finais

- ✅ Matriz RBAC definida
- ✅ Helpers de permissão implementados
- ✅ Endpoints críticos protegidos (audit, reports, alerts, SLA)
- ✅ Testes 401/403/admin/manager/operator/viewer passando (8/8)
- ✅ Falha W10 corrigida (test_w10_daily_report)
- ✅ Auditoria BETA-019A continua verde (54/54)
- ✅ Frontend BETA-019B continua verde (310/310)
- ✅ Gates oficiais verdes
- ✅ Git status limpo
- ✅ Migração aplicada com sucesso

## Governança

- Não houve merge
- Não houve auto-merge
- Não houve force push
- Não houve comando destrutivo
- Draft PR será criado
- Comentário final será publicado pela IA/agente
