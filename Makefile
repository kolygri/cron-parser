.PHONY: format lint test build

format:
	poetry run black .
	poetry run isort .

lint:
	poetry run mypy src tests

test:
	poetry run pytest

build: format lint test
	poetry build
