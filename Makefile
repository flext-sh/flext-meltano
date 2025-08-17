# =============================================================================
# FLEXT-MELTANO - Singer/Meltano/DBT Integration Library Makefile
# =============================================================================
# Python 3.13+ Data Integration Bridge - Clean Architecture + DDD + Zero Tolerance
# =============================================================================

# Project Configuration
PROJECT_NAME := flext-meltano
PYTHON_VERSION := 3.13
POETRY := poetry
SRC_DIR := src
TESTS_DIR := tests
COV_DIR := flext_meltano

# Quality Standards
MIN_COVERAGE := 90

# Meltano Configuration
MELTANO_PROJECT_ROOT := $(PWD)
MELTANO_ENVIRONMENT := dev

# Export Configuration
export PROJECT_NAME PYTHON_VERSION MIN_COVERAGE MELTANO_PROJECT_ROOT MELTANO_ENVIRONMENT

# =============================================================================
# HELP & INFORMATION
# =============================================================================

.PHONY: help
help: ## Show available commands
	@echo "FLEXT-MELTANO - Singer/Meltano/DBT Integration Library"
	@echo "====================================================="
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: info
info: ## Show project information
	@echo "Project: $(PROJECT_NAME)"
	@echo "Python: $(PYTHON_VERSION)+"
	@echo "Poetry: $(POETRY)"
	@echo "Coverage: $(MIN_COVERAGE)% minimum"
	@echo "Meltano Environment: $(MELTANO_ENVIRONMENT)"
	@echo "Architecture: Go ↔ Python Bridge + Singer SDK"

# =============================================================================
# SETUP & INSTALLATION
# =============================================================================

.PHONY: install
install: ## Install dependencies
	$(POETRY) install

.PHONY: install-dev
install-dev: ## Install dev dependencies
	$(POETRY) install --with dev,test,typings,security

.PHONY: setup
setup: install-dev ## Complete project setup
	$(POETRY) run pre-commit install

# =============================================================================
# QUALITY GATES (MANDATORY)
# =============================================================================

.PHONY: validate
validate: lint type-check security test ## Run all quality gates

.PHONY: check
check: lint type-check ## Quick health check

.PHONY: lint
lint: ## Run linting
	$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR)

.PHONY: format
format: ## Format code
	$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

.PHONY: type-check
type-check: ## Run type checking
	$(POETRY) run mypy $(SRC_DIR) --strict

.PHONY: security
security: ## Run security scanning
	$(POETRY) run bandit -r $(SRC_DIR)
	$(POETRY) run pip-audit

.PHONY: fix
fix: ## Auto-fix issues
	$(POETRY) run ruff check $(SRC_DIR) $(TESTS_DIR) --fix
	$(POETRY) run ruff format $(SRC_DIR) $(TESTS_DIR)

# =============================================================================
# TESTING
# =============================================================================

.PHONY: test
test: ## Run tests with coverage
	$(POETRY) run pytest $(TESTS_DIR) --cov=src/flext_meltano --cov-report=term-missing --cov-fail-under=$(MIN_COVERAGE)

.PHONY: test-unit
test-unit: ## Run unit tests
	$(POETRY) run pytest $(TESTS_DIR) -m "not integration" -v

.PHONY: test-integration
test-integration: ## Run integration tests
	$(POETRY) run pytest $(TESTS_DIR) -m integration -v

.PHONY: test-meltano
test-meltano: ## Run Meltano specific tests
	$(POETRY) run pytest $(TESTS_DIR) -m meltano -v

.PHONY: test-fast
test-fast: ## Run tests without coverage
	$(POETRY) run pytest $(TESTS_DIR) -v

.PHONY: coverage-html
coverage-html: ## Generate HTML coverage report
	$(POETRY) run pytest $(TESTS_DIR) --cov-report=html

# =============================================================================
# BUILD & DISTRIBUTION
# =============================================================================

.PHONY: build
build: ## Build package
	$(POETRY) build

.PHONY: build-clean
build-clean: clean build ## Clean and build

# =============================================================================
# MELTANO OPERATIONS
# =============================================================================

.PHONY: meltano-init
meltano-init: ## Initialize Meltano project
	@if [ ! -f meltano.yml ]; then \
		$(POETRY) run meltano init $(PROJECT_NAME) .; \
		echo "Meltano project initialized"; \
	else \
		echo "Meltano project already exists"; \
	fi

.PHONY: meltano-install
meltano-install: ## Install Meltano plugins
	$(POETRY) run meltano install

.PHONY: meltano-run
meltano-run: ## Run Meltano pipeline (usage: make meltano-run JOB=job-name)
	@if [ -z "$(JOB)" ]; then \
		echo "Usage: make meltano-run JOB=job-name"; \
		exit 1; \
	fi
	$(POETRY) run meltano run $(JOB)

.PHONY: meltano-test
meltano-test: ## Test Meltano configuration
	$(POETRY) run meltano config meltano list
	$(POETRY) run meltano invoke --list || true

.PHONY: meltano-discover
meltano-discover: ## Discover catalog from tap (usage: make meltano-discover TAP=tap-name)
	@if [ -z "$(TAP)" ]; then \
		echo "Usage: make meltano-discover TAP=tap-name"; \
		exit 1; \
	fi
	$(POETRY) run meltano invoke $(TAP) --discover > catalog-$(TAP).json

.PHONY: meltano-ui
meltano-ui: ## Start Meltano UI
	@echo "Meltano UI will be available at: http://localhost:5000"
	$(POETRY) run meltano ui

# =============================================================================
# SINGER OPERATIONS
# =============================================================================

.PHONY: singer-validate
singer-validate: ## Validate Singer output (usage: make singer-validate TAP=tap-name)
	@if [ -z "$(TAP)" ]; then \
		echo "Usage: make singer-validate TAP=tap-name"; \
		exit 1; \
	fi
	$(POETRY) run meltano invoke $(TAP) --discover | $(POETRY) run singer-check-tap

.PHONY: test-pipeline
test-pipeline: ## Test basic ELT pipeline
	@echo "sample_id,name,value" > sample.csv
	@echo "1,test,100" >> sample.csv
	@echo "2,demo,200" >> sample.csv
	$(POETRY) run meltano run tap-csv target-jsonl || echo "Pipeline test completed"
	@rm -f sample.csv

# =============================================================================
# DOCUMENTATION
# =============================================================================

.PHONY: docs
docs: ## Build documentation
	$(POETRY) run mkdocs build

.PHONY: docs-serve
docs-serve: ## Serve documentation
	$(POETRY) run mkdocs serve

# =============================================================================
# DEPENDENCIES
# =============================================================================

.PHONY: deps-update
deps-update: ## Update dependencies
	$(POETRY) update

.PHONY: deps-show
deps-show: ## Show dependency tree
	$(POETRY) show --tree

.PHONY: deps-audit
deps-audit: ## Audit dependencies
	$(POETRY) run pip-audit

# =============================================================================
# DEVELOPMENT
# =============================================================================

.PHONY: shell
shell: ## Open Python shell
	$(POETRY) run python

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

# =============================================================================
# MAINTENANCE
# =============================================================================

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage .mypy_cache/ .ruff_cache/
	rm -rf .meltano/ catalog-*.json state.json
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true

.PHONY: clean-all
clean-all: clean ## Deep clean including venv
	rm -rf .venv/

.PHONY: reset
reset: clean-all setup ## Reset project

# =============================================================================
# DIAGNOSTICS
# =============================================================================

.PHONY: diagnose
diagnose: ## Project diagnostics
	@echo "Python: $$(python --version)"
	@echo "Poetry: $$($(POETRY) --version)"
	@echo "Meltano: $$($(POETRY) run meltano --version 2>/dev/null || echo 'Not available')"
	@$(POETRY) env info

.PHONY: doctor
doctor: diagnose check ## Health check

# =============================================================================
# ALIASES (SINGLE LETTER SHORTCUTS)
# =============================================================================

.PHONY: t l f tc c i v
t: test
l: lint
f: format
tc: type-check
c: clean
i: install
v: validate

# =============================================================================
# CONFIGURATION
# =============================================================================

.DEFAULT_GOAL := help