.PHONY: help up down up-prod test cq

help:
	@echo "all commands:"
	@echo "up (run docker compose in development mode)"
	@echo "down (stop docker compose)"
	@echo "up-prod (run docker compose in production mode)"
	@echo "test (run pytest)"
	@echo "cq (run pre-commit)"

up:
	uv run alembic upgrade head
	docker compose -f docker-compose.dev.yml up -d --build

down:
	docker compose -f docker-compose.dev.yml down

down-prod:
	docker compose -f docker-compose.prod.yml down

up-prod:
	uv run alembic upgrade head
	docker compose -f docker-compose.prod.yml up -d --build

test:
	uv sync
	uv run pytest

cq:
	uv sync
	uv run pre-commit run --all-files
