FROM python:3.8-slim-buster

WORKDIR /bookmarks/

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN apt-get update \
    && apt-get install --no-install-recommends curl -qy wait-for-it \
    && rm -rf /var/lib/apt/list/*

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . .