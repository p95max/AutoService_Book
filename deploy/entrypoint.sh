#!/usr/bin/env bash
set -e

DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "Waiting for database ${DB_HOST}:${DB_PORT}..."
# используем pg_isready (надёжнее, чем nc)
until pg_isready -h "$DB_HOST" -p "$DB_PORT" >/dev/null 2>&1; do
  sleep 1
done

echo "Database is available — running migrations"
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# запускаем команду контейнера (gunicorn/uvicorn) из CMD
exec "$@"
