.PHONY: install run test docker-up docker-down lint

install:
	uv sync

run:
	uv run python main.py

test:
	uv run pytest tests/

docker-up:
	docker compose up -d

docker-down:
	docker compose down

lint:
	uv run ruff check .
