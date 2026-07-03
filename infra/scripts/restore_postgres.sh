#!/usr/bin/env sh
set -eu

test "$#" -eq 1 || { echo "uso: restore_postgres.sh backup.dump.gz" >&2; exit 2; }
BACKUP=$1
COMPOSE_FILE=${COMPOSE_FILE:-infra/docker-compose.prod.yml}
RESTORE_DB="ilex_restore_$(date -u +%Y%m%d%H%M%S)"

test -f "$BACKUP" && test -f "${BACKUP}.sha256"
(cd "$(dirname "$BACKUP")" && sha256sum -c "$(basename "$BACKUP").sha256")
cleanup() {
  docker compose -f "$COMPOSE_FILE" exec -T db dropdb --if-exists -U "$POSTGRES_USER" "$RESTORE_DB" >/dev/null 2>&1 || true
}
trap cleanup EXIT
docker compose -f "$COMPOSE_FILE" exec -T db createdb -U "$POSTGRES_USER" "$RESTORE_DB"
gzip -dc "$BACKUP" | docker compose -f "$COMPOSE_FILE" exec -T db \
  pg_restore --exit-on-error --no-owner --no-acl -U "$POSTGRES_USER" -d "$RESTORE_DB"
docker compose -f "$COMPOSE_FILE" exec -T db psql -U "$POSTGRES_USER" -d "$RESTORE_DB" \
  -v ON_ERROR_STOP=1 -c "SELECT count(*) FROM alembic_version;" >/dev/null
echo "restore validado em banco temporario: $RESTORE_DB"
