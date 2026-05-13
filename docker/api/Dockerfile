FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY Api/pyproject.toml ./
COPY Api/app ./app
COPY Api/migrations ./migrations
COPY Api/alembic.ini ./
COPY Infra/docker/api/api-entrypoint.sh /usr/local/bin/api-entrypoint.sh

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir -e .

RUN chmod +x /usr/local/bin/api-entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["api-entrypoint.sh"]
