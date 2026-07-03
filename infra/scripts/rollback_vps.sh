#!/usr/bin/env sh
set -eu

COMPOSE_FILE=${COMPOSE_FILE:-infra/docker-compose.prod.yml}
PREVIOUS_TAG=${1:?informe a tag anterior}
export ILEX_API_IMAGE="${ILEX_API_REPOSITORY:?}:$PREVIOUS_TAG"
export ILEX_WEB_IMAGE="${ILEX_WEB_REPOSITORY:?}:$PREVIOUS_TAG"

infra/scripts/backup_postgres.sh
if [ "${REVERSIBLE_DOWNGRADE:-false}" = "true" ]; then
  test -n "${DOWN_REVISION:-}" || { echo "DOWN_REVISION obrigatoria" >&2; exit 2; }
  docker compose -f "$COMPOSE_FILE" run --rm --entrypoint alembic api downgrade "$DOWN_REVISION"
fi
docker compose -f "$COMPOSE_FILE" pull api web
docker compose -f "$COMPOSE_FILE" up -d --remove-orphans
curl --fail --retry 12 --retry-delay 5 "https://${ILEX_DOMAIN:?}/api/v1/health/ready"
echo "rollback concluido: $PREVIOUS_TAG"
