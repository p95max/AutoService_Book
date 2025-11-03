# Dockerfile
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.6.1 \
    POETRY_HOME="/opt/poetry" \
    PATH="$POETRY_HOME/bin:$PATH" \
    PYTHONPATH="/app"

WORKDIR /app

# системные зависимости для сборки cffi/psycopg и netcat
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential gcc curl ca-certificates libpq-dev pkg-config libffi-dev libssl-dev netcat-openbsd \
  && rm -rf /var/lib/apt/lists/*

# poetry нужен только для экспорта зависимостей
RUN pip install "poetry==${POETRY_VERSION}"

# сначала метафайлы (кеширование слоёв)
COPY pyproject.toml poetry.lock* /app/

# копируем весь проект (нужно чтобы в образе был пакет приложения)
COPY . /app

# экспорт зависимостей и установка через pip в системный Python (гарантированно доступно)
RUN poetry config virtualenvs.create false \
 && poetry export -f requirements.txt --without-hashes --output requirements.txt --only main || poetry export -f requirements.txt --without-hashes --output requirements.txt \
 && pip install --no-cache-dir -r requirements.txt

# убедимся в правах entrypoint
COPY ./deploy/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]
