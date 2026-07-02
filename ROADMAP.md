# ROADMAP.md — Evolução do Ilex Logística

**Atualizado em:** 2026-07-02
**Método:** SDD + TDD; status baseado em evidência do repositório

## 1. Legenda

- **Confirmado:** model/rota/tela e testes relevantes identificados.
- **Parcial:** existe implementação, mas o aceite completo requer lacunas ou homologação.
- **Planejado:** requisito sem implementação identificada.

## 2. Estado consolidado

| Épico | Status | Evidência principal |
|---|---|---|
| Fundação API/Web/DB | Confirmado | apps, migrations e infra |
| Imports CSV/XLSX e Braspress | Confirmado | módulo imports, mapper e testes |
| Shipments, SLA e tratativas | Confirmado | módulos shipments/sla e testes |
| Eficiência, exceções e dashboard | Confirmado | analytics/dashboard e telas |
| Alertas e relatórios | Confirmado | módulos e páginas correspondentes |
| Segurança, RBAC e auditoria | Confirmado | auth/users/audit e testes |
| Cotação por pedido | Planejado | ausência de domínio/rotas/telas |

## 3. Backlog do Apêndice 1

| ID | Entrega | Status | Próxima evidência/ação |
|---|---|---|---|
| LOG-027 | Campos fiscais/financeiros | Confirmado no backend; Web parcial a validar | homologar listagem/detalhe/exportação |
| LOG-028 | NF na tabela e filtro | Parcial | validar ordenação e busca ponta a ponta |
| LOG-029 | Data de saída/coleta | Parcial | validar importação, tela e relatórios |
| LOG-030 | Valor do frete | Parcial | validar listagem, detalhe e exportação |
| LOG-031 | Percentual do frete | Confirmado por código/testes | validar casos nulos e zero em UI |
| LOG-032 | Filtros expandidos | Parcial | cobrir combinações transportadora/cliente/UF/período |
| LOG-033 | Busca global logística | Parcial | confirmar todos os campos do apêndice |
| LOG-034 | Eficiência por transportadora | Confirmado | homologar dados reais |
| LOG-035 | Indicadores por período | Parcial | validar mês/ano/todo período em KPIs e quadro |
| LOG-036 | Subaba de cotação | Planejado | especificar UX e contrato |
| LOG-037 | Importador de pedidos ERP | Planejado | definir layout CSV/XLSX mínimo |
| LOG-038 | Contrato ERP | Planejado | obter documentação e ambiente |
| LOG-039 | Motor comparativo | Planejado | definir domínio, status e idempotência |
| LOG-040 | Ranking de melhor frete | Planejado | homologar regra e desempate |
| LOG-041 | Fluxo Braspress | Parcial/confirmado em testes | recriar guia vigente sem credenciais |

## 4. Fases propostas

### Fase A — Homologação do monitoramento (prioridade alta)

Especificar e testar os aceites LOG-027 a LOG-035 com dados controlados. Fechar lacunas de busca, filtros, campos financeiros e recálculo dos indicadores. Cada item segue RED, GREEN e REFACTOR, com teste API e Web; fluxo crítico recebe Playwright.

### Fase B — Contratos de cotação (prioridade alta)

Concluir LOG-038 e a especificação de LOG-036/037/039/040: layout do pedido, statuses de cotação, regra inicial de menor preço, auditoria, permissões e falhas. Produzir ADR para as novas entidades e integração assistida.

### Fase C — MVP assistido de cotação (prioridade média/alta)

Criar migrations, models, importação de pedidos, API comparativa e subaba Web. O MVP usa CSV/XLSX e não automatiza portais. Aceite: pedido importado, uma cotação por transportadora habilitada, melhor opção destacada e histórico consultável.

### Fase D — Integrações automáticas (dependente)

Somente após contratos e homologação: conectar ERP e APIs de transportadoras, com retries, idempotência, observabilidade e gestão segura de credenciais.

## 5. Definition of Done

- Especificação e aceite aprovados antes do código.
- Testes RED/GREEN registrados e suítes afetadas verdes.
- Migration reversível e validada quando houver schema.
- Autorização/RBAC e erros operacionais cobertos.
- Documentação raiz, contexto e relatório atualizados.
- Secret scan, build e validadores aplicáveis aprovados.

## 6. Especificações de execução

O catálogo normativo está em `docs/specs/README.md`. A Fase A usa principalmente SPEC-04, SPEC-07 e SPEC-08; as Fases B e C usam SPEC-12 e suas dependências. Nenhum item planejado muda para confirmado sem evidência no código, migration e testes aplicáveis.
