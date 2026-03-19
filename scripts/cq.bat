@echo off

cd /d "%~dp0"
cd ../

uv sync
uv run pre-commit run --all-files
