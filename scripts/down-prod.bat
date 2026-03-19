@echo off

cd /d "%~dp0"
cd ../

docker compose -f docker-compose.prod.yml down
