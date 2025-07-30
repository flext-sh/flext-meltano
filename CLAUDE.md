# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLEXT Meltano is a consolidated Python library that provides Singer, Meltano, and DBT integration within the FLEXT ecosystem. This is a **library project**, not a service, designed for subprocess execution and Go bridge integration.

**Status**: ✅ **FUNCTIONAL LIBRARY** - Recently reorganized with simplified, flat module architecture.

**Current Architecture**: Consolidated from complex hierarchical structure to flat module organization in `src/flext_meltano/` with comprehensive test coverage and quality gates.

## Architecture

### Core Design Principles

1. **Consolidated Library**: Simplified structure with core modules in src/flext_meltano/
2. **Subprocess-Based**: Direct Meltano CLI execution through subprocess calls
3. **Go Bridge Integration**: Python library callable from Go services via bridge pattern
4. **Enterprise Integration**: Built on flext-core foundation patterns

### Current Library Structure

```
flext_meltano/
├── __init__.py          # Comprehensive public interface (DBT, Meltano, Singer exports)
├── base.py              # Base classes and factory functions with enterprise patterns
├── cli.py               # CLI interface and command implementations
├── common.py            # Common utilities and shared functionality
├── core.py              # Core enterprise functionality and services
├── dbt.py               # DBT integration and project management
├── discovery.py         # Plugin discovery and catalog management
├── execution.py         # Subprocess execution helpers and result handling
├── flext_singer.py      # Singer SDK integration and stream handling
├── installation.py      # Plugin installation utilities and management
├── singer.py            # Core Singer protocol implementation
└── validation.py        # Pipeline validation helpers and compliance checks
```

#### Bridge Integration Pattern

- **FlextMeltanoBridge**: Available via simple_bridge import (referenced in cache)
- **scripts/flext_meltano_bridge.py**: CLI script for Go subprocess calls
- **FlextMeltanoResult**: Local result type from flext_meltano_execution

## Development Commands

### Essential Makefile Commands

````bash

## TODO: GAPS DE ARQUITETURA IDENTIFICADOS - PRIORIDADE CRÍTICA

### 🚨 GAP 1: Go Bridge Integration Incomplete
**Status**: CRÍTICO - Bridge pattern implementado mas integration não completa
**Problema**:
- FlextMeltanoBridge available mas Go-Python communication não documented
- Bridge script em scripts/ mas integration patterns não specified
- FLEXT Service (Go/Python) integration não completa

**TODO**:
- [ ] Documentar complete Go-Python bridge patterns
- [ ] Implementar standardized bridge communication protocols
- [ ] Criar bridge testing patterns
- [ ] Integrar bridge com FLEXT Service architecture

### 🚨 GAP 2: Singer Projects Integration Gap
**Status**: CRÍTICO - Meltano não conectado com Singer ecosystem projects
**Problema**:
- 15 Singer projects (taps, targets, dbt) não integrated com Meltano library
- Plugin discovery não finds FLEXT Singer projects
- Meltano project configuration não generates from ecosystem

**TODO**:
- [ ] Integrar discovery com all FLEXT Singer projects
- [ ] Auto-generate meltano.yml from ecosystem structure
- [ ] Implement Singer project registration patterns
- [ ] Create unified Singer-Meltano workflow

### 🚨 GAP 3: CLI Integration Missing
**Status**: ALTO - Meltano operations não available via flext-cli
**Problema**:
- Subprocess execution não integrated with CLI
- Meltano commands não accessible via ecosystem CLI
- Pipeline management não integrated with CLI workflow

**TODO**:
- [ ] Integrar Meltano commands com flext-cli
- [ ] Criar meltano command group em flext-cli
- [ ] Implement pipeline management via CLI
- [ ] Document Meltano CLI usage patterns

```bash
# Quality Gates (MUST pass before committing)
make validate                 # Complete validation (lint + type + security + test)
make check                   # Quick health check (lint + type + test)
make lint                    # Ruff linting (ALL rules enabled)
make type-check              # MyPy strict type checking
make test                    # Run tests with 90% coverage minimum

# Development Setup
make setup                   # Complete development setup
make install                 # Install dependencies with Poetry
make dev-install             # Development environment setup with pre-commit

# Meltano Operations
make meltano-init            # Initialize Meltano project
make meltano-install         # Install Meltano plugins
make meltano-run JOB=job-name    # Run specific pipeline
make meltano-test            # Test Meltano configuration
make test-pipeline           # Run basic CSV test pipeline

# Build & Distribution
make build                   # Build distribution packages
make clean                   # Remove all artifacts
````

### Testing Commands

```bash
# Essential testing patterns
make test                    # Full test suite with 90% coverage requirement
make test-unit               # Unit tests only (tests/unit/)
make test-integration        # Integration tests only (tests/integration/)
make test-meltano           # Meltano-specific tests
make coverage               # Detailed coverage report with HTML output

# Specific test execution patterns
pytest tests/test_*.py -v -x                           # Run specific test with fail-fast
pytest tests/ -k "test_execution" -v                   # Run tests matching pattern
pytest tests/ --cov=src/flext_meltano --cov-fail-under=90 # Coverage with enforcement
```

## Core APIs and Usage

### Library Import Pattern

```python
import flext_meltano

# Comprehensive exports available (249 total):
# - FlextMeltanoBridge: Go integration bridge
# - FlextMeltanoResult: Result handling
# - flext_meltano_execute_job: Job execution
# - flext_meltano_run_command: Generic commands
# - Base classes: FlextMeltanoTap, FlextMeltanoTarget, FlextMeltanoDbt
# - Core services: FlextMeltanoOrchestrationService, FlextMeltanoDbtService
# - Singer SDK re-exports (Stream, Tap, Target, etc.)
# - DBT integrations and Meltano core components
```

### Execution Helpers (Primary API)

```python
from flext_meltano.execution import (
    FlextMeltanoExecutor,
    FlextMeltanoResult
)

# Create executor instance
executor = FlextMeltanoExecutor()

# Execute pipeline job
result = executor.run_pipeline("tap-csv", "target-csv")

# Run generic Meltano command
result = executor.run_command(["--version"])

# Check result status
if result.success:
    print(result.output)
else:
    print(f"Error: {result.error}")
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
MELTANO_ENVIRONMENT=dev              # Default environment
MELTANO_PROJECT_ROOT=$(PWD)          # Project root directory
PYTHONPATH=$(PWD)/src:$(PYTHONPATH)  # Python path setup
```

### Poetry Configuration

- **Python 3.13** strict requirement
- **Meltano 3.0+** with Singer SDK
- **DBT Core 1.10.5** for transformations
- All dependencies locked in `poetry.lock`

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

## Known Limitations & Status

1. **target-jsonl**: Incompatible with Python 3.13 (pytz syntax error)
2. **DBT Integration**: Core functionality available with `dbt.py` module but not fully tested end-to-end
3. **Testing Scope**: Primarily tested with CSV pipelines (other formats require validation)
4. **Meltano Project**: No `meltano.yml` in repository (initialized on demand via `make meltano-init`)
5. **Architecture Migration**: Recently consolidated from complex structure - some legacy imports may exist

### Current Implementation Status

✅ **Completed**: Core execution, discovery, installation, validation modules  
✅ **Completed**: Singer SDK integration and stream handling  
✅ **Completed**: Enterprise patterns integration with flext-core  
⚠️ **In Progress**: DBT end-to-end testing and validation  
⚠️ **In Progress**: Complete bridge testing for all Go integration scenarios

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
