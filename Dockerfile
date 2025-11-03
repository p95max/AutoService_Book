# Dockerfile
FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app

# system deps required to build some wheels (cffi, psycopg, cryptography)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    curl \
    netcat-openbsd \
    git \
 && rm -rf /var/lib/apt/lists/*

# install Poetry
RUN curl -sSL https://install.python-poetry.org | python - --version 1.8.2 \
 && poetry config virtualenvs.create false

# copy dependency manifests first (Poetry cache layer)
COPY pyproject.toml poetry.lock /app/

# install runtime deps only
RUN poetry install --no-interaction --no-ansi --only main

# copy project sources (after deps installed)
COPY . /app

# ensure entrypoint present and executable (we copy from project root)
RUN chmod +x /app/entrypoint.sh

# create non-root user (optional but good)
RUN useradd --create-home appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# default command — entrypoint will exec passed command
CMD ["/app/entrypoint.sh", "gunicorn", "autoservice_book.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]
