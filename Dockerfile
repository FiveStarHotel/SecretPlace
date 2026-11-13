FROM node:24-slim AS frontend
WORKDIR /frontend
COPY frontend/ ./
RUN npm ci && npm run build

FROM python:3.14.9-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /bin/
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY . .
COPY --from=frontend /frontend/dist ./frontend/dist

RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*
COPY crontab /etc/cron.d/cleanup

EXPOSE 8080
CMD ["sh", "-c", "uv run alembic upgrade head && cron && uv run uvicorn main:app --host 0.0.0.0 --port 8080"]