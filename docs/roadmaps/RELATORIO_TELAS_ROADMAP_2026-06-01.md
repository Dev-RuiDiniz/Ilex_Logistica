# Relatório de Telas (Roadmap W01–W18) - Estado Real

Data de referência: 2026-06-01  
Base: Roadmap Scrum + TDD (`Roadmap_Scrum_TDD_Ilex_Logistica.pdf`) + monorepo atual

## Resumo

- **Implementadas**: 5 telas
- **Parciais**: 2 telas
- **Pendentes**: 11 telas

## Matriz de telas

| Código | Tela do roadmap | Status | Evidência no monorepo |
|---|---|---|---|
| W01 | Login | Implementada | `apps/web/src/app/login/page.tsx` |
| W02 | Dashboard Logístico | Parcial | `apps/web/src/app/(private)/page.tsx` (dashboard base, sem KPIs completos) |
| W03 | Transportadoras | Implementada | `apps/web/src/app/(private)/carriers/page.tsx` |
| W04 | Importação de Entregas | Implementada | `apps/web/src/app/(private)/shipments/import/page.tsx` |
| W05 | Validação da Importação | Implementada | mesma tela W04 com pré-validação/erros por linha |
| W06 | Entregas Monitoradas | Implementada | `apps/web/src/app/(private)/shipments/page.tsx` |
| W07 | Detalhe da Entrega | Pendente | não há rota/tela dedicada de detalhe por shipment |
| W08 | Painel de Exceções | Pendente | não há rota/tela dedicada de fila de exceções |
| W09 | Regras de Prazo | Pendente | não há rota/tela de parametrização SLA por carrier/região |
| W10 | Relatório Diário | Pendente | não há rota/tela de relatório diário |
| W11 | Tratativas | Pendente | não há rota/tela de registro de tratativas |
| W12 | Logs de Coleta | Pendente | não há tela web dedicada de logs de coleta |
| W13 | Alertas | Pendente | não há tela de configuração/acompanhamento de alertas |
| W14 | Relatórios | Pendente | não há tela de exportações/relatórios gerenciais |
| W15 | Usuários e Permissões | Parcial | RBAC existe no backend; falta tela administrativa dedicada |
| W16 | Configurações | Pendente | não há tela de parâmetros gerais |
| W17 | Integrações | Pendente | não há tela de credenciais/status de integrações |
| W18 | Auditoria | Pendente | não há tela de trilha de auditoria |

## Observações importantes

1. A navegação atual no `AppShell` expõe apenas: `Dashboard`, `Transportadoras`, `Envios` e `Importar Envios` (`apps/web/src/components/app-shell.tsx`).
2. O módulo de envios já possui filtros e ordenação avançados, mas ainda sem visão explícita de “painel de exceções”.
3. O dashboard privado atual é apenas fundacional, sem KPIs operacionais completos esperados para W02 final.
4. Existe base de permissões por perfil (`admin`, `logistica`, `gestor`, `auditoria`) no backend e frontend, porém sem UI de gestão de usuários/perfis (W15).

## Próxima sequência recomendada de telas

1. **W08 Painel de Exceções** (prioridade alta, desbloqueia fluxo operacional crítico).
2. **W07 Detalhe da Entrega** (necessário para investigação e tratativas).
3. **W11 Tratativas** (registro de ação sobre exceções).
4. **W10 Relatório Diário** (visão executiva e rotina operacional).
5. **W15 Usuários e Permissões** (fechamento de governança funcional).

## Cobertura real por sprint (visão de produto web)

- **Sprint 1/2 (fundação + core)**: majoritariamente cobertas no Web.
- **Sprint 3/4 (exceções, relatório, alertas, auditoria e integrações)**: ainda em aberto no frontend.
