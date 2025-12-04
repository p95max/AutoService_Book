#!/bin/sh
set -e

echo "Waiting for database..."
# Неблокируемый wait: 60 попыток по 1с
if [ -n "$DATABASE_URL" ]; then
  python - <<'PY'
import os, time, socket
from urllib.parse import urlparse
u = urlparse(os.environ['DATABASE_URL'])
host, port = (u.hostname or 'db'), (u.port or 5432)
for i in range(60):
    try:
        s = socket.create_connection((host, port), timeout=2); s.close()
        print("DB reachable"); raise SystemExit(0)
    except Exception: time.sleep(1)
print("DB not reachable"); raise SystemExit(1)
PY
fi

echo "Apply database migrations"
python manage.py migrate --noinput

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Ensure superuser (idempotent)"
# Используем только стандартный механизм Django
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --noinput || true
fi

exec "$@"
