#!/bin/sh
python manage.py collectstatic --noinput
exec gunicorn auto_service_book.wsgi:application --bind 0.0.0.0:8000