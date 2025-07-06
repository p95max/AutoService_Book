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

# Копируем entrypoint.sh и даём права на исполнение
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

CMD ["/app/entrypoint.sh"]