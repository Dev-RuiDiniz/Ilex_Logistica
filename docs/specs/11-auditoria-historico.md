# SPEC-11 — Auditoria e Histórico Operacional

**Estado:** Confirmado

## Objetivo e contexto

Registrar eventos relevantes para investigação, conformidade e rastreabilidade sem expor dados sensíveis. Atores: auditoria e administradores autorizados; serviços internos produzem eventos.

## Estado atual e evidências

Há model, service, schemas e rotas de criar/listar/resumir/consultar logs, migration e página/testes Web. Imports, tratativas, alertas e relatórios também mantêm históricos próprios.

## Entradas, saídas e fluxo

Serviço recebe evento estruturado com ator, ação, recurso, resultado e metadados permitidos. Persiste registro imutável e disponibiliza consulta filtrada/paginada e resumo.

## Regras, dados e permissões

- Ator autenticado deriva da sessão sempre que possível.
- Eventos possuem timestamp, ação e alvo suficientes para correlação.
- Metadados passam por sanitização; senhas, tokens, secrets e conteúdo integral de arquivos são proibidos.
- Logs são append-only pela interface pública.
- Leitura exige permissão de auditoria; criação direta por usuário é restrita conforme endpoint vigente.

## Falhas esperadas

Evento inválido, metadado não serializável, consulta inválida ou falta de permissão retornam erro explícito. Falha de auditoria em ação crítica deve ser observável e seguir política transacional definida pelo serviço.

## Critérios de aceite

- Ações críticas previstas geram evento rastreável.
- Filtros e resumo reconciliam com a listagem.
- Nenhum padrão de segredo aparece em payloads ou documentação.
- Registros não são alterados por operações comuns.

## Cenários TDD

Criação por serviço, sanitização, filtros, paginação, resumo, `404`, `401/403` e tentativa de metadado sensível.

## Riscos, dependências e rastreabilidade

Retenção operacional inicial é de cinco anos. A API permanece append-only; descarte futuro exigirá rotina administrativa auditada e autorização específica. Evidência: configuração, `modules/audit`, migration e página de auditoria.
