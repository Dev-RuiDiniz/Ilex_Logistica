#!/usr/bin/env sh
set -eu

COMPOSE_FILE=${COMPOSE_FILE:-infra/docker-compose.prod.yml}
BACKUP_DIR=${BACKUP_DIR:-./backups}
RETENTION_DAYS=${RETENTION_DAYS:-30}
BACKUP_METRICS_FILE=${BACKUP_METRICS_FILE:-./monitoring/backup.prom}
STAMP=$(date -u +%Y%m%dT%H%M%SZ)
TARGET="${BACKUP_DIR}/ilex_${STAMP}.dump.gz"

mkdir -p "$BACKUP_DIR"
docker compose -f "$COMPOSE_FILE" exec -T db \
  pg_dump --format=custom --no-owner --no-acl -U "$POSTGRES_USER" "$POSTGRES_DB" | gzip -9 > "$TARGET"
test -s "$TARGET"
sha256sum "$TARGET" > "${TARGET}.sha256"
mkdir -p "$(dirname "$BACKUP_METRICS_FILE")"
printf 'ilex_backup_last_success_timestamp_seconds %s\n' "$(date +%s)" > "$BACKUP_METRICS_FILE"
find "$BACKUP_DIR" -type f -name 'ilex_*.dump.gz*' -mtime "+${RETENTION_DAYS}" -delete
printf '%s\n' "$TARGET"
