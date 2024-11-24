.PHONY: dev pre-commit isort black dist pylint lint

dev: pre-commit

pre-commit:
	pre-commit install
	pre-commit autoupdate

isort:
	isort . --profile black

black:
	black .

flake8:
	flake8 .

pylint:
	pylint hse_fastapi_autotest

lint: isort black  pylint flake8

dist:
	poetry build
