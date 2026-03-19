@echo off

cd /d "%~dp0"
cd ../

docker compose -f docker-compose.dev.yml down
