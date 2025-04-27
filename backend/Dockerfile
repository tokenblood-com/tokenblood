FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app/

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock README.md /app/

RUN poetry install --without dev --no-root

# COPY ./scripts /app/scripts
# COPY ./alembic.ini /app/
COPY ./app /app/app

RUN poetry install --without dev 
CMD ["poetry", "run", "fastapi", "run", "--workers", "4", "app/main.py"]