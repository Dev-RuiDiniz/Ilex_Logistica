# Continuidade, backup e rollback

## Política

- Backup PostgreSQL diário em formato custom comprimido, acompanhado de SHA-256.
- Retenção padrão de 30 dias; armazenamento externo/criptografado deve ser configurado no host.
- Restore em banco temporário todo mês e antes de mudanças destrutivas.
- Deploy sempre executa backup, migration, subida das imagens imutáveis e readiness.
- Downgrade de schema ocorre somente com `REVERSIBLE_DOWNGRADE=true` e `DOWN_REVISION` explicitamente revisada. Caso contrário, a imagem anterior precisa ser compatível com o schema já promovido.

## Comandos

```sh
set -a; . infra/.env; set +a
infra/scripts/backup_postgres.sh
infra/scripts/restore_postgres.sh backups/ilex_AAAAMMDDTHHMMSSZ.dump.gz
infra/scripts/deploy_vps.sh v1.0.0-rc.1
REVERSIBLE_DOWNGRADE=false infra/scripts/rollback_vps.sh v1.0.0-rc.0
```

O restore nunca sobrescreve diretamente o banco principal: cria um banco `ilex_restore_*`, valida o catálogo Alembic e remove o banco temporário ao sair. Promoção de dados restaurados exige janela aprovada e procedimento específico do incidente.

## Evidência obrigatória

Registrar data, host/classe de hardware, tag, tamanho/checksum, duração, resultado do restore, migration anterior/nova e responsável. Não anexar dumps, credenciais ou strings de conexão ao repositório.
