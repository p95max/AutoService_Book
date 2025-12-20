FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       build-essential \
       libpq-dev \
       curl \
       ca-certificates \
       python3-dev \
       python3-venv \
       libffi-dev \
    && rm -rf /var/lib/apt/lists/*


COPY pyproject.toml poetry.lock README.md /app/

RUN pip install --upgrade pip \
    && pip install "poetry==1.4.2" setuptools wheel

RUN poetry install --no-interaction --no-ansi --no-root --with dev

COPY . /app

RUN python manage.py collectstatic --noinput || true

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV DJANGO_SETTINGS_MODULE=autoservice_book.settings
ENV PORT=8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "autoservice_book.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
