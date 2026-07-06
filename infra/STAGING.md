# Homologação semelhante à produção

## Pré-requisitos

- VPS Linux com Docker/Compose, DNS e portas 80/443.
- `.env` criado de `env/vps.env.example` com secrets reais fora do Git.
- Imagens imutáveis de API/Web e ao menos uma transportadora ativa sanitizada.
- Usuário E2E descartável com perfil administrador/logística.

## Sequência

1. Validar `docker compose -f infra/docker-compose.prod.yml config`.
2. Executar `infra/scripts/deploy_vps.sh <tag>` e confirmar readiness/TLS.
3. Executar smoke somente leitura com `scripts/smoke_production.py`.
4. Autorizar dados descartáveis e executar apenas `production-authenticated.spec.ts` nos quatro projetos.
5. Executar `scripts/performance_gate.py`, backup/restore e rollback para a imagem anterior.
6. Anexar evidências sanitizadas à UAT sem tokens, dumps ou dados pessoais.

```sh
ILEX_SMOKE_BASE_URL=https://app.exemplo.com.br \
ILEX_SMOKE_TOKEN="$TOKEN_DESCARTAVEL" \
python scripts/smoke_production.py

ILEX_E2E_BASE_URL=https://app.exemplo.com.br \
ILEX_E2E_ALLOW_WRITES=true \
ILEX_E2E_EMAIL="$E2E_EMAIL" \
ILEX_E2E_PASSWORD="$E2E_PASSWORD" \
npx playwright test e2e/production-authenticated.spec.ts
```

O teste autenticado altera dados e nunca deve ser apontado para produção sem janela/autorização. Ausência de VPS, DNS, TLS ou credenciais mantém esta etapa pendente.
