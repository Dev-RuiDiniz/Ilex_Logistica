# Infra

Camada de infraestrutura do Ilex Logística para garantir ambientes consistentes, deploy seguro e operação monitorável.

## Objetivo no MVP

Padronizar execução local/homologação, CI/CD e configurações de ambiente para API, Web e serviços de suporte.

## Responsabilidades do repositório

- Dockerfiles e orquestração de serviços
- Configuração de Nginx/reverse proxy
- Pipelines de CI/CD no GitHub Actions
- Gestão de variáveis e segredos por ambiente
- Estratégia de deploy e rollback
- Base de observabilidade e saúde do sistema

## Stack prevista

- Docker
- Nginx
- GitHub Actions
- VPS/AWS/Render/Railway (conforme ambiente)

## Estrutura sugerida

```text
docker/
nginx/
.github/workflows/
envs/
scripts/
```

## Backlog prioritário (LOG-*)

- LOG-001: Criar arquitetura inicial dos repositórios
- LOG-025: Testes integrados e QA (suporte de ambiente)
- LOG-026: Documentação final e guia operacional de deploy

## Critérios de aceite iniciais

- Ambiente local sobe com dependências principais
- Pipeline valida build e testes básicos
- Deploy de homologação documentado e repetível

## Convenção de commits

`<tipo>(infra): <ID> <resumo em pt-BR>`

Exemplo: `docs(infra): LOG-001 descreve padrao inicial de ambiente`
