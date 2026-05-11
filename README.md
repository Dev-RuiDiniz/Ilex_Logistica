# Api

Camada de backend do Ilex Logística responsável por autenticação, regras de prazo/SLA, processamento de entregas e geração de relatórios operacionais.

## Objetivo no MVP

Entregar a API central da operação logística, preparada para ingestão de dados (importação/API/bots), cálculo de atraso, classificação de criticidade e auditoria.

## Responsabilidades do repositório

- Autenticação e autorização por perfil
- CRUD de transportadoras e parâmetros
- Importação e validação de entregas (Excel/CSV)
- Persistência de entregas, eventos e histórico
- Cálculo de atraso, SLA e criticidade
- Painel de exceções (fonte de dados)
- Relatório diário e alertas
- Logs e auditoria operacional

## Stack prevista

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL
- Celery/RQ (jobs assíncronos)

## Estrutura sugerida

```text
app/
  modules/
    auth/
    users/
    carriers/
    shipments/
    imports/
    tracking/
    exceptions/
    reports/
    alerts/
    audit/
  core/
  database/
  jobs/
  main.py
migrations/
tests/
```

## Backlog prioritário (LOG-*)

- LOG-002: Configurar banco PostgreSQL e migrations
- LOG-003: Criar autenticação JWT
- LOG-004: Criar perfis de acesso
- LOG-007: Validar colunas obrigatórias
- LOG-009: Persistir entregas
- LOG-014: Criar regras de prazo/SLA
- LOG-015: Calcular atraso automaticamente
- LOG-016: Classificar criticidade
- LOG-019: Criar relatório diário
- LOG-024: Criar auditoria de alterações

## Critérios de aceite iniciais

- API sobe localmente com conexão ao banco
- Endpoints protegidos por perfil
- Importação válida persiste dados sem duplicidade indevida
- Regra de SLA impacta status de atraso e criticidade
- Logs/auditoria registram ações sensíveis

## Convenção de commits

`<tipo>(api): <ID> <resumo em pt-BR>`

Exemplo: `docs(api): LOG-001 define responsabilidade do repositorio`
