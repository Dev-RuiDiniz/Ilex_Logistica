# Runbooks operacionais

## API indisponível

Confirmar `IlexApiUnavailable`, consultar logs por request ID, verificar readiness e containers. Reiniciar apenas após identificar dependência; se a nova imagem falhou, executar rollback para a tag anterior.

## PostgreSQL indisponível

Validar `pg_isready`, espaço/volume e logs sem imprimir credenciais. Suspender deploy/imports, recuperar o serviço e confirmar `/api/v1/health/ready`. Restore exige backup validado e janela aprovada.

## Redis indisponível

A API produtiva falha de forma segura em rotas limitadas. Verificar volume/memória e `redis-cli ping`; restaurar Redis e confirmar readiness antes de liberar tráfego.

## Migration falhou

Não repetir cegamente. Registrar revisão atual/head, erro e backup. Se a migration for declarada reversível, usar `rollback_vps.sh` com `REVERSIBLE_DOWNGRADE=true` e revisão explícita; caso contrário, corrigir forward.

## Import travado

Localizar `ImportHistory` e request ID, verificar tamanho/contadores e transação. Não editar contadores manualmente. Reprocessar apenas por preview/confirm idempotente após remover a causa.

## Backup falhou

Validar espaço, acesso ao container e checksum. Corrigir e repetir; o alerta só encerra quando o timestamp do textfile collector for atualizado por backup bem-sucedido. Escalar após duas tentativas ou antes da janela de deploy.

## Rollback

Confirmar tag anterior, compatibilidade de schema e backup recente. Executar o script, observar readiness/smoke e registrar decisão. Downgrade só é permitido quando a migration foi marcada e testada como reversível.
