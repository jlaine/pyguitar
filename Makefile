all:
	@echo "Usage: make lint|test"
	@exit 1

lint:
	flake8 scripts src tests
	isort --check-only --diff scripts src tests
	black --check --diff scripts src tests
	mypy scripts src tests

test:
	coverage erase
	coverage run -m unittest discover -v
	coverage report
	coverage xml

.PHONY: lint
