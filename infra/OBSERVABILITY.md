# Observabilidade local - Ilex Logística

## Objetivo

Registrar comandos mínimos para verificar saúde da API, saúde do PostgreSQL e logs da stack local.

## Subir stack

```bash
docker compose up --build
```

## Verificar estado dos serviços

```bash
docker compose ps
```

Estados esperados:

| Estado | Interpretação |
|---|---|
| `healthy` | O healthcheck do serviço passou. |
| `starting` | O serviço ainda está dentro do período inicial ou aguardando dependências. |
| `unhealthy` | O healthcheck falhou após as tentativas configuradas. |

## Logs em comando único

```bash
docker compose logs --tail=100 api db
```

Logs por serviço:

```bash
docker compose logs --tail=100 api
docker compose logs --tail=100 db
```

## Healthcheck da API

O container da API valida o endpoint local:

```bash
curl http://127.0.0.1:8000/health
```

Resultado esperado:

```json
{"status":"ok"}
```

## Healthcheck do DB

O container do PostgreSQL usa `pg_isready` com banco e usuário locais:

```bash
docker compose exec db pg_isready -U ilex -d ilex
```

Resultado esperado:

```text
/var/run/postgresql:5432 - accepting connections
```

## Simular falha do DB

Pare apenas o banco:

```bash
docker compose stop db
```

Verifique o estado:

```bash
docker compose ps
```

Consulte logs da API e do DB:

```bash
docker compose logs --tail=100 api db
```

Causa primária esperada:

- DB parado ou indisponível.
- API pode registrar erro de conexão, falha de migration ou dependência indisponível.
- `docker compose ps` deve refletir o serviço `db` como parado ou não saudável conforme o momento da verificação.

Para restaurar:

```bash
docker compose up -d db
docker compose up -d api
```

## Simular falha de healthcheck do DB

Altere temporariamente `POSTGRES_USER` ou `POSTGRES_DB` no `.env` para valor inválido e recrie a stack:

```bash
docker compose down
docker compose up --build
```

Verifique:

```bash
docker compose ps
docker compose logs --tail=100 db
```

Resultado esperado:

- O healthcheck do DB falha após `retries` configurado.
- O estado passa para `unhealthy`.
- Os logs e o healthcheck indicam falha de autenticação, banco inexistente ou serviço indisponível.

Reverta o `.env` para os valores válidos e recrie a stack.

## Configuração dos healthchecks

| Serviço | Comando | Intervalo | Timeout | Tentativas | Start period |
|---|---|---:|---:|---:|---:|
| `db` | `pg_isready` | `10s` | `5s` | `5` | `10s` |
| `api` | HTTP `/health` | `10s` | `5s` | `5` | `20s` |

## Logging

Os serviços usam driver `json-file` com rotação local:

| Opção | Valor |
|---|---|
| `max-size` | `10m` |
| `max-file` | `3` |

## Produção

- `/api/v1/health/live` informa vida do processo.
- `/api/v1/health/ready` verifica PostgreSQL e Redis e retorna `503` quando não está pronto.
- `/metrics` existe somente na API/rede interna; Caddy não publica essa rota.
- Logs são JSON e correlacionam request ID, método, template de rota, status e latência, sem token ou conteúdo de arquivo.
- Prometheus, exporters e regras ficam em `docker-compose.prod.yml`, `prometheus.yml` e `prometheus-rules.yml`.
- Procedimentos de incidente ficam em `RUNBOOKS.md`.

O roteamento externo deve encaminhar `/api/*` e `/health*`, nunca `/metrics`. O acesso ao Prometheus ocorre por túnel/VPN administrativo, sem porta pública no Compose.
