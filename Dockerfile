FROM python:3.12.3-slim

# Установка системных зависимостей для psycopg и сборки пакетов
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Установка poetry
RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/
COPY . /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Собираем статику (и можно миграции, если хочешь)
RUN python manage.py collectstatic --noinput

# (опционально) Миграции:
 RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "auto_service_book.wsgi:application", "--bind", "0.0.0.0:8000"]