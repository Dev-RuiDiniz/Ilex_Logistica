# ESCOPO.md — Escopo Completo do Ilex Logística

**Versão:** 2.0
**Atualizado em:** 2026-07-03
**Status:** MVP avançado em estabilização e homologação
**Fonte complementar:** `ESCOPO_PROJETO_ILEX_LOGISTICA_APENDICE_1.md`

## 1. Sumário executivo

O Ilex Logística é uma plataforma web operacional que centraliza entregas de múltiplas transportadoras, importa dados logísticos, calcula SLA e criticidade, evidencia exceções, registra tratativas, produz alertas e relatórios e controla acesso por perfil. A evolução prevista amplia o monitoramento pós-expedição com comparação de cotações antes da expedição.

O sistema atende administração, equipe de logística, gestão logística e auditoria/backoffice. Código, migrations e testes são a evidência do estado implementado; requisitos sem evidência são classificados como parciais, planejados ou a confirmar.

## 2. Objetivos e resultados esperados

- Reduzir consultas manuais e consolidar o acompanhamento de entregas.
- Detectar atrasos, extravios, falta de atualização e criticidade operacional.
- Priorizar tratativas com indicadores e relatórios auditáveis.
- Comparar desempenho, volume e custo por transportadora.
- Preservar histórico de importação, alterações e eventos relevantes.
- Evoluir para cotação de frete por pedido com entrada assistida do ERP.

## 3. Perfis e responsabilidades

| Perfil | Responsabilidade | Estado |
|---|---|---|
| Administrador | usuários, transportadoras, regras, parâmetros e auditoria | Confirmado por RBAC |
| Logística/Operador | importar, consultar entregas e registrar tratativas | Confirmado |
| Gestor | acompanhar KPIs, eficiência, exceções e relatórios | Confirmado |
| Auditoria/Viewer | consulta controlada de histórico e logs | Confirmado |

Permissões exatas são definidas pelo backend e devem ser verificadas em cada endpoint; nomes históricos de papéis não substituem a matriz implementada.

## 4. Escopo funcional

| Domínio | Capacidades | Estado |
|---|---|---|
| Autenticação e RBAC | login, refresh JWT, usuários, papéis, permissões e proteção de rotas | Confirmado |
| Transportadoras | cadastro, edição, listagem e inativação | Confirmado |
| Importações | CSV/XLSX, preview, validação, confirmação, duplicidades, histórico e Braspress | Confirmado |
| Entregas monitoradas | listagem, detalhe, filtros, campos fiscais/financeiros e promoção de delivery | Parcialmente homologado |
| SLA e criticidade | regras, recálculo, atraso e criticidade | Confirmado; regra operacional final a homologar |
| Tratativas e exceções | registro de ações e painel priorizado | Confirmado |
| Eficiência | agregação e comparação por transportadora | Confirmado; métricas complementares parciais |
| Dashboard | KPIs, resumo, filtros e tendência | Confirmado |
| Alertas | geração, leitura, resolução e logs de entrega | Confirmado |
| Relatórios | geração, consulta e exportação de relatório diário | Confirmado |
| Auditoria | eventos operacionais, consulta e resumo | Confirmado |
| Pedidos e cotações | importação de pedidos, comparação e melhor opção | Planejado |

As especificações normativas de cada domínio estão em `docs/specs/`.

## 5. Entregas monitoradas — Apêndice 1

### 5.1 Dados

Cada entrega deve suportar rastreio, cliente, destino, transportadora, status, datas previstas/realizadas, número e valor da nota fiscal, data de saída/coleta, valor do frete e percentual do frete.

```text
percentual_frete = (valor_frete / valor_nota_fiscal) * 100
```

O percentual fica indisponível se um valor estiver ausente ou se o valor da NF for menor ou igual a zero. Valores monetários não podem usar ponto flutuante binário na persistência.

### 5.2 Busca, filtros e apresentação

- Busca por NF, cliente, rastreio, UF e transportadora.
- Filtros combináveis por status, transportadora, cliente, UF, mês, ano e todo o período.
- Ordenação e paginação coerentes com o conjunto filtrado.
- KPIs e quadro de eficiência recalculados com os mesmos filtros.
- Estados vazios, carregamento e erro sem inventar dados.

## 6. Eficiência por transportadora

O sistema deve apresentar, por transportadora e período filtrado: total de NFs/entregas, quantidade e percentual no prazo, atrasadas e extraviadas, frete total e percentual médio de frete. Ranking pode considerar eficiência, custo e volume, desde que a fórmula e o desempate sejam explícitos. A definição de “no prazo” depende da regra de SLA homologada.

## 7. Cotação de frete por pedido

### 7.1 MVP assistido

- Importar pedidos do ERP por CSV/XLSX padronizado.
- Criar uma comparação por pedido e transportadoras habilitadas.
- Registrar valor ou status `pendente`, `cotado`, `indisponivel`, `erro` ou `vencido`.
- Destacar inicialmente o menor valor válido; desempates seguem ordem estável definida na spec.
- Preservar histórico auditável sem sobrescrever rodadas anteriores.

### 7.2 Evolução automática

Integrações por API com ERP e transportadoras só entram após contrato, credenciais seguras, ambiente de homologação, idempotência, limites de requisição e política de retry aprovados. Automação de portal/captcha não integra o MVP.

## 8. Requisitos não funcionais

- **Segurança:** JWT, RBAC, validação de entrada, secrets fora do repositório e auditoria de ações críticas.
- **Qualidade:** SDD antes do código; TDD RED/GREEN/REFACTOR; não reduzir cobertura sem justificativa.
- **Confiabilidade:** importações idempotentes, erros por linha e consistência transacional.
- **Desempenho:** paginação e filtros server-side; metas numéricas permanecem A CONFIRMAR.
- **Acessibilidade:** navegação e componentes Web devem manter semântica, teclado e feedback compreensível.
- **Observabilidade:** logs operacionais sem dados sensíveis; monitoramento externo A CONFIRMAR.
- **Compatibilidade:** PostgreSQL em produção/Docker e SQLite apenas onde suportado por testes/desenvolvimento.
- **Privacidade:** retenção, base legal e política de descarte A CONFIRMAR com o cliente.

## 9. Integrações e dados

| Integração | Estratégia | Estado |
|---|---|---|
| Braspress | relatório exportado e importação assistida | Confirmado por mapper/testes |
| Outras transportadoras | CSV/XLSX ou conector futuro | Parcial/A CONFIRMAR |
| ERP | importação assistida; API futura | Planejado |
| Notificações externas | logs de entrega presentes; canal real | PENDENTE DE VALIDAÇÃO |

Entidades confirmadas incluem usuários, papéis, permissões, transportadoras, históricos de importação, deliveries, shipments, tratativas, regras SLA, alertas, logs de entrega, relatórios e auditoria. `orders` e `freight_quotes` são planejadas e exigem migration própria.

## 10. Limites e fora de escopo

- Não armazenar credenciais em documentação, frontend ou arquivos importados.
- Não automatizar captcha ou contornar controles de portais.
- Pagamentos, faturamento, roteirização de frota e marketplace não estão contemplados.
- Não prometer APIs de terceiros sem documentação e homologação.
- Não usar dados sintéticos como evidência de produção.

## 11. Riscos e dependências

- Contrato e ambiente do ERP ainda não fornecidos.
- Nem toda transportadora possui API ou layout estável.
- Qualidade dos indicadores depende da qualidade de NF, datas, status e frete importados.
- Regra única de SLA, extravio e eficiência precisa de homologação operacional.
- Retenção de auditoria, relatórios e cotações permanece A CONFIRMAR.

## 12. Critérios globais de aceite

- Cada requisito possui spec, status e evidência ou marcação explícita de pendência.
- Filtros combinados produzem listagens e KPIs consistentes.
- Cálculos monetários tratam nulos e divisão por zero.
- Importações reportam erro por linha, duplicidade e resultado persistido.
- Rotas privadas distinguem autenticação ausente (`401`) de permissão insuficiente (`403`).
- Alterações críticas deixam trilha auditável.
- Novos schemas usam migration testada em upgrade/downgrade.
- Suítes afetadas, build, validação documental e secret scan passam antes da entrega.
- O projeto somente será considerado concluído quando os gates P0–P5 do `ROADMAP.md` e o UAT do MVP assistido estiverem aprovados.

## 13. Matriz do Apêndice 1

| IDs | Resultado | Estado atual | Spec |
|---|---|---|---|
| LOG-027–031 | campos fiscais e financeiros | API e Web confirmados; UAT complementar pendente | `04-entregas-monitoradas.md` |
| LOG-032–033 | filtros e busca | API, Web e E2E confirmados | `04-entregas-monitoradas.md` |
| LOG-034–035 | eficiência e indicadores por período | Implementação presente; aceite complementar parcial | `07-eficiencia-transportadoras.md` |
| LOG-036–040 | pedidos e cotação | Planejado | `12-pedidos-cotacao-frete.md` |
| LOG-041 | fluxo Braspress | Implementação/testes presentes; guia consolidado na spec | `03-importacoes-braspress.md` |

## 14. Fontes de verdade

- Apêndice: `ESCOPO_PROJETO_ILEX_LOGISTICA_APENDICE_1.md`.
- Índice SDD: `docs/specs/README.md`.
- Implementação: `apps/api/app/modules/`, `apps/web/src/` e migrations.
- Estado e prioridade: `CONTEXTO.md` e `ROADMAP.md`.
