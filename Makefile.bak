# FLEXT-MELTANO Makefile - Enterprise Meltano Integration
# ======================================================

.PHONY: help install test clean lint format build docs meltano project pipeline state extensions

# Default target
help: ## Show this help message
	@echo "🎵 FLEXT-MELTANO - Enterprise Meltano Integration"
	@echo "==============================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\\033[36m%-20s\\033[0m %s\\n", $$1, $$2}'

# Installation & Setup
install: ## Install dependencies with Poetry
	@echo "📦 Installing dependencies for flext-meltano..."
	poetry install --all-extras

install-dev: ## Install with dev dependencies
	@echo "🛠️  Installing dev dependencies..."
	poetry install --all-extras --group dev --group test --group meltano

# Meltano Project Management
project-init: ## Initialize new Meltano project
	@echo "🎵 Initializing Meltano project..."
	@read -p "Project name: " project_name; \
	poetry run python -c "
from flext_meltano.project_manager import MeltanoProjectManager
import asyncio

async def main():
    manager = MeltanoProjectManager()
    print(f'🎯 Creating Meltano project: {project_name}')
    
    try:
        result = await manager.create_project('$$project_name', {
            'template': 'default',
            'python_version': '3.11',
            'enable_extensions': True
        })
        if result.success:
            print('✅ Project created successfully')
            print(f'📁 Project location: {result.value.path}')
        else:
            print(f'❌ Project creation failed: {result.error}')
    except Exception as e:
        print(f'💥 Error: {e}')

asyncio.run(main())
" project_name="$$project_name"

project-list: ## List all Meltano projects
	@echo "📋 Listing Meltano projects..."
	poetry run python -c "
from flext_meltano.project_manager import MeltanoProjectManager
import asyncio

async def main():
    manager = MeltanoProjectManager()
    projects = await manager.list_projects()
    
    if projects.success and projects.value:
        print('🎵 Available Meltano projects:')
        for project in projects.value:
            status = '✅' if project.is_valid else '❌'
            print(f'  {status} {project.name} - {project.path}')
    else:
        print('📭 No Meltano projects found')

asyncio.run(main())
"

project-validate: ## Validate Meltano project configuration
	@echo "🔍 Validating project configuration..."
	@read -p "Project name: " project_name; \
	poetry run python -c "
from flext_meltano.project_manager import MeltanoProjectManager
import asyncio

async def main():
    manager = MeltanoProjectManager()
    
    print(f'🔍 Validating project: $$project_name')
    result = await manager.validate_project('$$project_name')
    
    if result.success:
        validation = result.value
        print(f'✅ Project is valid')
        print(f'📊 Taps: {len(validation.taps)}')
        print(f'📤 Targets: {len(validation.targets)}')
        print(f'🔧 Transforms: {len(validation.transforms)}')
    else:
        print(f'❌ Validation failed: {result.error}')

asyncio.run(main())
" project_name="$$project_name"

# Pipeline Execution
pipeline-run: ## Run Meltano pipeline
	@echo "🚀 Running Meltano pipeline..."
	@read -p "Pipeline command (e.g., 'tap-csv target-jsonl'): " pipeline_cmd; \
	poetry run python -c "
from flext_meltano.orchestrator import MeltanoOrchestrator
import asyncio

async def main():
    orchestrator = MeltanoOrchestrator()
    
    print(f'🚀 Executing pipeline: $$pipeline_cmd')
    
    # Run pipeline with monitoring
    async for event in orchestrator.execute_pipeline('$$pipeline_cmd'):
        if event.level == 'INFO':
            print(f'ℹ️  {event.message}')
        elif event.level == 'ERROR':
            print(f'❌ {event.message}')
        elif event.level == 'SUCCESS':
            print(f'✅ {event.message}')
        else:
            print(f'📝 {event.message}')

asyncio.run(main())
" pipeline_cmd="$$pipeline_cmd"

pipeline-test: ## Test pipeline configuration
	@echo "🧪 Testing pipeline configuration..."
	poetry run python -c "
from flext_meltano.orchestrator import MeltanoOrchestrator
import asyncio

async def main():
    orchestrator = MeltanoOrchestrator()
    
    # Test with dry run
    print('🧪 Running pipeline test (dry run)...')
    result = await orchestrator.test_pipeline('tap-csv target-jsonl', dry_run=True)
    
    if result.success:
        print('✅ Pipeline configuration is valid')
        print(f'📊 Estimated records: {result.value.estimated_records}')
        print(f'⏱️  Estimated duration: {result.value.estimated_duration}s')
    else:
        print(f'❌ Pipeline test failed: {result.error}')

asyncio.run(main())
"

pipeline-schedule: ## Schedule pipeline execution
	@echo "📅 Scheduling pipeline..."
	@read -p "Pipeline command: " pipeline_cmd; \
	@read -p "Cron schedule (e.g., '0 2 * * *'): " cron_schedule; \
	poetry run python -c "
from flext_meltano.job_manager import JobManager
import asyncio

async def main():
    job_manager = JobManager()
    
    print(f'📅 Scheduling pipeline: $$pipeline_cmd')
    print(f'⏰ Schedule: $$cron_schedule')
    
    result = await job_manager.schedule_job(
        command='$$pipeline_cmd',
        schedule='$$cron_schedule',
        enabled=True
    )
    
    if result.success:
        print(f'✅ Job scheduled with ID: {result.value.job_id}')
    else:
        print(f'❌ Scheduling failed: {result.error}')

asyncio.run(main())
" pipeline_cmd="$$pipeline_cmd" cron_schedule="$$cron_schedule"

# State Management
state-backup: ## Create state backup
	@echo "💾 Creating state backup..."
	@read -p "Environment (production/staging/dev): " env_name; \
	poetry run python -c "
from flext_meltano.state_manager import StateManager
import asyncio

async def main():
    state_manager = StateManager()
    
    print(f'💾 Creating backup for environment: $$env_name')
    
    result = await state_manager.create_backup(
        environment='$$env_name',
        include_secrets=False,
        compress=True
    )
    
    if result.success:
        backup = result.value
        print(f'✅ Backup created successfully')
        print(f'🆔 Backup ID: {backup.backup_id}')
        print(f'📦 Size: {backup.size_mb:.1f} MB')
        print(f'📅 Created: {backup.created_at}')
    else:
        print(f'❌ Backup failed: {result.error}')

asyncio.run(main())
" env_name="$$env_name"

state-restore: ## Restore from state backup
	@echo "🔄 Restoring from backup..."
	@read -p "Backup ID: " backup_id; \
	@read -p "Target environment: " target_env; \
	poetry run python -c "
from flext_meltano.state_manager import StateManager
import asyncio

async def main():
    state_manager = StateManager()
    
    print(f'🔄 Restoring backup: $$backup_id')
    print(f'🎯 Target environment: $$target_env')
    
    result = await state_manager.restore_backup(
        backup_id='$$backup_id',
        target_env='$$target_env',
        validate=True
    )
    
    if result.success:
        print('✅ Backup restored successfully')
    else:
        print(f'❌ Restore failed: {result.error}')

asyncio.run(main())
" backup_id="$$backup_id" target_env="$$target_env"

state-list: ## List available state backups
	@echo "📋 Listing state backups..."
	poetry run python -c "
from flext_meltano.state_manager import StateManager
import asyncio

async def main():
    state_manager = StateManager()
    
    backups = await state_manager.list_backups()
    
    if backups.success and backups.value:
        print('💾 Available backups:')
        for backup in backups.value:
            print(f'  🆔 {backup.backup_id}')
            print(f'     📅 {backup.created_at}')
            print(f'     🌍 {backup.environment}')
            print(f'     📦 {backup.size_mb:.1f} MB')
            print('')
    else:
        print('📭 No backups found')

asyncio.run(main())
"

# Extensions Management
extensions-list: ## List available extensions
	@echo "🧩 Listing Meltano extensions..."
	poetry run python -c "
from flext_meltano.extensions import ExtensionManager
import asyncio

async def main():
    extension_manager = ExtensionManager()
    
    extensions = await extension_manager.list_extensions()
    
    if extensions.success:
        print('🧩 Available extensions:')
        for ext in extensions.value:
            status = '✅' if ext.enabled else '❌'
            print(f'  {status} {ext.name} - {ext.description}')
            print(f'      Version: {ext.version}')
            print(f'      Type: {ext.extension_type}')
            print('')
    else:
        print('❌ Failed to list extensions')

asyncio.run(main())
"

extensions-install: ## Install Meltano extension
	@echo "📦 Installing extension..."
	@read -p "Extension name (oracle-oic/ldap/monitoring/orchestration): " ext_name; \
	poetry run python -c "
from flext_meltano.extensions import ExtensionManager
import asyncio

async def main():
    extension_manager = ExtensionManager()
    
    print(f'📦 Installing extension: $$ext_name')
    
    result = await extension_manager.install_extension('$$ext_name')
    
    if result.success:
        print(f'✅ Extension {$$ext_name} installed successfully')
    else:
        print(f'❌ Installation failed: {result.error}')

asyncio.run(main())
" ext_name="$$ext_name"

extensions-configure: ## Configure extension
	@echo "⚙️  Configuring extension..."
	@read -p "Extension name: " ext_name; \
	poetry run python -c "
from flext_meltano.extensions import ExtensionManager
import asyncio

async def main():
    extension_manager = ExtensionManager()
    
    print(f'⚙️  Configuring extension: $$ext_name')
    
    # Show current configuration
    config = await extension_manager.get_configuration('$$ext_name')
    if config.success:
        print('📋 Current configuration:')
        for key, value in config.value.items():
            print(f'  {key}: {value}')
    
    print('\\n💡 Edit .env file to update configuration')

asyncio.run(main())
" ext_name="$$ext_name"

# Job Management
jobs-list: ## List running and scheduled jobs
	@echo "📋 Listing jobs..."
	poetry run python -c "
from flext_meltano.job_manager import JobManager
import asyncio

async def main():
    job_manager = JobManager()
    
    jobs = await job_manager.list_jobs()
    
    if jobs.success and jobs.value:
        print('💼 Jobs:')
        for job in jobs.value:
            status_icon = {
                'running': '🏃',
                'completed': '✅', 
                'failed': '❌',
                'scheduled': '📅',
                'paused': '⏸️'
            }.get(job.status, '❓')
            
            print(f'  {status_icon} {job.job_id}')
            print(f'     Command: {job.command}')
            print(f'     Status: {job.status}')
            print(f'     Created: {job.created_at}')
            print('')
    else:
        print('📭 No jobs found')

asyncio.run(main())
"

jobs-logs: ## View job logs
	@echo "📄 Viewing job logs..."
	@read -p "Job ID: " job_id; \
	poetry run python -c "
from flext_meltano.job_manager import JobManager
import asyncio

async def main():
    job_manager = JobManager()
    
    print(f'📄 Logs for job: $$job_id')
    print('=' * 50)
    
    async for log_entry in job_manager.stream_logs('$$job_id'):
        timestamp = log_entry.timestamp.strftime('%H:%M:%S')
        print(f'[{timestamp}] {log_entry.level}: {log_entry.message}')

asyncio.run(main())
" job_id="$$job_id"

# Performance Testing
performance-test: ## Run performance tests
	@echo "⚡ Running performance tests..."
	poetry run python -c "
from flext_meltano.orchestrator import MeltanoOrchestrator
from flext_meltano.project_manager import MeltanoProjectManager
import asyncio
import time

async def main():
    print('⚡ Meltano Performance Tests')
    print('=' * 40)
    
    # Test project initialization
    start = time.time()
    manager = MeltanoProjectManager()
    projects = await manager.list_projects()
    init_time = time.time() - start
    print(f'📊 Project list time: {init_time:.3f}s')
    
    # Test orchestrator startup
    start = time.time()
    orchestrator = MeltanoOrchestrator()
    await orchestrator.initialize()
    startup_time = time.time() - start
    print(f'🚀 Orchestrator startup: {startup_time:.3f}s')
    
    print('\\n📈 Performance Summary:')
    if init_time < 1.0:
        print('✅ Project operations: EXCELLENT')
    elif init_time < 3.0:
        print('⚠️  Project operations: ACCEPTABLE')
    else:
        print('❌ Project operations: NEEDS IMPROVEMENT')
        
    if startup_time < 2.0:
        print('✅ Orchestrator startup: EXCELLENT')
    elif startup_time < 5.0:
        print('⚠️  Orchestrator startup: ACCEPTABLE')
    else:
        print('❌ Orchestrator startup: NEEDS IMPROVEMENT')

asyncio.run(main())
"

# Testing
test: ## Run Meltano integration tests
	@echo "🧪 Running Meltano tests..."
	poetry run pytest tests/ -v --tb=short

test-coverage: ## Run tests with coverage
	@echo "📊 Running tests with coverage..."
	poetry run pytest tests/ --cov=src/flext_meltano --cov-report=html:reports/coverage --cov-report=xml:reports/coverage.xml --cov-fail-under=85

test-integration: ## Run integration tests with real Meltano
	@echo "🔗 Running integration tests..."
	@echo "⚠️  This requires Meltano to be installed"
	poetry run pytest tests/integration/ -v --tb=short

# Code Quality - Maximum Strictness
lint: ## Run all linters with maximum strictness
	@echo "🔍 Running maximum strictness linting for Meltano..."
	poetry run ruff check . --output-format=verbose
	@echo "✅ Ruff linting complete"

format: ## Format code with strict standards
	@echo "🎨 Formatting Meltano code..."
	poetry run black .
	poetry run ruff check --fix .
	@echo "✅ Code formatting complete"

type-check: ## Run strict type checking
	@echo "🎯 Running strict MyPy type checking..."
	poetry run mypy src/flext_meltano --strict --show-error-codes
	@echo "✅ Type checking complete"

check: lint type-check test ## Run all quality checks
	@echo "✅ All quality checks complete for flext-meltano!"

# Build & Distribution
build: ## Build the Meltano package
	@echo "🔨 Building flext-meltano package..."
	poetry build
	@echo "📦 Package built successfully"

# Documentation
docs: ## Generate Meltano documentation
	@echo "📚 Generating Meltano documentation..."
	@mkdir -p docs/generated
	poetry run python -c "
from flext_meltano.project_manager import MeltanoProjectManager
from flext_meltano.orchestrator import MeltanoOrchestrator
import inspect

# Generate documentation
doc = '''# Meltano Integration Documentation

## Project Manager

'''
doc += inspect.getdoc(MeltanoProjectManager) or 'Project lifecycle management'

doc += '''

## Orchestrator

'''
doc += inspect.getdoc(MeltanoOrchestrator) or 'Pipeline orchestration'

with open('docs/generated/meltano.md', 'w') as f:
    f.write(doc)

print('✅ Meltano documentation generated')
"

# Development Workflow
dev-setup: install-dev ## Complete development setup
	@echo "🎯 Setting up Meltano development environment..."
	poetry run pre-commit install
	mkdir -p reports logs data_buffers/locks data_buffers/sync_states
	@echo "🎵 Run 'make project-list' to see available projects"
	@echo "🚀 Run 'make pipeline-test' to test pipeline execution"
	@echo "📦 Run 'make extensions-list' to see available extensions"
	@echo "✅ Development setup complete!"

# Cleanup
clean: ## Clean build artifacts and generated files
	@echo "🧹 Cleaning build artifacts..."
	@rm -rf build/ dist/ *.egg-info/
	@rm -rf reports/ logs/ .coverage htmlcov/
	@rm -rf docs/generated/
	@rm -rf data_buffers/locks/* data_buffers/sync_states/*
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@find . -name "*.pyo" -delete 2>/dev/null || true

# Environment variables
export PYTHONPATH := $(PWD)/src:$(PYTHONPATH)
export MELTANO_PROJECT_ROOT := $(PWD)/projects
export FLEXT_MELTANO_DEV := true
export FLEXT_MELTANO_DEBUG := true