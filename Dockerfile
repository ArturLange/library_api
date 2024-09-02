FROM python:3-alpine AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
    
FROM base AS builder

RUN pip install poetry==1.8.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-dev \
    python3-dev

RUN mkdir /install && \
    pip3 install --prefix=/install \
    psycopg2 \
    python-dotenv 

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

# The runtime image, used to just run the code provided its virtual environment
FROM base

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apk add --no-cache libpq

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY lib_api ./lib_api

CMD fastapi run lib_api/main.py --port 8000