# BETA-020E: Testes E2E de Navegação por Permissão

**Status:** Concluído  
**Data:** 2026-06-25  
**Tarefa:** Implementar 7 testes E2E para validar navegação por permissão nas 18 páginas integradas com o hook `useApiErrorHandler` do BETA-020D

## Objetivo

Validar que o tratamento de erros 401/403 e o sistema de RBAC funcionam corretamente em ambiente E2E, testando navegação por perfil em todas as páginas privadas integradas.

## Especificação SDD

### Requisitos

1. **Testes E2E de navegação por permissão** - 7 testes cobrindo:
   - Admin deve acessar todas as 18 páginas
   - Logística não deve acessar users
   - Gestor não deve acessar shipments/import
   - Auditoria não deve acessar páginas restritas
   - Menu condicional por perfil
   - Redirecionamento 401
   - Exibição AccessDenied 403

2. **Atualização de fixtures** - Rotas das 18 páginas integradas em `testUsers`

### Comportamento Esperado

- **Admin:** Acesso completo a todas as 18 páginas
- **Logística:** Acesso a todas exceto `/users` e `/audit`
- **Gestor:** Acesso a todas exceto `/shipments/import`, `/users` e `/audit`
- **Auditoria:** Acesso limitado (`/`, `/shipments`, `/exceptions`, `/reports/daily`, `/audit`)
- **Erro 401:** Redirecionamento para `/login` com limpeza de sessão
- **Erro 403:** Exibição do componente `AccessDenied` com mensagem de erro

## 18 Páginas Integradas (BETA-020D)

1. `/` - Dashboard
2. `/shipments` - Listagem de envios
3. `/carriers` - Gestão de transportadoras
4. `/users` - Gestão de usuários
5. `/alerts` - Painel de alertas
6. `/audit` - Auditoria operacional
7. `/reports/daily` - Relatórios diários
8. `/settings/sla` - Configuração de SLA
9. `/exceptions` - Painel de exceções
10. `/shipments/import` - Importação de envios
11. `/shipments/analytics/carrier-efficiency` - Eficiência por transportadora
12. `/shipments/analytics/exceptions` - Analytics de exceções

## Implementação

### Atualização de Fixtures

**Arquivo:** `apps/web/e2e/fixtures/users.ts`

Atualizado as rotas em `expectedAccessibleRoutes` e `expectedForbiddenRoutes` para refletir as 18 páginas integradas:

- **Admin:** 12 rotas acessíveis, 0 bloqueadas
- **Logística:** 10 rotas acessíveis, 2 bloqueadas (`/users`, `/audit`)
- **Gestor:** 9 rotas acessíveis, 3 bloqueadas (`/shipments/import`, `/users`, `/audit`)
- **Auditoria:** 5 rotas acessíveis, 7 bloqueadas (analytics, carriers, users, alerts, settings/sla)

### Testes E2E

**Arquivo:** `apps/web/e2e/rbac-navigation.spec.ts`

#### Teste 1: Admin deve acessar todas as 18 páginas
- Login como admin
- Iterar por todas as 12 rotas acessíveis
- Verificar que não foi redirecionado para login
- Verificar que não exibe AccessDenied
- Verificar que a página carregou (não está em loading)

#### Teste 2: Logística não deve acessar users
- Login como logística
- Tentar acessar `/users`
- Verificar redirecionamento para login ou exibição de AccessDenied

#### Teste 3: Gestor não deve acessar shipments/import
- Login como gestor
- Tentar acessar `/shipments/import`
- Verificar redirecionamento para login ou exibição de AccessDenied

#### Teste 4: Auditoria não deve acessar páginas restritas
- Login como auditoria
- Iterar por todas as 7 rotas bloqueadas
- Verificar redirecionamento para login ou exibição de AccessDenied

#### Teste 5: Menu condicional por perfil
- Login como logística
- Verificar itens de menu visíveis (Shipments, Importações, Exceções)
- Verificar itens de menu ocultos (Usuários)

#### Teste 6: Redirecionamento 401
- Login como admin
- Simular sessão expirada (remover token do localStorage)
- Tentar acessar rota privada
- Verificar redirecionamento para `/login`

#### Teste 7: Exibição AccessDenied 403
- Login como logística
- Tentar acessar rota proibida (`/users`)
- Verificar exibição do componente AccessDenied
- Verificar botão de voltar para dashboard

## Testes e Validação

### Testes E2E

- 7 testes E2E escritos em `rbac-navigation.spec.ts`
- Cobertura de navegação por perfil para admin, logística, gestor e auditoria
- Validação de redirecionamento 401 e exibição 403

### Execução

Para executar os testes E2E:

```bash
cd apps/web
npx playwright test e2e/rbac-navigation.spec.ts
```

**Nota:** Os testes E2E requerem que o servidor esteja rodando em `http://localhost:3000`.

## Decisões Arquiteturais

### Por que testes E2E em vez de unitários?

- Testes E2E validam o fluxo completo de navegação por permissão
- Testam a integração real entre frontend, RBAC backend e tratamento de erros
- Validam o comportamento do hook `useApiErrorHandler` em ambiente real

### Por que usar AuthHelper e NavigationHelper existentes?

- Reutilização de helpers já testados e validados
- Consistência com testes E2E existentes
- Redução de código duplicado

### Por que não simular 401/403 com mock de API?

- Testes E2E devem validar o comportamento real
- Simulação de 401 via remoção de token do localStorage é suficiente
- Simulação de 403 via acesso a rota bloqueada é mais realista

## Arquivos Modificados

### Arquivos Modificados
- `apps/web/e2e/fixtures/users.ts` - Atualizado rotas das 18 páginas

### Arquivos Novos
- `apps/web/e2e/rbac-navigation.spec.ts` - Testes E2E de navegação por permissão
- `docs/BETA_020E.md` - Documentação técnica

## Limitações Conhecidas

1. **Dependência de servidor rodando:** Testes E2E requerem servidor em `localhost:3000`
2. **UI não implementada:** Algumas páginas podem não ter UI completamente implementada
3. **Seletores Playwright:** Seletores podem mudar com atualizações de UI

## Próximos Passos

1. **BETA-020F:** Remover `error-handler.ts` antigo após completa migração
2. **BETA-020G:** Implementar SSO/OAuth externo se necessário
3. **BETA-026:** Completar Épico 4 - Eficiência por Transportadora
4. **BETA-028:** Completar Épico 6 - Relatório Diário
5. **BETA-029:** Completar Épico 10 - Dashboard Beta

## Referências

- BETA-020D: Integração de Tratamento de Erros RBAC no Frontend
- BETA-020C: Frontend de Segurança e RBAC
- Documentação de RBAC: `docs/BETA_020C_SECURITY_RBAC_FRONTEND.md`
- Hook `useApiErrorHandler`: `apps/web/src/lib/useApiErrorHandler.ts`
- Componente AccessDenied: `apps/web/src/components/AccessDenied.tsx`
