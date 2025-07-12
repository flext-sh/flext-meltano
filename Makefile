# FLEXT-MELTANO Makefile - Enterprise ETL Pipeline with Meltano Integration
# Uses FLEXT standardized patterns and flext-core integration

# Project Configuration
PROJECT_NAME := flext-meltano
PYTHON_VERSION := 3.13
POETRY := poetry
PYTHON := $(POETRY) run python
PYTEST := $(POETRY) run pytest
RUFF := $(POETRY) run ruff
MYPY := $(POETRY) run mypy

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
RED := \033[0;31m
RESET := \033[0m

# Default target
.DEFAULT_GOAL := help

## Help
help: ## Show this help message
	@echo "$(BLUE)FLEXT-MELTANO Makefile$(RESET)"
	@echo "Enterprise ETL Pipeline with Meltano Integration"
	@echo ""
	@echo "$(GREEN)Available commands:$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(BLUE)%-20s$(RESET) %s\\n", $$1, $$2}' $(MAKEFILE_LIST)

## Development
install: ## Install all dependencies
	@echo "$(BLUE)📦 Installing dependencies for $(PROJECT_NAME)...$(RESET)"
	@$(POETRY) install
	@echo "$(GREEN)✅ Dependencies installed$(RESET)"

install-dev: ## Install development dependencies
	@echo "$(BLUE)📦 Installing development dependencies...$(RESET)"
	@$(POETRY) install --with dev
	@echo "$(GREEN)✅ Development dependencies installed$(RESET)"

update: ## Update dependencies
	@echo "$(BLUE)🔄 Updating dependencies...$(RESET)"
	@$(POETRY) update
	@echo "$(GREEN)✅ Dependencies updated$(RESET)"

## Code Quality
lint: ## Run linting
	@echo "$(BLUE)🔍 Running linting for $(PROJECT_NAME)...$(RESET)"
	@$(RUFF) check src/ tests/ || true
	@echo "$(GREEN)✅ Linting complete$(RESET)"

lint-fix: ## Fix linting issues
	@echo "$(BLUE)🔧 Fixing linting issues...$(RESET)"
	@$(RUFF) check --fix src/ tests/ || true
	@$(RUFF) format src/ tests/ || true
	@echo "$(GREEN)✅ Linting issues fixed$(RESET)"

format: ## Format code
	@echo "$(BLUE)🎨 Formatting code...$(RESET)"
	@$(RUFF) format src/ tests/
	@echo "$(GREEN)✅ Code formatted$(RESET)"

type-check: ## Run type checking
	@echo "$(BLUE)🔍 Running type checking...$(RESET)"
	@$(MYPY) src/flext_meltano/ || true
	@echo "$(GREEN)✅ Type checking complete$(RESET)"

check: lint type-check ## Run all code quality checks

## Testing
test: ## Run all tests
	@echo "$(BLUE)🧪 Running tests for $(PROJECT_NAME)...$(RESET)"
	@$(PYTEST) -v
	@echo "$(GREEN)✅ All tests passed$(RESET)"

test-unit: ## Run unit tests only
	@echo "$(BLUE)🧪 Running unit tests...$(RESET)"
	@$(PYTEST) tests/unit/ -v -m "not integration"
	@echo "$(GREEN)✅ Unit tests passed$(RESET)"

test-integration: ## Run integration tests only
	@echo "$(BLUE)🧪 Running integration tests...$(RESET)"
	@$(PYTEST) tests/integration/ -v -m "integration"
	@echo "$(GREEN)✅ Integration tests passed$(RESET)"

test-cov: ## Run tests with coverage
	@echo "$(BLUE)🧪 Running tests with coverage...$(RESET)"
	@$(PYTEST) --cov=flext_meltano --cov-report=html --cov-report=term-missing
	@echo "$(GREEN)✅ Tests with coverage complete$(RESET)"

## Meltano Operations
meltano-config: ## Show current Meltano configuration
	@echo "$(BLUE)⚙️ Showing FLEXT Meltano configuration...$(RESET)"
	@$(PYTHON) -c "from flext_meltano.config import get_meltano_settings; settings = get_meltano_settings(); print(f'Project: {settings.project_name}'); print(f'Version: {settings.project_version}'); print(f'Project Root: {settings.project.project_root}'); print(f'Environment: {settings.project.default_environment}'); print(f'Max Jobs: {settings.execution.max_concurrent_jobs}')"

meltano-test: ## Test Meltano system
	@echo "$(BLUE)🧪 Testing FLEXT Meltano system...$(RESET)"
	@$(PYTHON) -c "from flext_meltano.config import get_meltano_settings; settings = get_meltano_settings(); print('✅ Meltano configuration loaded successfully'); print(f'Project: {settings.project_name}'); print(f'Environment: {settings.environment}'); print('✅ FLEXT Meltano system is working')"

meltano-init: ## Initialize new Meltano project
	@echo "$(BLUE)🚀 Initializing new Meltano project...$(RESET)"
	@$(PYTHON) -m flext_meltano.cli init --name example-project

meltano-install: ## Install Meltano plugins
	@echo "$(BLUE)🔌 Installing Meltano plugins...$(RESET)"
	@$(PYTHON) -m flext_meltano.cli install

meltano-run: ## Run Meltano pipeline
	@echo "$(BLUE)▶️ Running Meltano pipeline...$(RESET)"
	@$(PYTHON) -m flext_meltano.cli run

meltano-state: ## Show Meltano state
	@echo "$(BLUE)📊 Showing Meltano state...$(RESET)"
	@$(PYTHON) -m flext_meltano.cli state list

meltano-health: ## Check Meltano health
	@echo "$(BLUE)🏥 Checking Meltano health...$(RESET)"
	@$(PYTHON) -m flext_meltano.cli health

## Pipeline Operations
pipeline-list: ## List available pipelines
	@echo "$(BLUE)📋 Listing available pipelines...$(RESET)"
	@$(PYTHON) -m flext_meltano.pipeline list

pipeline-run: ## Run specific pipeline
	@echo "$(BLUE)▶️ Running pipeline...$(RESET)"
	@$(PYTHON) -m flext_meltano.pipeline run --name ${PIPELINE_NAME}

pipeline-status: ## Check pipeline status
	@echo "$(BLUE)📊 Checking pipeline status...$(RESET)"
	@$(PYTHON) -m flext_meltano.pipeline status

pipeline-logs: ## Show pipeline logs
	@echo "$(BLUE)📝 Showing pipeline logs...$(RESET)"
	@$(PYTHON) -m flext_meltano.pipeline logs --follow

## Build and Distribution
build: ## Build the package
	@echo "$(BLUE)🏗️ Building $(PROJECT_NAME)...$(RESET)"
	@$(POETRY) build
	@echo "$(GREEN)✅ Package built$(RESET)"

clean: ## Clean build artifacts
	@echo "$(BLUE)🧹 Cleaning build artifacts...$(RESET)"
	@rm -rf dist/ build/ *.egg-info/
	@rm -rf .coverage htmlcov/ .pytest_cache/
	@rm -rf .mypy_cache/ .ruff_cache/
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	@echo "$(GREEN)✅ Build artifacts cleaned$(RESET)"

## Development Utilities
shell: ## Start Python shell with project context
	@echo "$(BLUE)🐍 Starting Python shell...$(RESET)"
	@$(POETRY) shell

env: ## Show environment information
	@echo "$(BLUE)🌍 Environment Information:$(RESET)"
	@echo "Project: $(PROJECT_NAME)"
	@echo "Python: $(PYTHON_VERSION)"
	@echo "Poetry: $(shell $(POETRY) --version)"
	@echo "Virtual Environment: $(shell $(POETRY) env info --path)"

## Security
security: ## Run security checks
	@echo "$(BLUE)🔒 Running security checks...$(RESET)"
	@$(POETRY) run bandit -r src/ || true
	@echo "$(GREEN)✅ Security checks complete$(RESET)"

## Version Management
version: ## Show current version
	@echo "$(BLUE)📋 Current version:$(RESET)"
	@$(POETRY) version

bump-patch: ## Bump patch version
	@echo "$(BLUE)📈 Bumping patch version...$(RESET)"
	@$(POETRY) version patch
	@echo "$(GREEN)✅ Patch version bumped$(RESET)"

bump-minor: ## Bump minor version
	@echo "$(BLUE)📈 Bumping minor version...$(RESET)"
	@$(POETRY) version minor
	@echo "$(GREEN)✅ Minor version bumped$(RESET)"

bump-major: ## Bump major version
	@echo "$(BLUE)📈 Bumping major version...$(RESET)"
	@$(POETRY) version major
	@echo "$(GREEN)✅ Major version bumped$(RESET)"

## ETL Development
etl-scaffold: ## Create ETL pipeline scaffold
	@echo "$(BLUE)🏗️ Creating ETL pipeline scaffold...$(RESET)"
	@$(PYTHON) -m flext_meltano.cli scaffold --type pipeline

tap-scaffold: ## Create Singer tap scaffold
	@echo "$(BLUE)🔄 Creating Singer tap scaffold...$(RESET)"
	@$(PYTHON) -m flext_meltano.cli scaffold --type tap

target-scaffold: ## Create Singer target scaffold
	@echo "$(BLUE)🎯 Creating Singer target scaffold...$(RESET)"
	@$(PYTHON) -m flext_meltano.cli scaffold --type target

## Quick Development Workflow
dev: install lint-fix test ## Full development workflow (install, fix, test)
	@echo "$(GREEN)✅ Development workflow complete$(RESET)"

ci: check test ## Continuous integration workflow
	@echo "$(GREEN)✅ CI workflow complete$(RESET)"

## Information
info: ## Show project information
	@echo "$(BLUE)📊 Project Information:$(RESET)"
	@echo "Name: $(PROJECT_NAME)"
	@echo "Description: FLEXT Meltano - Enterprise ETL Pipeline with Meltano Integration"
	@echo "Python: $(PYTHON_VERSION)"
	@echo "Poetry: $(shell $(POETRY) --version)"
	@echo ""
	@echo "$(GREEN)📁 Project Structure:$(RESET)"
	@echo "├── src/flext_meltano/       # Source code"
	@echo "├── tests/                   # Test files"
	@echo "├── pyproject.toml          # Project configuration"
	@echo "├── Makefile                # This file"
	@echo "└── README.md               # Documentation"
	@echo ""
	@echo "$(GREEN)🚀 Quick Start:$(RESET)"
	@echo "1. make install             # Install dependencies"
	@echo "2. make meltano-test        # Test the system"
	@echo "3. make meltano-init        # Initialize project"
	@echo "4. make dev                 # Full development workflow"
	@echo ""
	@echo "$(GREEN)🔄 ETL Operations:$(RESET)"
	@echo "• make meltano-run          - Run ETL pipeline"
	@echo "• make pipeline-list        - List pipelines"
	@echo "• make pipeline-status      - Check status"
	@echo "• make meltano-state        - Show state"
	@echo ""
	@echo "Documentation available in README.md"

.PHONY: help install install-dev update lint lint-fix format type-check check test test-unit test-integration test-cov meltano-config meltano-test meltano-init meltano-install meltano-run meltano-state meltano-health pipeline-list pipeline-run pipeline-status pipeline-logs build clean shell env security version bump-patch bump-minor bump-major etl-scaffold tap-scaffold target-scaffold dev ci info
