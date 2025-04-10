FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /api

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

RUN apt-get update && apt-get install -y supervisor

COPY api ./
COPY supervisord.ini /etc/supervisor/conf.d/supervisord.conf

# Запускаем supervisord, который выполнит миграции, запустит API
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]