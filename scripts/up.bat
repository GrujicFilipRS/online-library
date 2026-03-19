@echo off

cd /d "%~dp0"
cd ../

uv run alembic upgrade head
docker compose -f docker-compose.dev.yml up -d --build
