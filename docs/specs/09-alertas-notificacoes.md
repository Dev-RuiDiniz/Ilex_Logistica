# SPEC-09 — Alertas e Notificações

**Estado:** Alertas confirmados; canais externos parcialmente validados

## Objetivo e contexto

Gerar e acompanhar alertas operacionais para eventos que exigem ação, preservando estado e tentativas de entrega. Atores: logística e gestão; administração configura o que estiver disponível.

## Estado atual e evidências

Models, schemas e rotas suportam listagem, resumo, geração, leitura, resolução e logs de entrega, incluindo ausência de atualização e falha de importação. Há página e testes Web/API.

## Entradas, saídas e fluxo

Eventos elegíveis entram no gerador, que evita duplicidade conforme regra vigente e persiste alertas. Usuário marca como lido/resolvido. Logs registram canal, estado e tentativa sem armazenar segredo.

## Regras, dados e permissões

- Um mesmo evento não gera alertas ilimitados sem mudança relevante.
- Lido não equivale a resolvido.
- Resolução preserva histórico e autoria quando disponível.
- Falha de canal não apaga alerta interno.
- Consulta e mutação obedecem RBAC.

## Falhas esperadas

Alvo inexistente, transição inválida, canal indisponível e erro de persistência produzem estado explícito e retry controlado; nenhum token entra no log.

## Critérios de aceite

- Geração cria apenas alertas elegíveis.
- Ler/resolver é idempotente conforme contrato.
- Resumo confere com listagem.
- Falha externa permanece rastreável e não perde o alerta.

## Cenários TDD

Geração normal, no-update, import-failure, duplicidade, leitura, resolução, delivery pendente/falha/sucesso e RBAC; Web cobre feedback e atualização da lista.

## Riscos, dependências e rastreabilidade

Canais reais, destinatários, cadência, retry e escalonamento estão A CONFIRMAR. Evidência: `modules/alerts`, migrations de alerts/delivery logs e páginas/testes.
