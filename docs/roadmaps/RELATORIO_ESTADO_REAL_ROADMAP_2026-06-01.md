# Relatório de Estado Real do Projeto vs Roadmap Scrum + TDD

Data de referência: 2026-06-01  
Base do roadmap: `Roadmap_Scrum_TDD_Ilex_Logistica.pdf`  
Base verificada: monorepo `Dev-RuiDiniz/Ilex_Logistica` (estado local pós-migração)

## Resumo executivo

- **Concluídas**: 12 tarefas
- **Parciais**: 7 tarefas
- **Pendentes**: 7 tarefas

O projeto está sólido até o núcleo de fundação e boa parte do core logístico (Sprints 1 e 2), com lacunas relevantes nas entregas de exceções, relatório diário, integrações, auditoria e QA/deploy final (Sprints 3 e 4).

## Evidências estruturais relevantes

- API com autenticação, RBAC, carriers, importação e listagem de shipments: `apps/api/app/modules/*` e `apps/api/tests/*`
- Web com login, área privada, carriers, listagem e importação de shipments: `apps/web/src/app/(private)/*`
- Infra base e documentação operacional: `infra/docker-compose.yml`, `infra/README.md`, `infra/OBSERVABILITY.md`
- Integrações ainda sem implementação técnica (apenas docs): `integrations/README.md`, `integrations/C09_QA_MINIMO_EVIDENCIA.md`
- Ponto crítico pós-monorepo: workflows estão em `apps/api/.github/workflows` e `apps/web/.github/workflows`, não em `.github/workflows` do repositório raiz.

## Status por tarefa do roadmap (LOG-001..LOG-026)

| ID | Status | Leitura do estado real |
|---|---|---|
| LOG-001 | Concluída | Arquitetura consolidada no monorepo com domínios separados (`apps/api`, `apps/web`, `infra`, `docs`, `integrations`, `.github`). |
| LOG-002 | Concluída | Banco e migrations implementados (`apps/api/migrations`, Alembic, testes de migration). |
| LOG-003 | Concluída | JWT funcional (`apps/api/app/modules/auth/*`, `tests/test_auth.py`). |
| LOG-004 | Concluída | Perfis de acesso implementados (`admin/logistica/gestor/auditoria`) com RBAC e testes. |
| LOG-005 | Concluída | CRUD de transportadoras implementado com cobertura de teste. |
| LOG-006 | Parcial | Há logs e tratamento de erro base; não há trilha robusta de observabilidade funcional fim-a-fim na API. |
| LOG-007 | Concluída | Importador CSV implementado com fluxo web+api e testes amplos. |
| LOG-008 | Concluída | Validação de colunas obrigatórias implementada e testada. |
| LOG-009 | Concluída | Prévia de importação existe no fluxo upload/validação antes da confirmação. |
| LOG-010 | Parcial | Persistência de shipments está pronta; persistência clara de “eventos” logísticos ainda não está explícita como módulo dedicado. |
| LOG-011 | Concluída | Listagem de entregas com paginação/filtros implementada. |
| LOG-012 | Pendente | Não há endpoint/tela clara de detalhe completo por entrega (`W07`) no estado atual. |
| LOG-013 | Parcial | Regras SLA estão implícitas no cálculo atual; falta módulo configurável de regras por transportadora/região. |
| LOG-014 | Concluída | Cálculo automático de atraso implementado em serviço de shipments. |
| LOG-015 | Concluída | Classificação de criticidade implementada. |
| LOG-016 | Pendente | Painel de exceções dedicado ainda não existe como feature/tela específica. |
| LOG-017 | Pendente | Registro de tratativas operacionais não identificado no modelo/rotas/telas. |
| LOG-018 | Pendente | Relatório diário operacional não identificado (geração/consulta no produto). |
| LOG-019 | Pendente | Envio por e-mail do relatório não implementado. |
| LOG-020 | Pendente | Logs avançados de coleta (API+integrations) não implementados como trilha técnica. |
| LOG-021 | Pendente | Conectores de API de transportadoras não implementados (sem código de worker/client). |
| LOG-022 | Pendente | Bots/scraping controlado não implementados. |
| LOG-023 | Parcial | Existe dashboard/listas base no Web, mas não “dashboard logístico final” consolidado. |
| LOG-024 | Pendente | Auditoria de alterações (trilha de change log por usuário/ação) não identificada. |
| LOG-025 | Parcial | Há testes de API/Web e QA documental; faltam testes integrados fim-a-fim e validação unificada no monorepo. |
| LOG-026 | Parcial | Documentação foi fortalecida, mas ainda falta manual final de uso orientado ao usuário operacional/gestor por fluxo completo. |

## Em qual tarefa continuar agora

### Próxima tarefa recomendada: **LOG-016 (Criar painel de exceções)**

Motivo:
1. Depende diretamente do que já existe (delay + criticality + listagem).
2. Destrava LOG-017, LOG-018 e LOG-023.
3. Entrega valor operacional imediato para o time de logística.

## Sequência recomendada de execução (curto prazo)

1. **LOG-016** Painel de exceções (API filtro dedicado + tela web de fila priorizada).
2. **LOG-017** Registro de tratativas (modelo, endpoints e UI de ação/comentário/status).
3. **LOG-018** Relatório diário (geração no backend + tela/endpoint de consulta).
4. **LOG-019** Envio por e-mail do relatório diário.
5. **LOG-021/022** Base de integrações (conector API + estrutura para bot controlado).
6. **LOG-024** Auditoria de alterações.
7. **LOG-025/026** QA integrado final + manual de uso final.

## Alertas críticos para o monorepo (antes de avançar muito)

1. Ajustar CI para monorepo: workflows hoje estão em subpastas de app e com caminhos que não refletem execução a partir da raiz.
2. Corrigir estrutura de `.github` importada (há aninhamento `.github/.github`), para garantir convenções GitHub no repositório raiz.
3. Endereçar regressão atual de teste na API (caso de autenticação retornando `403` onde o teste espera `401`) para manter baseline de qualidade.
