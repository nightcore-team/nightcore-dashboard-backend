date = $(shell date)

lint:
	uv run ruff check --config=pyproject.toml .

format:
	uv run ruff format --config=pyproject.toml .

.PHONY: lint format