#!/bin/sh
set -e

echo "Waiting for database..."
if [ -n "$DATABASE_URL" ]; then
  python - <<'PY'
import os, time, socket
from urllib.parse import urlparse
u = urlparse(os.environ['DATABASE_URL'])
host, port = (u.hostname or 'db'), int(u.port or 5432)
for i in range(60):
    try:
        s = socket.create_connection((host, port), timeout=2); s.close()
        print("DB reachable"); raise SystemExit(0)
    except Exception:
        time.sleep(1)
print("DB not reachable"); raise SystemExit(1)
PY
fi

if [ "${AUTO_MAKEMIGRATIONS:-0}" = "1" ]; then
  echo "Auto make migrations (dev)"
  python manage.py makemigrations || true
fi

echo "Apply database migrations"
python manage.py migrate --noinput

echo "Load fixtures: brands (idempotent)"
: "${FIXTURE_BRANDS:=/app/service_book/fixtures/brands.json}"
if [ -f "$FIXTURE_BRANDS" ]; then
  python - <<'PY'
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "autoservice_book.settings"))
django.setup()

from django.db import connection
from django.core.management import call_command

fixture = os.environ.get("FIXTURE_BRANDS", "/app/service_book/fixtures/brands.json")

def brand_count():
    with connection.cursor() as c:
        c.execute("SELECT to_regclass('public.service_book_brand')")
        if not c.fetchone()[0]:
            return 0
        c.execute("SELECT COUNT(*) FROM service_book_brand")
        return c.fetchone()[0]

cnt = brand_count()
if cnt == 0:
    print(f"Loading fixtures from {fixture}")
    call_command("loaddata", fixture, verbosity=1)
else:
    print(f"Brands already present: {cnt}")
PY
else
  echo "Fixture file not found: $FIXTURE_BRANDS (skip)"
fi

if [ -n "$CHECK_TABLE" ]; then
  echo "Check table exists: $CHECK_TABLE"
  python - <<'PY' || true
import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("DJANGO_SETTINGS_MODULE", "autoservice_book.settings"))
django.setup()

from django.db import connection

tbl = os.environ.get("CHECK_TABLE")
with connection.cursor() as c:
    c.execute("SELECT to_regclass(%s)", (tbl,))
    print("Table:", tbl, "->", c.fetchone())
PY
fi

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Ensure superuser (idempotent)"
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  python manage.py createsuperuser --noinput || true
fi

exec "$@"
