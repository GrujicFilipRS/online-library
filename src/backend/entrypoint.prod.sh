#!/bin/sh
set -e

uv run alembic upgrade head

exec /app/.venv/bin/gunicorn src.backend.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
