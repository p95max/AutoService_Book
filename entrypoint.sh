#!/usr/bin/env bash
set -e

# параметры
: "${DJANGO_SUPERUSER_USERNAME:=manager}"
: "${DJANGO_SUPERUSER_EMAIL:=maxpetrikin@gmail.com}"
: "${DJANGO_SUPERUSER_PASSWORD:=045155655}"
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "Waiting for database ${DB_HOST}:${DB_PORT}..."

# ждём пока nc появится и порт откроется
until nc -z ${DB_HOST} ${DB_PORT}; do
  echo "Waiting for database..."
  sleep 1
done

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collect static files..."
python manage.py collectstatic --noinput

# create admin if not exist
python - <<'PY'
import os
from django.contrib.auth import get_user_model
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get('DJANGO_SETTINGS_MODULE','autoservice_book.settings'))
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME','manager')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL','admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD','admin')
if not User.objects.filter(username=username).exists():
    print("Creating superuser:", username)
    User.objects.create_superuser(username=username, email=email, password=password)
else:
    print("Superuser already exists:", username)
PY

# finally run server (gunicorn recommended). Fallback to runserver if gunicorn absent.
if command -v gunicorn >/dev/null 2>&1; then
  echo "Starting Gunicorn..."
  exec gunicorn autoservice_book.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-tmp-dir /dev/shm
else
  echo "Gunicorn not found, starting Django dev server (not for production)"
  exec python manage.py runserver 0.0.0.0:8000
fi
