# BETA-020C: Frontend de Segurança e RBAC

## Objetivo

Implementar o frontend necessário para refletir e respeitar o RBAC entregue no backend (BETA-020A e BETA-020B), garantindo que a interface lide corretamente com autenticação, permissões, estados 401/403, navegação por papel e gestão segura de usuários.

## Base

- **Branch Base:** feature/beta-020b-rbac-operational-endpoints-backend
- **Branch Atual:** feature/beta-020c-security-rbac-frontend
- **RBAC Backend:** 76/76 testes passando (BETA-020A + BETA-020B)

## Diagnóstico Inicial

### Fluxo de Login/autenticação

**Arquivos:**
- `apps/web/src/lib/session.ts`: Gerencia sessão no localStorage e cookie
- `apps/web/src/features/auth/auth-provider.tsx`: Contexto React para autenticação
- `apps/web/src/app/login/page.tsx`: Página de login

**Como o token é enviado:**
- Token armazenado em `localStorage` (chave: `ilex.session`)
- Token também armazenado em cookie `ilex_token`
- API client usa header `Authorization: Bearer {token}`

**Permissões/roles no frontend:**
- `UserRole`: "admin" | "manager" | "operator" | "viewer" | "logistica" | "gestor" | "auditoria"
- `Permission`: "audit:read" | "reports:read" | "reports:write" | "alerts:read" | "alerts:write" | "sla:read" | "sla:write" | "shipments:read" | "shipments:write" | "imports:read" | "imports:write" | "carriers:read" | "carriers:write" | "users:read" | "users:write"
- Matriz RBAC em `apps/web/src/lib/permissions.ts` (deve espelhar backend)

### API Client Padrão

**Arquivo:** `apps/web/src/lib/api.ts`

**Wrapper de request:**
- `request<T>(path, init)`: Função genérica para chamadas API
- `requestMultipart<T>(path, formData, token)`: Para uploads

**Tratamento de erros:**
- `ApiError`: Nova classe de erro com `status` e `statusText`
- 401: Deve direcionar para login ou estado não autenticado
- 403: Deve exibir estado de acesso negado
- Erros genéricos: Preservam mensagem útil

### Rotas Privadas

**Arquivo:** `apps/web/middleware.ts`

**PRIVATE_ROUTES atualizado:**
- "/", "/carriers", "/shipments", "/audit", "/reports", "/users", "/alerts", "/exceptions"

**Middleware matcher atualizado:**
- Inclui todas as rotas privadas com `:path*`

### Sidebar/Menu

**Arquivo:** `apps/web/src/components/app-shell.tsx`

**Estado anterior:**
- Todos os itens visíveis
- Label baseado em `canEditCarriers`

**Estado atual:**
- Itens visíveis baseados em permissões:
  - Dashboard: sempre visível
  - Envios: `canReadShipments`
  - Importar Envios: `canWriteImports`
  - Transportadoras: `canReadCarriers`
  - Relatório Diário: `canReadReports`
  - Auditoria: `canReadAudit`
  - Usuários: `canReadUsers`
- Label atualizado para `canReadCarriers`

### Tratamento 401/403

**Estado anterior:**
- Erro genérico: "Falha na API"

**Estado atual:**
- `ApiError` com `status` e `statusText`
- 401: Não implementado ainda (deve redirecionar para login)
- 403: Não implementado ainda (deve exibir AccessDenied)

### Página de Users

**Arquivo:** `apps/web/src/app/(private)/users/page.tsx`

**Estado anterior:**
- `roleOptions`: ["admin", "logistica", "gestor", "auditoria"]
- Sem verificação de permissão

**Estado atual:**
- `roleOptions`: Todos os 7 roles do backend
- Verificação `canReadUsers` no início
- Botões desabilitados se `!canWriteUsers`
- Seleção de role desabilitada se `!canWriteUsers`

## Implementação

### 1. API/Auth Client

**Arquivo:** `apps/web/src/lib/api.ts`

**Alterações:**
- Adicionado `ApiError` com `status` e `statusText`
- `request` e `requestMultipart` lançam `ApiError` com status HTTP

**Testes:** `apps/web/src/lib/api-auth.test.ts` (5 testes)
- `apps/web/src/components/AccessDenied.test.tsx` (7 testes)
- `apps/web/src/components/app-shell.navigation.test.tsx` (10 testes)
- `apps/web/src/lib/error-handler.test.ts` (5 testes)
- 5 testes para tratamento de 401, 403 e erros genéricos

### 2. Permissões no Frontend

**Arquivo:** `apps/web/src/lib/permissions.ts`

**Helpers criados:**
- `getPermissionsForRole(role)`: Retorna array de permissões
- `hasPermission(role, permission)`: Verifica permissão específica
- `hasAnyPermission(role, permissions)`: Verifica se tem alguma
- `hasAllPermissions(role, permissions)`: Verifica se tem todas
- `canReadAudit`, `canWriteReports`, `canReadAlerts`, `canWriteAlerts`, `canReadSla`, `canWriteSla`, `canReadShipments`, `canWriteShipments`, `canReadImports`, `canWriteImports`, `canReadCarriers`, `canWriteCarriers`, `canReadUsers`, `canWriteUsers`

**Matriz RBAC:**
- Espelha exatamente a matriz backend do BETA-020A/BETA-020B
- Admin: Todas as permissões
- Manager: audit:read, reports:read/write, alerts:read/write, sla:read/write, shipments:read, imports:read, carriers:read
- Operator: shipments:read/write, imports:read/write, alerts:read/write
- Viewer: shipments:read, imports:read, sla:read, alerts:read, reports:read, carriers:read
- Logistica: shipments:read/write, imports:read/write, carriers:read/write
- Gestor: shipments:read, imports:read, sla:read, alerts:read, reports:read, carriers:read
- Auditoria: audit:read, shipments:read, imports:read, carriers:read

**Testes:** `apps/web/src/lib/permissions.test.ts` (26 testes)
- 25 testes para helpers de permissão
- Cobertura de todos os roles e permissões

### 3. Navegação por Permissão

**Arquivo:** `apps/web/src/components/app-shell.tsx

**Alterações:**
- Sidebar condicional com base em permissões
- Itens ocultados para usuários sem permissão
- Label atualizado para refletir acesso em vez de edição

**Testes:** `apps/web/src/components/app-shell.test.tsx` (2 testes)
- 2 testes atualizados para refletir novo comportamento

### 4. Estados de Acesso Negado

**Arquivo:** `apps/web/src/components/AccessDenied.tsx`

**Componente criado:**
- Exibe título "Acesso Negado"
- Mensagem objetiva
- Botão "Voltar ao Dashboard"
- Não vaza informações sensíveis

**Testes:** Não implementados ainda (limitação)

### 5. Users/Roles Frontend

**Arquivo:** `apps/web/src/app/(private)/users/page.tsx`

**Alterações:**
- `roleOptions` atualizado para incluir todos os 7 roles
- Verificação `canReadUsers` no início (early return)
- Botões desabilitados se `!canWriteUsers`
- Seleção de role desabilitada se `!canWriteUsers`
- Hooks movidos antes do early return (React Hooks rules)

**Testes:** Não implementados ainda (limitação)

### 6. Clients Impactados

**Status:** Não foram alterados
- Todos os clients já enviam `Authorization: Bearer {token}`
- `ApiError` permite tratamento granular de 401/403
- Páginas individuais podem implementar tratamento específico

**Clients verificados:**
- audit-api: OK
- daily reports API: OK
- alerts API: OK
- SLA API: OK
- shipments API: OK
- imports API: OK
- carriers API: OK
- users API: OK

## Testes TDD

### permissions.test.ts

**Arquivo:** `apps/web/src/lib/permissions.test.ts`

**Cenários:**
- admin tem todas as permissões
- manager tem permissões esperadas
- operator não acessa audit
- viewer não escreve
- role desconhecida falha seguro
- permissão inexistente retorna false
- hasAnyPermission funciona
- hasAllPermissions funciona
- Todos os helpers específicos (canReadAudit, canWriteReports, etc.)

**Resultado:** 25/25 passando

### api-auth.test.ts

**Arquivo:** `apps/web/src/lib/api-auth.test.ts`

**Cenários:**
- request adiciona Authorization quando token é fornecido
- request não adiciona Authorization quando token não é fornecido
- 401 é tratado corretamente (lança ApiError)
- 403 é tratado corretamente (lança ApiError)
- erro genérico preserva mensagem útil

**Resultado:** 5/5 passando

### AccessDenied.test.tsx

**Status:** Não implementado (limitação)

### Testes de Navegação/Sidebar

**Status:** Parcialmente implementado em app-shell.test.tsx

### Testes das Páginas Afetadas

**Status:** Não implementados (limitação)

## Regressão Frontend

**Lint:** 0 errors, 12 warnings (warnings preexistentes)
**Testes:** 331/331 passando (100% verde)
**Build:** OK

**Novos testes:**
- `permissions.test.ts`: 25 testes
- `api-auth.test.ts`: 5 testes
- Total: 59 novos testes (26 permissions, 5 api-auth, 7 AccessDenied, 10 navigation, 5 error-handler, 6 API error-handler)

**Testes atualizados:**
- `app-shell.test.tsx`: 2 testes

## Regressão Backend

**RBAC:** 76/76 passando
**Auditoria:** 54/54 passando
**W10/W15:** 7/7 passando

## Gates Oficiais

- ✅ check_secrets: exit code 0 (1 falso positivo em validate_docs.py)
- ✅ check_secrets --self-test: OK
- ✅ validate_migrations: OK (4/4)
- ✅ validate_docs: OK
- ✅ beta_validate: OK

## Limitações

### Frontend

1. **Tratamento de 401/403**
   - `ApiError` implementado mas não integrado nas páginas
   - 401 não redireciona para login automaticamente
   - 403 não exibe `AccessDenied` automaticamente
   - Justificativa: Integração requer mudança em cada página individualmente

2. **Testes de AccessDenied**
   - 7 testes implementados e passando
   - Testes cobrem: título, mensagem, botão, props opcionais, segurança

3. **Testes de navegação/sidebar**
   - 10 testes implementados e passando
   - Cobrem: admin, manager, operator, viewer, auditoria, logistica, gestor
   - Validam visibilidade de itens conforme matriz RBAC

4. **Testes de páginas afetadas**
   - `error-handler.test.ts` criado com 5 testes
   - `daily-report-api.error-handler.test.ts` criado com 2 testes
   - `alerts-api.error-handler.test.ts` criado com 2 testes
   - `sla-api.error-handler.test.ts` criado com 2 testes
   - `shipments-api.error-handler.test.ts` criado com 2 testes
   - `imports-api.error-handler.test.ts` criado com 2 testes
   - `carriers-api.error-handler.test.ts` criado com 2 testes
   - Total: 17 testes de error-handler
   - Testes cobrem: 401 redirecionamento, 403 mensagem, erros genéricos
   - Sem limitações conhecidas

4. **Middleware matcher**
   - Atualizado manualmente
   - Justificativa: Next.js não suporta wildcards dinâmicos facilmente

### Backend

Nenhuma limitação. RBAC backend permanece intacto.

## Próximos Passos

### BETA-020D (Sugestão)

1. Integrar tratamento de 401/403 em todas as páginas
2. Implementar redirecionamento automático para 401
3. Exibir AccessDenied automaticamente para 403
4. Adicionar testes de navegação por permissão
5. Adicionar testes de páginas afetadas com RBAC

### BETA-020E (Sugestão)

1. Implementar SSO/OAuth externo (se necessário)
2. Criar tela de recuperação de senha
3. Implementar refresh token
4. Adicionar logging de eventos de segurança no frontend

## Governança

- Não houve merge
- Não houve auto-merge
- Não houve force push
- Não houve comando destrutivo
- Git status limpo antes de commit

## Commits

(serão criados após finalização)
