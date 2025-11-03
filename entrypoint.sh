#!/bin/sh
set -e

echo "Waiting for database..."

if [ -n "$DATABASE_URL" ]; then
  python - <<'PY'
import os, time, socket
from urllib.parse import urlparse
d = os.environ.get('DATABASE_URL')
u = urlparse(d)
host = u.hostname or os.environ.get('RENDER_DB_HOST','db')
port = int(u.port or 5432)
for i in range(60):
    try:
        s = socket.create_connection((host, port), timeout=2)
        s.close()
        print("DB reachable")
        raise SystemExit(0)
    except Exception:
        time.sleep(1)
print("DB not reachable")
raise SystemExit(1)
PY
fi

echo "Apply database migrations"
python manage.py migrate --noinput

echo "Collect static files"
python manage.py collectstatic --noinput

if [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_EMAIL" ] && [ -n "$ADMIN_PASSWORD" ]; then
  python - <<PY
from django.contrib.auth import get_user_model
User = get_user_model()
u = "${ADMIN_USERNAME}"
e = "${ADMIN_EMAIL}"
p = "${ADMIN_PASSWORD}"
if not User.objects.filter(username=u).exists():
    User.objects.create_superuser(u, e, p)
    print("Superuser created:", u)
else:
    print("Superuser already exists:", u)
PY
fi

exec "$@"
