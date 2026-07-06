# Checklist de implantação

## Antes

- [ ] Tag/commit aprovado e imagens imutáveis publicadas.
- [ ] UAT assinada; riscos críticos/altos resolvidos ou aceitos.
- [ ] `.env` produtivo validado fora do Git; DNS/TLS prontos.
- [ ] Backup recente com checksum e restore mensal aprovado.
- [ ] Compatibilidade/downgrade das migrations revisada.
- [ ] Suporte, comunicação e janela de retorno confirmados.

## Durante

- [ ] Executar `deploy_vps.sh <tag>` e registrar horários/responsável.
- [ ] Confirmar migration head, liveness/readiness e exporters.
- [ ] Executar smoke read-only e E2E autorizado.
- [ ] Validar login, pedidos/cotações, envios, relatório e auditoria.

## Depois

- [ ] Monitorar 5xx, p95, rate limits, backlog, imports e backup.
- [ ] Registrar evidências sanitizadas e incidentes.
- [ ] Em falha, aplicar `RUNBOOKS.md` e `rollback_vps.sh`.
- [ ] Atualizar decisão GO/NO-GO e relatório.
