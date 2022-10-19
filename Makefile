all:
	@echo "Usage: make lint|test"
	@exit 1

lint:
	flake8 scripts src tests
	isort --check-only --diff scripts src tests
	black --check --diff scripts src tests

test:
	python -m unittest

.PHONY: lint
