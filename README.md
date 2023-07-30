# todo-calendar

Application with todo calendar. Day to day planning.

## Development

Requires [poetry](https://python-poetry.org/).

### Preparation

```shell
poetry install
poetry run alembic upgrade head
```

### Lint

```shell
poetry run mypy .
poetry run ruff --fix .
```

### Test

```shell
poetry run pytest
```

### Run

```shell
cp .env.example .env
poetry run uvicorn todo_calendar.main:app
```
