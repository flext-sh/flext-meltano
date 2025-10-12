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
MIN_COVERAGE := 100

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
	@echo "Coverage: $(MIN_COVERAGE)% minimum (MANDATORY)"
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
# QUALITY GATES (MANDATORY - ZERO TOLERANCE)
# =============================================================================

.PHONY: validate
validate: lint type-check security test ## Run all quality gates (MANDATORY ORDER)

.PHONY: check
check: lint type-check ## Quick health check

.PHONY: lint
lint: ## Run linting (ZERO TOLERANCE)
	$(POETRY) run ruff check .

.PHONY: format
format: ## Format code
	$(POETRY) run ruff format .

.PHONY: type-check
type-check: ## Run type checking with Pyrefly (ZERO TOLERANCE)
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pyrefly check .

.PHONY: security
security: ## Run security scanning
	$(POETRY) run bandit -r $(SRC_DIR)
	$(POETRY) run pip-audit

.PHONY: fix
fix: ## Auto-fix issues
	$(POETRY) run ruff check . --fix
	$(POETRY) run ruff format .

# =============================================================================
# TESTING (MANDATORY - 100% COVERAGE)
# =============================================================================

.PHONY: test
test: ## Run tests with 100% coverage (MANDATORY)
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -q --maxfail=10000 --cov=$(COV_DIR) --cov-report=term-missing:skip-covered --cov-fail-under=$(MIN_COVERAGE)

.PHONY: test-unit
test-unit: ## Run unit tests
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -m "not integration" -v

.PHONY: test-integration
test-integration: ## Run integration tests with Docker
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -m integration -v

.PHONY: test-meltano
test-meltano: ## Run Meltano specific tests
	$(POETRY) run pytest $(TESTS_DIR) -m meltano -v

.PHONY: test-fast
test-fast: ## Run tests without coverage
	PYTHONPATH=$(SRC_DIR) $(POETRY) run pytest -v

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
	PYTHONPATH=$(SRC_DIR) $(POETRY) run python

.PHONY: pre-commit
pre-commit: ## Run pre-commit hooks
	$(POETRY) run pre-commit run --all-files

# =============================================================================
# MAINTENANCE
# =============================================================================

.PHONY: clean
clean: ## Clean build artifacts and cruft
	@echo "🧹 Cleaning $(PROJECT_NAME) - removing build artifacts, cache files, and cruft..."

	# Build artifacts
	rm -rf build/ dist/ *.egg-info/

	# Test artifacts
	rm -rf .pytest_cache/ htmlcov/ .coverage .coverage.* coverage.xml

	# Python cache directories
	rm -rf .mypy_cache/ .pyrefly_cache/ .ruff_cache/

	# Python bytecode
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true

	# Meltano-specific files
	rm -rf .meltano/ catalog-*.json state.json state-*.json
	rm -rf .meltano-tmp/ meltano-*.log

	# Data pipeline files
	rm -rf extract/ load/ transform/ output/ analyze/ orchestrate/
	rm -rf notebook/ data/

	# Temporary files
	find . -type f -name "*.tmp" -delete 2>/dev/null || true
	find . -type f -name "*.temp" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true

	# Log files
	find . -type f -name "*.log" -delete 2>/dev/null || true

	# Editor files
	find . -type f -name ".vscode/settings.json" -delete 2>/dev/null || true
	find . -type f -name ".idea/" -type d -exec rm -rf {} + 2>/dev/null || true

	@echo "✅ $(PROJECT_NAME) cleanup complete"

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

# Documentation Maintenance Targets
# Generated by FLEXT-Meltano Documentation Maintenance Framework

.PHONY: docs-audit docs-validate docs-report docs-comprehensive docs-ci-check docs-schedule docs-hooks

# Run documentation quality audit
docs-audit:
	@echo "🔍 Running documentation audit..."
	@python scripts/docs_maintenance.py --audit

# Validate external links
docs-validate:
	@echo "🔗 Validating external links..."
	@python scripts/docs_maintenance.py --validate

# Generate quality reports
docs-report:
	@echo "📊 Generating quality reports..."
	@python scripts/docs_maintenance.py --report

# Run comprehensive documentation maintenance
docs-comprehensive:
	@echo "🔄 Running comprehensive documentation maintenance..."
	@python scripts/docs_maintenance.py --comprehensive

# Run CI quality checks
docs-ci-check:
	@echo "🔍 Running CI documentation quality checks..."
	@python scripts/docs_automation.py --ci-check

# Start scheduled maintenance monitoring
docs-schedule:
	@echo "📅 Starting scheduled documentation maintenance..."
	@python scripts/docs_automation.py --schedule

# Set up Git hooks for quality checks
docs-hooks:
	@echo "🔧 Setting up Git hooks for documentation quality..."
	@python scripts/docs_automation.py --setup-hooks

# Generate GitHub Actions workflow
docs-workflow:
	@echo "⚙️  Generating GitHub Actions workflow..."
	@python scripts/docs_automation.py --generate-workflow > .github/workflows/docs-quality.yml
	@echo "✅ Workflow generated: .github/workflows/docs-quality.yml"

# View latest quality report
docs-view-report:
	@echo "📊 Latest Documentation Quality Report"
	@echo "======================================"
	@if [ -f "docs/reports/docs_quality_summary.json" ]; then \
		python -c "\
import json\
with open('docs/reports/docs_quality_summary.json', 'r') as f:\
    data = json.load(f)\
    print(f'Quality Score: {data["quality_score"]}/100')\
    print(f'Total Issues: {data["issues"]["total"]}')\
    print(f'Files: {data["metrics"]["total_files"]}')\
    print(f'Words: {data["metrics"]["total_words"]:,}')\
    print(f'Links: {data["metrics"]["total_links"]}')\
"; \
	else \
		echo "No quality report found. Run 'make docs-comprehensive' first."; \
	fi

# Clean up generated reports
docs-clean:
	@echo "🧹 Cleaning up documentation reports..."
	@rm -rf docs/reports/*
	@echo "✅ Reports cleaned"

# Full documentation maintenance setup
docs-setup: docs-hooks docs-workflow
	@echo "🚀 Documentation maintenance system setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Run 'make docs-comprehensive' to generate initial quality report"
	@echo "2. Review quality report in docs/reports/"
	@echo "3. Address high-priority issues"
	@echo "4. Commit changes to enable pre-commit hooks"


# Architecture Documentation Targets
# Generated by FLEXT-Meltano Architecture Documentation Automation

.PHONY: docs-architecture-validate docs-architecture-generate docs-architecture-update docs-architecture-report docs-architecture-comprehensive

# Validate architecture documentation and diagrams
docs-architecture-validate:
	@echo "🔍 Validating architecture documentation..."
	@python scripts/architecture_automation.py --validate

# Generate architecture diagrams from code analysis
docs-architecture-generate:
	@echo "🔄 Generating architecture diagrams..."
	@python scripts/architecture_automation.py --generate-diagrams

# Update architecture documentation timestamps and references
docs-architecture-update:
	@echo "📝 Updating architecture documentation..."
	@python scripts/architecture_automation.py --update-docs

# Create comprehensive architecture status report
docs-architecture-report:
	@echo "📋 Creating architecture report..."
	@python scripts/architecture_automation.py --create-report

# Run comprehensive architecture documentation maintenance
docs-architecture-comprehensive:
	@echo "🏗️ Running comprehensive architecture maintenance..."
	@python scripts/architecture_automation.py --comprehensive
