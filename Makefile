# Makefile for finance-api

.PHONY: requirements env env-down

# Generates requirements.txt from pyproject.toml
requirements:
	@echo "Generating requirements.txt from pyproject.toml..."
	@pdm export -f requirements -o requirements.txt --without-hashes

# Starts the local development environment (PostgreSQL database)
env:
	@echo "Starting local database via Docker Compose..."
	@docker compose up -d

# Stops the local development environment
env-down:
	@echo "Stopping local database..."
	@docker compose down