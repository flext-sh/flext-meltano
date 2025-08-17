# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLEXT Meltano is a **production-ready Python library** that serves as the Go ↔ Python bridge integration component within the FLEXT Enterprise Data Integration Platform. This library enables Go services (FlexCore, FLEXT Service) to orchestrate data pipelines using the Meltano/Singer/DBT ecosystem through enterprise subprocess orchestration.

**Status**: 🚧 **ACTIVE DEVELOPMENT** - Core functionality working, significant quality issues remain

**Architecture**: Consolidated module organization with bridge integration, **~20% test coverage** (target: 90%), MyPy type errors need resolution.

### Position in FLEXT Ecosystem

FLEXT Meltano is a critical component of the **33-project FLEXT ecosystem** (Version 2.0.0), providing data pipeline orchestration capabilities:

- **Parent Ecosystem**: FLEXT Enterprise Data Integration Platform ([../README.md](../README.md))
- **Workspace Documentation**: Complete ecosystem documentation ([../docs/](../docs/))
- **Integration Role**: Bridge between Go services and Python data processing ecosystem

## Architecture

### Core Design Principles

1. **Consolidated Library**: Simplified structure with core modules in src/flext_meltano/
2. **Subprocess-Based**: Direct Meltano CLI execution through subprocess calls
3. **Go Bridge Integration**: Python library callable from Go services via bridge pattern
4. **Enterprise Integration**: Built on flext-core foundation patterns

### Production Library Structure (16 Modules) ✅ Enterprise Ready

```
src/flext_meltano/
├── __init__.py           # ✅ Comprehensive public interface (449+ exports)
├── base.py               # ✅ Base classes and factory functions
├── cli.py                # ✅ CLI interface and command implementations
├── common.py             # ✅ Common utilities and shared functionality
├── common_schemas.py     # ✅ Centralized Singer schema definitions
├── container.py          # ✅ Dependency injection container
├── core.py               # ✅ Core enterprise functionality and services
├── dbt.py                # ✅ DBT integration and project management
├── discovery.py          # ✅ Plugin discovery and catalog management
├── exceptions.py         # ✅ Enterprise exception hierarchy
├── execution.py          # ✅ Subprocess execution helpers and result handling
├── flext_singer.py       # ✅ Singer SDK integration and stream handling
├── installation.py       # ✅ Plugin installation utilities and management
├── simple_bridge.py      # ✅ Go ↔ Python bridge implementation
├── singer.py             # ✅ Core Singer protocol implementation
├── singer_base.py        # ✅ Singer base classes and utilities
├── singer_unified.py     # ✅ Unified Singer interface
└── validation.py         # ✅ Pipeline validation helpers and compliance checks
```

### Bridge Integration ✅ Production Ready

**Complete Go ↔ Python Bridge Implementation:**

- **FlextMeltanoBridge**: Production-ready bridge class with comprehensive functionality
- **scripts/flext_meltano_bridge.py**: Operational CLI script for Go subprocess integration
- **JSON Serialization**: Complete Go-compatible response formatting
- **JSON API**: Returns structured JSON responses for Go service consumption

## Critical Development Notes

### **PRIORITY 1: Quality Gates Must Pass First**

Before any feature development, these must be resolved:

1. **MyPy Type Errors**: 147 errors across 16 files - use `poetry run mypy src --strict` to see details
2. **Test Coverage**: Currently ~20%, target 90% - run `make test` to check current status  
3. **Lint Issues**: 7 errors in test files - run `make lint` to see specifics
4. **Module Architecture**: 36 source files need consolidation

### **Critical Architecture Understanding**

- **Bridge Pattern**: `simple_bridge.py` contains `FlextMeltanoBridge` for Go ↔ Python communication
- **Execution Core**: `execution.py` handles subprocess-based Meltano CLI calls with FlextResult patterns
- **Singer Integration**: `singer_*.py` modules provide tap/target functionality
- **DBT Integration**: `dbt.py` and related modules handle transformation workflows

## Development Commands

### Essential Makefile Commands

```bash
# Quality Gates (pytest config now fixed)
make validate                 # Complete validation (lint + type + security + test)
make check                   # Quick health check (lint + type-check only)
make lint                    # Ruff linting (7 errors to fix)
make type-check              # MyPy strict type checking (147 errors to fix)
make test                    # Run tests with coverage (config fixed)
make security                # Bandit security scanning + pip-audit

# Development Setup
make setup                   # Complete development setup with pre-commit hooks
make install                 # Install dependencies with Poetry
make install-dev             # Install dev dependencies

# Meltano Operations
make meltano-init            # Initialize Meltano project
make meltano-install         # Install Meltano plugins
make meltano-run JOB=job-name    # Run specific pipeline (required JOB parameter)
make meltano-test            # Test Meltano configuration
make meltano-discover TAP=tap-name  # Discover catalog from tap
make meltano-ui              # Start Meltano UI (port 5000)
make test-pipeline           # Run basic CSV test pipeline

# Additional Quality Commands
make format                  # Auto-format code with ruff
make fix                     # Auto-fix linting issues
make coverage-html           # Generate HTML coverage report
make pre-commit              # Run pre-commit hooks

# Build & Distribution
make build                   # Build distribution packages
make clean                   # Remove all artifacts
make clean-all               # Deep clean including venv
make reset                   # Complete reset (clean-all + setup)

# Development Utilities
make shell                   # Open Poetry Python shell
make diagnose                # Project diagnostics
make doctor                  # Complete health check
make deps-update             # Update dependencies
make deps-audit              # Security audit dependencies
```

### Testing Commands

```bash
# Essential testing patterns
make test                    # Full test suite with 90% coverage requirement
make test-unit               # Unit tests only (tests/unit/)
make test-integration        # Integration tests only (tests/integration/)
make test-fast               # Tests without coverage for quick feedback
make coverage-html           # HTML coverage report in reports/coverage/

# Pytest markers (from pyproject.toml)
pytest -m unit               # Unit tests only
pytest -m integration        # Integration tests only
pytest -m e2e                # End-to-end tests only
pytest -m slow               # Slow tests only
pytest -m smoke              # Smoke tests only
pytest -m performance        # Performance tests only

# Specific test execution patterns
pytest tests/test_*.py -v -x                           # Run specific test with fail-fast
pytest tests/ -k "test_execution" -v                   # Run tests matching pattern
pytest tests/ --cov=src/flext_meltano --cov-fail-under=90 # Coverage with enforcement
pytest tests/test_flext_singer.py -v                   # Test Singer integration
pytest tests/test_dbt_integration.py -v                # Test DBT integration
pytest tests/extensions/ -v                            # Extension-specific tests
```

## Core APIs and Usage

### Library Import Pattern

```python
import flext_meltano

# Comprehensive exports available (249+ total):
# - Core execution functions: execute pipeline, run commands
# - Singer SDK re-exports: Stream, Tap, Target, Sink classes
# - DBT integrations and Meltano core components
# - Base classes: FlextMeltanoTap, FlextMeltanoTarget, FlextMeltanoDbt
# - Enterprise patterns: FlextResult, dependency injection
# - Bridge components: FlextMeltanoBridge (from simple_bridge)
```

### Primary APIs

#### Execution API (Subprocess-based)

```python
from flext_meltano.execution import (
    execute_meltano_command,
    run_pipeline,
    FlextMeltanoExecutionResult
)

# Execute Meltano command
result = execute_meltano_command(["--version"])

# Run pipeline between tap and target
result = run_pipeline("tap-csv", "target-csv")

# Check enterprise result pattern
if result.success:
    print(f"Output: {result.data}")
else:
    print(f"Error: {result.error_message}")
```

#### Discovery API

```python
from flext_meltano.discovery import (
    discover_plugins,
    discover_catalog,
    get_plugin_config
)

# Discover available plugins
plugins = discover_plugins()

# Discover schema from tap
catalog = discover_catalog("tap-csv")
```

### Discovery and Installation

```python
from flext_meltano.discovery import (
    FlextMeltanoDiscovery,
    discover_catalog,
    discover_plugins
)
from flext_meltano.installation import (
    FlextMeltanoInstaller,
    install_plugin
)

# Discover available plugins
discovery = FlextMeltanoDiscovery()
plugins = discovery.discover_plugins()

# Install and configure a plugin
installer = FlextMeltanoInstaller()
result = installer.install_plugin("extractor", "tap-csv")
```

### CLI Bridge Usage (Go Integration)

```bash
# Via bridge script (called from Go)
python scripts/flext_meltano_bridge.py version
python scripts/flext_meltano_bridge.py run_pipeline tap-csv target-csv
python scripts/flext_meltano_bridge.py add_plugin extractor tap-csv
```

## 🚧 Development Status (2025-08-17)

**ACTIVE DEVELOPMENT** - Core functionality implemented but quality gates failing.

### Current Implementation Status

1. **✅ FlextMeltanoBridge Implementation**:

   - Complete bridge class implementation in `simple_bridge.py`
   - Functional methods: `get_version()`, `list_plugins()`, `run_pipeline()`
   - JSON API responses for Go service consumption

2. **❌ Type Checking Issues**:

   - **MyPy Status**: ❌ 147 errors across 16 files
   - Type safety issues in core modules need resolution
   - Missing type stubs for duckdb and pandas

3. **✅ Bridge Script Implementation**:

   - JSON response formatting for Go service integration
   - **Bridge Status**: ✅ Functional with JSON API

4. **❌ Test Infrastructure Issues**:

   - **Test Status**: ❌ Pytest configuration conflicts
   - Coverage reporting broken due to duplicate arguments
   - Test coverage at ~20% vs 90% requirement

5. **✅ Module Exports**:
   - Bridge components available in `__init__.py`
   - **Import Status**: ✅ Core imports working

### Current Quality Status (2025-08-17)

```bash
# Quality Gate Status
make check                   # ❌ FAILING (7 lint errors, 147 MyPy errors)
make test                    # ❌ FAILING (pytest config conflicts, ~20% coverage)
make validate                # ❌ FAILING (multiple quality issues)

# Specific Status
Lint Errors: 7              # ❌ ARG002, ANN401 violations in tests
Type Errors: 147            # ❌ Multiple type safety issues across modules
Test Coverage: ~20%         # ❌ Significantly below 90% requirement
Pytest Config: Conflicting  # ❌ Duplicate coverage arguments
```

### Bridge Integration Demo

```bash
# Working bridge commands
python scripts/flext_meltano_bridge.py version
# {"success": true, "data": {"meltano": "3.8.0", "python": "3.13.5", "flext_meltano": "2.0.0-enterprise"}}

python scripts/flext_meltano_bridge.py list_plugins
# {"success": true, "data": [...]}
```

### Next Phase Priorities (CURRENT FOCUS)

1. **🚨 CRITICAL: Quality Gates Completely Failing**: Fix fundamental issues before feature development

   - **Immediate blockers requiring attention**:
   - Test Coverage: ~20% (need 70% improvement to reach 90%)
   - MyPy Errors: 147 type errors across 16 files
   - Pytest Configuration: Conflicting coverage arguments prevent test execution
   - Lint Issues: 7 errors in test files (ARG002, ANN401)
   - Module Architecture: 36 source files with complex interdependencies

2. **✅ Fix Pytest Configuration**: Resolved conflicting coverage arguments
3. **Type Safety Overhaul**: Address 147 MyPy errors across core modules
4. **Test Infrastructure**: Build comprehensive test suite from ~20% to 90% coverage
5. **Architecture Consolidation**: Simplify 36-module structure while maintaining functionality

## Integration Patterns & Architecture

### Core Module Organization

**Base Classes (`base.py`)**:

- `FlextMeltanoConfig`: Configuration management
- `FlextMeltanoTap`, `FlextMeltanoTarget`, `FlextMeltanoDbt`: Base Singer/DBT classes
- Factory functions: `create_tap()`, `create_target()`, `create_dbt_service()`

**Core Services (`core.py`)**:

- `FlextMeltanoOrchestrationService`: Pipeline orchestration
- `FlextMeltanoDbtService`: DBT operations
- `FlextMeltanoSingerService`: Singer protocol handling
- Enterprise patterns with flext-core integration

**Execution Layer**:

- `execution.py`: Subprocess-based Meltano CLI execution with FlextResult patterns
- `cli.py`: CLI interface for direct commands and user interactions
- Bridge scripts for Go integration via `scripts/flext_meltano_bridge.py`

### Singer/Meltano Integration

**Tap/Target Development**:

- Use base classes from `flext_meltano.base`
- Follow Singer SDK patterns with FLEXT result handling
- Examples: `FlextMeltanoTapOracle`, `FlextMeltanoTargetCsv`

**DBT Integration**:

- `FlextMeltanoDbtService` for project management
- Integration with Meltano's DBT execution
- `dbt/` directory contains project configurations

## Testing Strategy

### Test Structure

```
tests/
├── test_*.py                    # Main functionality tests
├── unit/                        # Unit tests
├── integration/                 # Integration tests
├── e2e/                         # End-to-end tests
├── extensions/oracle_oic/       # Extension-specific tests
└── fixtures/                    # Test data and fixtures
```

### Key Test Requirements

- **90% minimum coverage** (enforced by pytest configuration)
- **Bridge integration testing**: Go ↔ Python communication validation
- **Singer protocol compliance**: Tap/target validation
- **Enterprise pattern testing**: flext-core integration tests

### Running Specific Tests

```bash
# Test core functionality
pytest tests/test_flext_meltano_*.py -v
pytest tests/test_basic.py -v
pytest tests/test_models.py -v

# Test specific modules
pytest tests/test_execution_comprehensive.py -v
pytest tests/test_real_dbt_functionality.py -v
pytest tests/test_meltano_integration.py -v

# Extension testing
pytest tests/extensions/oracle_oic/ -v

# Test with coverage reporting
pytest tests/ --cov=src/flext_meltano --cov-report=term-missing --cov-fail-under=90
```

## Configuration and Environment

### Required Environment Variables

```bash
MELTANO_ENVIRONMENT=dev              # Default environment (used by Makefile)
MELTANO_PROJECT_ROOT=$(PWD)          # Project root directory (used by Makefile)
PYTHONPATH=$(PWD)/src:$(PYTHONPATH)  # Python path setup for development
```

### Dependencies & Requirements

#### Core Requirements (from pyproject.toml)

- **Python 3.13** strict requirement (`>=3.13,<3.14`)
- **Meltano 3.0+** (`>=3.0.0,<4.0.0`) for ELT orchestration
- **Singer SDK 0.44+** (`>=0.44.0,<1.0.0`) for data extraction/loading
- **DBT Core 1.10.5** exact version for data transformations
- **flext-core** (local dependency) for enterprise patterns

#### Enterprise Stack

- **Pydantic 2.11+** for configuration and validation
- **FastAPI 0.115+** for API services
- **SQLAlchemy 2.0+** for database operations
- **Structlog 25.1+** for structured logging
- All dependencies locked in `poetry.lock` for reproducible builds

## Quality Standards

### Zero Tolerance Quality Gates

- **Linting**: Ruff with ALL rules enabled
- **Type Checking**: MyPy strict mode with no untyped code
- **Security**: Bandit security scanning
- **Coverage**: 90% minimum test coverage
- **Pre-commit**: Automated quality checks

### Code Style Requirements

- **Python 3.13** with type hints throughout
- **Pydantic** for configuration and validation
- **Async/await** patterns where applicable
- **Clean Architecture** with dependency injection
- **SOLID principles** enforcement

## Current Status & Known Limitations

### Implementation Status

✅ **Production Ready**:

- Core execution layer with subprocess-based Meltano CLI integration
- Singer SDK integration and stream handling (`singer_*.py` modules)
- Enterprise patterns integration with flext-core (`base.py`, `core.py`)
- Plugin discovery and installation (`discovery.py`, `installation.py`)
- Comprehensive validation and error handling (`validation.py`, `exceptions.py`)

⚠️ **Current Blockers**:

1. **🚨 CRITICAL: Quality Gates Not Functional**: All quality checks failing

   - **Test Coverage**: ~20% vs 90% requirement (70% gap)
   - **Type Safety**: 147 MyPy errors requiring resolution
   - **Test Execution**: ✅ Pytest config fixed, can now run tests
   - **Lint Compliance**: 7 lint errors in test files

2. **Quality Gate Infrastructure**: `make test` now functional, others need quality fixes
3. **Production Readiness**: Cannot be released until quality gates pass
4. **Meltano Project**: No `meltano.yml` in repository (initialized on demand)
5. **Architecture Debt**: 36 modules with complex interdependencies need consolidation

### Current Architecture Benefits

- **Simplified Structure**: Consolidated from complex hierarchy to flat module organization
- **Enterprise Integration**: Built on flext-core patterns (FlextResult, dependency injection)
- **Type Safety**: ❌ 147 MyPy errors across 16 files
- **Bridge Pattern**: ✅ Functional Go service integration via `scripts/flext_meltano_bridge.py`
- **Core Functionality**: ✅ All critical features operational

## Integration Points

### FLEXT Ecosystem Integration

- **flext-core**: Base patterns, result handling, dependency injection
- **FlexCore Service**: Go service integration via bridge pattern
- **FLEXT Service**: Python bridge execution for Meltano operations

### External Dependencies

- **Meltano**: ELT orchestration platform (3.0+)
- **Singer SDK**: Data extraction/loading protocol (0.44+)
- **DBT Core**: Data transformation framework (1.10.5+)
- **Pydantic**: Configuration and validation (2.11+)

## Common Workflows

### Adding New Tap/Target

1. Create implementation in `taps/` or `targets/`
2. Use existing patterns from `taps/oracle/` as template
3. Add comprehensive tests with Singer protocol validation
4. Register with Meltano via `make meltano-add-extractor` or `make meltano-add-loader`

### Testing Pipeline End-to-End

1. Run `make test-pipeline` for basic CSV validation
2. Use `make meltano-run JOB=job-name` for specific jobs
3. Check execution logs and output validation
4. Verify state management and incremental processing

### Go Bridge Development

1. Modify `FlextMeltanoBridge` class for new operations
2. Update `flext_meltano_bridge.py` CLI interface
3. Test bridge communication with result validation
4. Ensure JSON serialization compatibility

## Development Best Practices

### Code Organization & Standards

1. **Always run quality gates** before committing: `make validate`
2. **Follow consolidated structure**: Use the current flat module organization in src/flext_meltano/
3. **Enterprise integration**: Build on flext-core patterns (FlextResult, dependency injection)
4. **Type safety**: Follow strict MyPy configuration with comprehensive type hints
5. **Subprocess pattern**: Use execution module for all Meltano CLI interactions with proper FlextResult handling

### Testing Requirements

6. **90% coverage minimum**: All code must meet coverage requirements
7. **Test bridge integration**: Validate Go ↔ Python communication when modifying core
8. **Comprehensive test coverage**: Include unit, integration, and e2e tests
9. **Use pytest markers**: Utilize markers for test organization (unit, integration, e2e, slow)

### Integration Guidelines

10. **Bridge pattern**: Maintain Go integration via scripts/flext_meltano_bridge.py
11. **Singer compliance**: Follow Singer SDK patterns for tap/target development
12. **DBT integration**: Use FlextMeltanoDbtService for project management
13. **Configuration management**: Document environment variables and Meltano settings
14. **Error handling**: Use FlextResult pattern from flext-core for consistent error handling

### Quality Enforcement

15. **Ruff linting**: ALL rules enabled - zero tolerance for style violations
16. **Security scanning**: Bandit + pip-audit required for all changes
17. **Pre-commit hooks**: Automated quality checks on every commit
18. **Documentation**: Keep CLAUDE.md updated with architectural changes
