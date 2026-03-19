@echo off

cd /d "%~dp0"
cd ../

uv sync
uv run pytest
