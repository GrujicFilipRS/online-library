@echo off

cd /d "%~dp0"
cd ../

uv run alembic upgrade head
docker compose -f docker-compose.prod.yml up -d --build
