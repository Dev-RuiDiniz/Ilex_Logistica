#!/usr/bin/env sh
set -e

until nc -z db 5432; do
  echo "waiting for postgres"
  sleep 1
done

alembic upgrade head

exec uvicorn app.main:app --host 0.0.0.0 --port 8000
