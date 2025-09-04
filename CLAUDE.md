# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Essential Quality Gates
```bash
# Complete validation pipeline (MANDATORY before commits)
make validate                 # Runs: lint + type-check + security + test

# Quick health checks
make check                    # Quick: lint + type-check only
make lint                     # Ruff linting with strict rules
make type-check              # MyPy strict mode type checking
make test                    # Full test suite with coverage
make format                  # Auto-format code with Ruff

# Quality status shortcuts
make l                       # Alias for lint
make t                       # Alias for test  
make tc                      # Alias for type-check
make v                       # Alias for validate
```

### Meltano-Specific Operations
```bash
# Meltano project management
make meltano-init            # Initialize Meltano project (creates meltano.yml)
make meltano-install         # Install plugins from meltano.yml
make meltano-test            # Test Meltano configuration

# Pipeline operations
make meltano-run JOB=job     # Run specific pipeline job
make test-pipeline           # Run basic CSV test pipeline
make meltano-discover TAP=tap-name  # Discover catalog from tap

# Plugin discovery and validation
make singer-validate TAP=tap-name   # Validate Singer tap output
```

### Testing Commands
```bash
# Test execution patterns
make test                    # Full test suite with 90% coverage requirement
make test-fast              # Tests without coverage (faster)
make test-unit              # Unit tests only
make test-integration       # Integration tests only
make test-meltano           # Meltano-specific tests only
make coverage-html          # Generate HTML coverage report
```

## Architecture Overview

### High-Level Structure

This is a **Level 3** library in the FLEXT ecosystem hierarchy:

```
LEVEL 4: flext-tap-*, flext-target-*, flext-dbt-* (consumers)
LEVEL 3: [THIS PROJECT] flext-meltano (technological base)
LEVEL 2: flext-cli, flext-observability (intermediate services)
LEVEL 1: flext-core (abstract foundation)
```

**Core Architecture Principles:**
- **Railway-Oriented Programming**: All operations return `FlextResult[T]`
- **SOLID Principles**: Single responsibility, dependency inversion
- **Real API Integration**: 100% real Meltano/Singer/DBT APIs, zero mocks
- **Type Safety**: Python 3.13+ with MyPy strict mode

### Module Organization

**Foundation Layer:**
- `constants.py` - Meltano-specific constants extending FlextConstants
- `typings.py` - Type definitions and aliases  
- `exceptions.py` - Exception hierarchy for Meltano operations

**Service Layer:**
- `services.py` - Core service implementations (TapService, TargetService, DbtService)
- `adapters.py` - Meltano Core API integration with project management

**Execution Layer:**
- `executors.py` - CLI command processing and execution
- `executors_bridge.py` - Go ↔ Python bridge communication
- `executors_cli.py` - CLI-specific command implementations

**Integration Layer:**
- `singer_types.py` - Singer Protocol type abstractions
- `tap_abstractions.py` - Tap service abstractions  
- `target_abstractions.py` - Target service abstractions

**Support Layer:**
- `config.py` - Configuration management
- `utilities.py` - Utility functions and helpers
- `validators.py` - Validation functions extending FlextUtilities
- `file_managers.py` - File and directory management
- `config_builders.py` - Configuration builders

### Bridge Communication Architecture

The project provides Go ↔ Python interoperability:

```bash
# Bridge operations (JSON API)
python scripts/flext_meltano_bridge.py version
python scripts/flext_meltano_bridge.py list_plugins
python scripts/flext_meltano_bridge.py run_pipeline tap-csv target-csv
```

## Import Rules

### Mandatory Import Patterns

**✅ CORRECT - Root module imports only:**
```python
from flext_meltano import FlextMeltanoAdapter, FlextMeltanoService
from flext_core import FlextResult, FlextServiceProcessor, FlextLogger
from flext_cli import CLICommand, FlextCliApi
```

**❌ PROHIBITED - Internal module imports:**
```python
# Never import from internal modules - violates architectural boundaries
from flext_meltano.adapters import FlextMeltanoAdapter  # WRONG
from flext_core.internal.services import Service        # WRONG  
```

### Dependency Constraints

**Allowed dependencies (Level 1-2 only):**
- `flext-core` - Foundation patterns, FlextResult, service base classes
- `flext-cli` - CLI patterns and command processing  
- `flext-api` - API client patterns
- External: `meltano>=3.0.0`, `singer-sdk>=0.44.0`, `dbt-core>=1.10.5`

**Prohibited dependencies:**
- Same level (other Level 3) or higher level modules
- Direct subprocess calls (use native APIs)
- Mock libraries in production code (tests use real APIs)

## Code Quality Standards

### Type Safety Requirements
- **MyPy Strict Mode**: All source code must pass `mypy src --strict`
- **Python 3.13+**: Use modern Python features and type annotations
- **Generic Types**: Proper generic type annotations with constraints
- **FlextResult Pattern**: All business operations return `FlextResult[T]`

### Linting Standards
- **Ruff**: All rules enabled, zero tolerance for violations
- **Complexity Limits**: Functions with complexity >10 require refactoring
- **Parameter Limits**: Functions with >5 parameters need restructuring  
- **Return Statements**: Functions with >3 returns need simplification

### Testing Philosophy
- **Real API Integration**: 100% real Meltano/Singer/DBT APIs
- **No Mocks**: Tests validate actual functionality, not mocked interfaces
- **Coverage Target**: 90% minimum coverage with meaningful tests
- **Test Categories**: Unit, integration, Meltano-specific markers available

## Development Workflow

### Before Making Changes
1. **Check Current Status**: `make check` to verify current quality gates
2. **Understand Architecture**: Review module dependencies and patterns
3. **Run Target Tests**: `make test-fast` to verify functionality works

### During Development
1. **Follow FlextResult Pattern**: All operations return `FlextResult[T]`
2. **Use Real APIs**: Integrate with actual Meltano/Singer/DBT APIs
3. **Maintain Type Safety**: Add proper type annotations
4. **Check Quality Incrementally**: Run `make lint` frequently

### Before Committing  
1. **Complete Validation**: `make validate` must pass 100%
2. **Test Coverage**: Maintain or improve coverage percentage
3. **Architecture Compliance**: No internal imports, follow SOLID principles
4. **Documentation**: Update README.md if public API changes

## Environment Setup

### Required Environment Variables
```bash
export MELTANO_ENVIRONMENT=dev
export MELTANO_PROJECT_ROOT=$(PWD)  
export PYTHONPATH=$(PWD)/src:$(PYTHONPATH)
```

### Virtual Environment
```bash
# Use FLEXT workspace virtual environment
cd /path/to/flext
source .venv/bin/activate
cd flext-meltano
make install-dev
```

### Key Files for Understanding
- `src/flext_meltano/__init__.py` - Module structure and export aggregation
- `src/flext_meltano/services.py` - Core service implementations  
- `src/flext_meltano/adapters.py` - Meltano integration patterns
- `src/flext_meltano/executors.py` - Command execution patterns
- `tests/test_*_complete.py` - Comprehensive real API tests

This project follows enterprise-grade development standards with strict quality gates and real API integration testing. All code must pass validation before integration.