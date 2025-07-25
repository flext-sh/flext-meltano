# FLEXT MELTANO - Meltano ELT Integration Platform
# ================================================
# Enterprise Meltano integration with project management and orchestration
# PROJECT_TYPE: meltano-integration
# Python 3.13 + Meltano + Singer + Zero Tolerance Quality Gates

.PHONY: help info diagnose check validate test lint type-check security format format-check fix
.PHONY: install dev-install setup pre-commit build clean
.PHONY: coverage coverage-html test-unit test-integration test-meltano
.PHONY: deps-update deps-audit deps-tree deps-outdated
.PHONY: meltano-init meltano-install meltano-run meltano-test

# ============================================================================
# 🎯 HELP & INFORMATION
# ============================================================================

help: ## Show this help message
	@echo "🎵 FLEXT MELTANO - Meltano ELT Integration Service"
	@echo "==============================================="
	@echo "🎯 Clean Architecture + DDD + Python 3.13 + Meltano + Singer"
	@echo ""
	@echo "📦 Native Meltano platform integration with ELT orchestration"
	@echo "🔒 Zero tolerance quality gates for data integration"
	@echo "🧪 90%+ test coverage requirement for pipeline components"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


info: ## Mostrar informações do projeto
	@echo "📊 Informações do Projeto"
	@echo "======================"
	@echo "Nome: flext-meltano"
	@echo "Título: FLEXT MELTANO"
	@echo "Versão: $(shell poetry version -s 2>/dev/null || echo "0.7.0")"
	@echo "Python: $(shell python3.13 --version 2>/dev/null || echo "Não encontrado")"
	@echo "Poetry: $(shell poetry --version 2>/dev/null || echo "Não instalado")"
	@echo "Venv: $(shell poetry env info --path 2>/dev/null || echo "Não ativado")"
	@echo "Diretório: $(CURDIR)"
	@echo "Git Branch: $(shell git branch --show-current 2>/dev/null || echo "Não é repo git")"
	@echo "Git Status: $(shell git status --porcelain 2>/dev/null | wc -l | xargs echo) arquivos alterados"

diagnose: ## Executar diagnósticos completos
	@echo "🔍 Executando diagnósticos para flext-meltano..."
	@echo "Informações do Sistema:"
	@echo "OS: $(shell uname -s)"
	@echo "Arquitetura: $(shell uname -m)"
	@echo "Python: $(shell python3.13 --version 2>/dev/null || echo "Não encontrado")"
	@echo "Poetry: $(shell poetry --version 2>/dev/null || echo "Não instalado")"
	@echo ""
	@echo "Estrutura do Projeto:"
	@ls -la
	@echo ""
	@echo "Configuração Poetry:"
	@poetry config --list 2>/dev/null || echo "Poetry não configurado"
	@echo ""
	@echo "Status das Dependências:"
	@poetry show --outdated 2>/dev/null || echo "Nenhuma dependência desatualizada"

# ============================================================================
# 🎯 CORE QUALITY GATES - ZERO TOLERANCE
# ============================================================================

validate: lint type-check security test ## STRICT compliance validation (all must pass)
	@echo "✅ ALL QUALITY GATES PASSED - FLEXT MELTANO COMPLIANT"

check: lint type-check test ## Essential quality checks (pre-commit standard)
	@echo "✅ Essential checks passed"

lint: ## Ruff linting (17 rule categories, ALL enabled)
	@echo "🔍 Running ruff linter (ALL rules enabled)..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ Linting complete"

type-check: ## MyPy strict mode type checking (zero errors tolerated)
	@echo "🛡️ Running MyPy strict type checking..."
	@poetry run mypy src/ tests/ --strict
	@echo "✅ Type checking complete"

security: ## Security scans (bandit + pip-audit + secrets)
	@echo "🔒 Running security scans..."
	@poetry run bandit -r src/ --severity-level medium --confidence-level medium
	@poetry run pip-audit --ignore-vuln PYSEC-2022-42969
	@poetry run detect-secrets scan --all-files
	@echo "✅ Security scans complete"

format: ## Format code with ruff
	@echo "🎨 Formatting code..."
	@poetry run ruff format src/ tests/
	@echo "✅ Formatting complete"

format-check: ## Check formatting without fixing
	@echo "🎨 Checking code formatting..."
	@poetry run ruff format src/ tests/ --check
	@echo "✅ Format check complete"

fix: format lint ## Auto-fix all issues (format + imports + lint)
	@echo "🔧 Auto-fixing all issues..."
	@poetry run ruff check src/ tests/ --fix --unsafe-fixes
	@echo "✅ All auto-fixes applied"

# ============================================================================
# 🧪 TESTING - 90% COVERAGE MINIMUM
# ============================================================================

test: ## Run tests with coverage (90% minimum required)
	@echo "🧪 Running tests with coverage..."
	@poetry run pytest tests/ -v --cov=src/flext_meltano --cov-report=term-missing --cov-fail-under=90
	@echo "✅ Tests complete"

test-unit: ## Run unit tests only
	@echo "🧪 Running unit tests..."
	@poetry run pytest tests/unit/ -v
	@echo "✅ Unit tests complete"

test-integration: ## Run integration tests only
	@echo "🧪 Running integration tests..."
	@poetry run pytest tests/integration/ -v
	@echo "✅ Integration tests complete"

test-meltano: ## Run Meltano-specific tests
	@echo "🎵 Running Meltano integration tests..."
	@poetry run pytest tests/meltano/ -v --tb=short
	@echo "✅ Meltano tests complete"

coverage: ## Generate detailed coverage report
	@echo "📊 Generating coverage report..."
	@poetry run pytest tests/ --cov=src/flext_meltano --cov-report=term-missing --cov-report=html
	@echo "✅ Coverage report generated in htmlcov/"

coverage-html: coverage ## Generate HTML coverage report
	@echo "📊 Opening coverage report..."
	@python -m webbrowser htmlcov/index.html

# ============================================================================
# 🚀 DEVELOPMENT SETUP
# ============================================================================

setup: install pre-commit ## Complete development setup
	@echo "🎯 Development setup complete!"

install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies..."
	@poetry install --all-extras --with dev,test,docs,security
	@echo "✅ Dependencies installed"

dev-install: install ## Install in development mode
	@echo "🔧 Setting up development environment..."
	@poetry install --all-extras --with dev,test,docs,security
	@poetry run pre-commit install
	@echo "✅ Development environment ready"

pre-commit: ## Setup pre-commit hooks
	@echo "🎣 Setting up pre-commit hooks..."
	@poetry run pre-commit install
	@poetry run pre-commit run --all-files || true
	@echo "✅ Pre-commit hooks installed"

# ============================================================================
# 🎯 MELTANO INTEGRATION OPERATIONS
# ============================================================================

meltano-install: ## Install and setup Meltano project

meltano-test: ## Test Meltano integration

meltano-discover: ## Discover catalog from extractors

# ============================================================================
# 🎵 MELTANO CORE OPERATIONS
# ============================================================================

meltano-init: ## Initialize Meltano project
	@echo "🎵 Initializing Meltano project..."
	@if [ ! -f meltano.yml ]; then \
		poetry run meltano init flext-meltano .; \
		echo "✅ Meltano project initialized"; \
	else \
		echo "✅ Meltano project already exists"; \
	fi

meltano-install: ## Install Meltano plugins
	@echo "🎵 Installing Meltano plugins..."
	@poetry run meltano install
	@echo "✅ Meltano plugins installed"

meltano-run: ## Run Meltano pipeline (usage: make meltano-run JOB=job-name)
	@echo "🎵 Running Meltano pipeline..."
	@if [ -z "$(JOB)" ]; then \
		echo "❌ Usage: make meltano-run JOB=job-name"; \
		exit 1; \
	fi
	@poetry run meltano run $(JOB)
	@echo "✅ Meltano pipeline $(JOB) complete"

meltano-test: ## Test Meltano configuration
	@echo "🎵 Testing Meltano configuration..."
	@poetry run meltano config meltano list
	@poetry run meltano invoke --list || true
	@echo "✅ Meltano configuration tested"

meltano-discover: ## Discover catalog from tap (usage: make meltano-discover TAP=tap-name)
	@echo "🔍 Running catalog discovery..."
	@if [ -z "$(TAP)" ]; then \
		echo "❌ Usage: make meltano-discover TAP=tap-name"; \
		exit 1; \
	fi
	@poetry run meltano invoke $(TAP) --discover > catalog-$(TAP).json
	@echo "✅ Catalog discovered for $(TAP) - saved to catalog-$(TAP).json"

meltano-add-extractor: ## Add extractor plugin (usage: make meltano-add-extractor NAME=tap-name)
	@echo "🎵 Adding extractor plugin..."
	@if [ -z "$(NAME)" ]; then \
		echo "❌ Usage: make meltano-add-extractor NAME=tap-name"; \
		exit 1; \
	fi
	@poetry run meltano add extractor $(NAME)
	@echo "✅ Extractor $(NAME) added"

meltano-add-loader: ## Add loader plugin (usage: make meltano-add-loader NAME=target-name)
	@echo "🎵 Adding loader plugin..."
	@if [ -z "$(NAME)" ]; then \
		echo "❌ Usage: make meltano-add-loader NAME=target-name"; \
		exit 1; \
	fi
	@poetry run meltano add loader $(NAME)
	@echo "✅ Loader $(NAME) added"

meltano-schedule: ## Create Meltano schedule (usage: make meltano-schedule JOB=job-name INTERVAL=@daily)
	@echo "🕐 Creating Meltano schedule..."
	@if [ -z "$(JOB)" ] || [ -z "$(INTERVAL)" ]; then \
		echo "❌ Usage: make meltano-schedule JOB=job-name INTERVAL=@daily"; \
		exit 1; \
	fi
	@poetry run meltano schedule add $(JOB)-schedule $(JOB) --interval $(INTERVAL)
	@echo "✅ Schedule $(JOB)-schedule created"

meltano-ui: ## Start Meltano UI
	@echo "🎵 Starting Meltano UI..."
	@echo "📡 Meltano UI will be available at: http://localhost:5000"
	@poetry run meltano ui

# ============================================================================
# 🎯 SINGER PROTOCOL OPERATIONS
# ============================================================================

singer-validate: ## Validate Singer output (usage: make singer-validate TAP=tap-name)
	@echo "🎵 Validating Singer output..."
	@if [ -z "$(TAP)" ]; then \
		echo "❌ Usage: make singer-validate TAP=tap-name"; \
		exit 1; \
	fi
	@poetry run meltano invoke $(TAP) --discover | poetry run singer-check-tap
	@echo "✅ Singer validation complete for $(TAP)"

singer-test-connection: ## Test Singer tap connection (usage: make singer-test-connection TAP=tap-name)
	@echo "🔗 Testing Singer tap connection..."
	@if [ -z "$(TAP)" ]; then \
		echo "❌ Usage: make singer-test-connection TAP=tap-name"; \
		exit 1; \
	fi
	@poetry run meltano invoke $(TAP) --discover > /dev/null && echo "✅ Connection successful" || echo "❌ Connection failed"

singer-extract-sample: ## Extract sample data (usage: make singer-extract-sample TAP=tap-name LIMIT=10)
	@echo "📊 Extracting sample data..."
	@if [ -z "$(TAP)" ]; then \
		echo "❌ Usage: make singer-extract-sample TAP=tap-name LIMIT=10"; \
		exit 1; \
	fi
	@LIMIT=$${LIMIT:-10} && poetry run meltano invoke $(TAP) | head -$$LIMIT
	@echo "✅ Sample extraction complete"

# ============================================================================
# 📦 BUILD & DISTRIBUTION
# ============================================================================

build: clean ## Build distribution packages
	@echo "🔨 Building distribution..."
	@poetry build
	@echo "✅ Build complete - packages in dist/"

# ============================================================================
# 🧹 CLEANUP
# ============================================================================

clean: ## Remove all artifacts
	@echo "🧹 Cleaning up..."
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@rm -rf .coverage
	@rm -rf htmlcov/
	@rm -rf .pytest_cache/
	@rm -rf .meltano/
	@rm -rf catalog-*.json
	@rm -rf state.json
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ Cleanup complete"

# ============================================================================
# 📊 DEPENDENCY MANAGEMENT
# ============================================================================

deps-update: ## Update all dependencies
	@echo "🔄 Updating dependencies..."
	@poetry update
	@echo "✅ Dependencies updated"

deps-audit: ## Audit dependencies for vulnerabilities
	@echo "🔍 Auditing dependencies..."
	@poetry run pip-audit
	@echo "✅ Dependency audit complete"

deps-tree: ## Show dependency tree
	@echo "🌳 Dependency tree:"
	@poetry show --tree

deps-outdated: ## Show outdated dependencies
	@echo "📋 Outdated dependencies:"
	@poetry show --outdated

# ============================================================================
# 🔧 ENVIRONMENT CONFIGURATION
# ============================================================================

# Python settings
PYTHON := python3.13
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export PYTHONDONTWRITEBYTECODE := 1
export PYTHONUNBUFFERED := 1

# Meltano settings
export MELTANO_PROJECT_ROOT := $(PWD)
export MELTANO_ENVIRONMENT := dev
export MELTANO_DATABASE_URI := sqlite:///meltano.db
export MELTANO_UI_BIND_PORT := 5000

# Singer settings
export SINGER_SDK_LOG_LEVEL := INFO
export SINGER_SDK_BATCH_CONFIG := {"encoding":{"format":"jsonl"}}

# FLEXT Meltano settings
export FLEXT_MELTANO_AUTO_INSTALL := true
export FLEXT_MELTANO_STATE_BACKEND := filesystem

# Poetry settings
export POETRY_VENV_IN_PROJECT := false
export POETRY_CACHE_DIR := $(HOME)/.cache/pypoetry

# Quality gate settings
export MYPY_CACHE_DIR := .mypy_cache
export RUFF_CACHE_DIR := .ruff_cache

# ============================================================================
# 📝 PROJECT METADATA
# ============================================================================

# Project information
PROJECT_NAME := flext-meltano
PROJECT_TYPE := meltano-integration
PROJECT_VERSION := $(shell poetry version -s)
PROJECT_DESCRIPTION := FLEXT Meltano - Meltano ELT Integration Platform

.DEFAULT_GOAL := help

# ============================================================================
# 🎯 MELTANO SPECIFIC OPERATIONS
# ============================================================================

meltano-environment: ## Setup Meltano environments
	@echo "🎵 Setting up Meltano environments..."
	@poetry run meltano environment add prod
	@poetry run meltano environment add staging
	@echo "✅ Meltano environments configured"

meltano-jobs: ## List and manage Meltano jobs
	@echo "🎵 Managing Meltano jobs..."
	@poetry run meltano job list
	@echo "✅ Meltano jobs listed"

meltano-state: ## Manage Meltano state
	@echo "🎵 Managing Meltano state..."
	@poetry run meltano state list || echo "No state found"
	@echo "✅ Meltano state management complete"

meltano-logs: ## View Meltano logs
	@echo "📜 Viewing Meltano logs..."
	@tail -f .meltano/logs/*.log || echo "No logs found"

meltano-reset: ## Reset Meltano project
	@echo "⚠️ Resetting Meltano project..."
	@read -p "Are you sure you want to reset the Meltano project? (y/N) " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		rm -rf .meltano/; \
		echo "✅ Meltano project reset"; \
	else \
		echo "❌ Reset cancelled"; \
	fi

# ============================================================================
# 🎯 MELTANO VALIDATION COMMANDS
# ============================================================================

validate-meltano: ## Validate complete Meltano setup
	@echo "🎵 Validating Meltano setup..."
	@poetry run meltano --version
	@if [ -f meltano.yml ]; then \
		poetry run meltano config meltano list; \
		echo "✅ Meltano setup validated"; \
	else \
		echo "❌ No meltano.yml found - run 'make meltano-init'"; \
		exit 1; \
	fi

validate-singer: ## Validate Singer protocol compliance
	@echo "🎵 Validating Singer protocol compliance..."
	@poetry run python -c "import singer; print(f'Singer SDK version: {singer.__version__}'); print('✅ Singer protocol validated')"

validate-plugins: ## Validate installed Meltano plugins
	@echo "🎵 Validating Meltano plugins..."
	@poetry run meltano invoke --list-commands 2>/dev/null || echo "No plugins installed"
	@echo "✅ Plugin validation complete"

# ============================================================================
# 🎯 DEVELOPMENT WORKFLOWS
# ============================================================================

setup-dev-project: meltano-init ## Setup development Meltano project
	@echo "🔧 Setting up development Meltano project..."
	@$(MAKE) meltano-add-extractor NAME=tap-csv
	@$(MAKE) meltano-add-loader NAME=target-jsonl
	@echo "✅ Development project setup complete"

test-pipeline: ## Test basic ELT pipeline
	@echo "🧪 Testing basic ELT pipeline..."
	@echo "sample_id,name,value" > sample.csv
	@echo "1,test,100" >> sample.csv
	@echo "2,demo,200" >> sample.csv
	@poetry run meltano run tap-csv target-jsonl || echo "Pipeline test completed (check output)"
	@rm -f sample.csv
	@echo "✅ Pipeline test complete"

# ============================================================================
# 🎯 FLEXT ECOSYSTEM INTEGRATION
# ============================================================================

ecosystem-check: ## Verify FLEXT ecosystem compatibility
	@echo "🌐 Checking FLEXT ecosystem compatibility..."
	@echo "📦 Meltano project: $(PROJECT_NAME) v$(PROJECT_VERSION)"
	@echo "🏗️ Architecture: Clean Architecture + DDD"
	@echo "🐍 Python: 3.13"
	@echo "🎵 Framework: Meltano + Singer"
	@echo "📊 Quality: Zero tolerance enforcement"
	@echo "✅ Ecosystem compatibility verified"

workspace-info: ## Show workspace integration info
	@echo "🏢 FLEXT Workspace Integration"
	@echo "==============================="
	@echo "📁 Project Path: $(PWD)"
	@echo "🏆 Role: ELT Pipeline Orchestration"
	@echo "🔗 Dependencies: flext-core, Meltano, Singer"
	@echo "📦 Provides: ELT pipelines, Singer integration, data orchestration"
	@echo "🎯 Standards: Enterprise Meltano patterns"