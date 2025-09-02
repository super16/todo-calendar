#!make

.PHONY: dev
dev:
	npm --prefix todo_calendar/frontend run dev

.PHONY: install
install:
	uv sync
	pnpm --prefix todo_calendar/frontend i

.PHONY: lint
lint:
	uv run mypy .
	uv run ruff check --fix .

.PHONY: migrate
migrate:
	uv run alembic upgrade head

.PHONY: run
run:
	pnpm --prefix todo_calendar/frontend run build
	uv run uvicorn todo_calendar.main:app

.PHONY: test
test:
	uv run pytest
