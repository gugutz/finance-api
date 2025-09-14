# Makefile for finance-api

.PHONY: requirements env env-down

# Generates requirements.txt from pyproject.toml
requirements:
	@echo "Generating requirements.txt from pyproject.toml..."
	@pdm export -f requirements -o requirements.txt --without-hashes

install:
	pip install -r requirements.txt

# Starts the local development environment (PostgreSQL database)
env:
	@echo "Starting local database via Docker Compose..."
	@docker compose up -d

# Stops the local development environment
env-down:
	@echo "Stopping local database..."
	@docker compose down


rundev:
	uvicorn main:app --reload

runprod: requirements install
	uvicorn main:app 

pgcli:
	pgcli -h localhost -p 5432 -U finance_user -p finance_password
