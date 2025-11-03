#!/bin/sh
set -e

# default env names
DB_HOST="${DB_HOST:-db}"
DB_PORT="${DB_PORT:-5432}"

# Wait for DB to be available (uses nc)
echo "Waiting for database ${DB_HOST}:${DB_PORT}..."
counter=0
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  counter=$((counter+1))
  if [ $counter -gt 120 ]; then
    echo "Timeout waiting for ${DB_HOST}:${DB_PORT}"
    exit 1
  fi
  sleep 1
done
echo "Database is up."

# Run migrations, collectstatic
python manage.py migrate --no-input
python manage.py collectstatic --no-input --clear

# Create admin if variables present (non-interactive)
if [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_EMAIL" ] && [ -n "$ADMIN_PASSWORD" ]; then
  python - <<PY
from django.contrib.auth import get_user_model
User = get_user_model()
username="${ADMIN_USERNAME}"
email="${ADMIN_EMAIL}"
pw="${ADMIN_PASSWORD}"
if not User.objects.filter(username=username).exists():
    print("Creating admin user", username)
    User.objects.create_superuser(username=username, email=email, password=pw)
else:
    print("Admin exists")
PY
fi

# Exec main process
exec "$@"
