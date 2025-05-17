FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /tokenblood/backend

RUN pip install --no-cache-dir poetry

COPY backend/pyproject.toml backend/poetry.lock backend/README.md /tokenblood/backend/

COPY ai/src /tokenblood/ai/src
COPY ai/pyproject.toml ai/poetry.lock ai/README.md /tokenblood/ai/

RUN poetry install --without dev --no-root

# COPY ./scripts /app/scripts
# COPY ./alembic.ini /app/
COPY backend/app /tokenblood/backend/app

RUN poetry install --without dev
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"] 