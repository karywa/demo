# Makefile for Agent Scheduling Control Plane

PYTHON ?= python3

.PHONY: run test ui lint

# Run the CLI.
# Usage:
#   make run INPUT=sample.csv
run:
	@if [ -z "$(INPUT)" ]; then \
	  echo "Usage: make run INPUT=path/to/input.csv"; \
	  exit 1; \
	fi
	$(PYTHON) -m scheduler.cli --input $(INPUT)

# Run tests (unit + golden).
test:
	$(PYTHON) -m pytest -q

# Run the tiny UI (Flask app).
# Opens http://localhost:5000
ui:
	$(PYTHON) web_app.py

# Optional: basic lint (if you add flake8 or ruff to requirements.txt)
lint:
	flake8 scheduler tests || true
