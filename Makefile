all:
	@echo "Usage: make lint|test"
	@exit 1

lint:
	ruff check .
	ruff format --check --diff .
	mypy examples src tests

test:
	coverage erase
	coverage run -m unittest discover -v
	coverage report
	coverage xml

.PHONY: lint
