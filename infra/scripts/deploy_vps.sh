#!/usr/bin/env sh
set -eu

COMPOSE_FILE=${COMPOSE_FILE:-infra/docker-compose.prod.yml}
TARGET_TAG=${1:?informe a tag imutavel da release}
export ILEX_API_IMAGE="${ILEX_API_REPOSITORY:?}:$TARGET_TAG"
export ILEX_WEB_IMAGE="${ILEX_WEB_REPOSITORY:?}:$TARGET_TAG"

infra/scripts/backup_postgres.sh
docker compose -f "$COMPOSE_FILE" pull api web
docker compose -f "$COMPOSE_FILE" run --rm --entrypoint alembic api upgrade head
docker compose -f "$COMPOSE_FILE" up -d --remove-orphans
curl --fail --retry 12 --retry-delay 5 "https://${ILEX_DOMAIN:?}/api/v1/health/ready"
echo "deploy concluido: $TARGET_TAG"
