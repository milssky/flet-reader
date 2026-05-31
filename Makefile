SHELL := /usr/bin/env bash

.DEFAULT_GOAL := help

.PHONY: help
help: ## Show the help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: pytest
pytest: ## Execute pytest.
	uv run pytest

.PHONY: mypy
mypy: ## Execute mypy.
	uv run mypy .

.PHONY: run
run: ## Launch app
	uv run flet run

.PHONY: format
format: ## Format by Ruff
	uv run ruff format

.PHONY: lint
lint: ## Execute ruff check and format
	uv run ruff check --exit-non-zero-on-fix && uv run ruff format --check --diff && uv run flake8 .

.PHONY: sql-lint
sql-lint: ## Lint sql files
	uv run sqlfluff lint flet_reader

.PHONY: codespell
codespell: ## Codespell all
	uv run codespell .

.PHONY: test
test: ## Run all dev checks and tests
	make lint && make mypy && make pytest && make sql-lint && make codespell
