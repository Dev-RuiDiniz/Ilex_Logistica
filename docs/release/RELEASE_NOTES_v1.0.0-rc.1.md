# Release notes — v1.0.0-rc.1 (candidata, não publicada)

## Destaques

- Monitoramento de entregas, SLA, exceções, tratativas, alertas, relatórios e auditoria.
- KPIs/ranking com filtros reconciliados e datasets controlados.
- Pedidos ERP CSV/XLSX com preview/confirm idempotente.
- Rodadas de cotação Web/CSV, recomendação determinística, override justificado e histórico.
- RBAC para administrador, logística, gestor e auditoria.
- Hardening produtivo, rate limiting Redis, observabilidade, continuidade e scripts de deploy/rollback.

## Incompatibilidades e operação

- Aplicar migrations até `20260703_03` antes da RC.
- Produção exige PostgreSQL, Redis, JWT forte, CORS HTTPS e domínio configurado.
- Imagens, tag e GitHub Release ainda não foram publicados.

## Pendências bloqueadoras

- PostgreSQL/backup/restore/deploy/rollback reais.
- Carga de 50 usuários em VPS.
- E2E autenticado externo e suíte histórica completa.
- UAT assinada por quatro perfis e homologação de regras operacionais.
- Decisão formal de go-live.

## Riscos conhecidos

- Tokens Web permanecem no armazenamento da sessão do navegador; migração HttpOnly/BFF é defesa futura recomendada.
- Dois avisos moderados Next/PostCSS permanecem sem atualização compatível indicada pelo npm.
- SLA, feriados, canais externos e amostras de layouts dependem de aceite humano.
