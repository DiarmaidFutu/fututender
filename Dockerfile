FROM python:3.12-bookworm AS build

ARG POETRY_VERSION=1.8.3
ARG ENVIRONMENT=development
# configure shell
ENV ENVIRONMENT=${ENVIRONMENT} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # Poetry's configuration:
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local'
RUN pip install poetry==${POETRY_VERSION}

WORKDIR /app
COPY poetry.lock pyproject.toml /app/

RUN poetry install $(test "${ENVIRONMENT}" == production && echo "--only=main") --no-interaction --no-ansi

WORKDIR /
COPY src /app
WORKDIR /app

CMD ["/wait-for-it", "db:5432", "--", "uvicorn", "mpchat.api.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
