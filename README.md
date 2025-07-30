# FLEXT Meltano - Enterprise Data Integration Library

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://python.org)
[![Poetry](https://img.shields.io/badge/poetry-1.8+-blue.svg)](https://python-poetry.org)
[![Quality Gates](https://img.shields.io/badge/quality-zero%20tolerance-green.svg)](docs/quality-standards.md)
[![Coverage](https://img.shields.io/badge/coverage-90%25%2B-green.svg)](reports/coverage/index.html)

**STATUS**: â **ENTERPRISE LIBRARY** - Production-ready Singer/Meltano/DBT orchestration platform

## ð¯ Overview

FLEXT Meltano is a **consolidated Python library** that provides enterprise-grade Singer, Meltano, and DBT integration within the FLEXT ecosystem. Built with Clean Architecture principles and designed for subprocess execution with Go bridge integration.

## ðï¸ Current Architecture

### Core Module Structure

```
src/flext_meltano/
â"â"â" __init__.py                      # Comprehensive public interface (249 exports)
â"â"â" base.py                          # Base classes and factory functions
â"â"â" core.py                          # Core enterprise functionality
â"â"â" flext_meltano_cli.py            # CLI interface and commands
â"â"â" flext_meltano_discovery.py      # Plugin discovery and catalog management
â"â"â" flext_meltano_execution.py      # Subprocess execution helpers
â"â"â" flext_meltano_installation.py   # Plugin installation utilities
â"â"â" flext_meltano_validation.py     # Pipeline validation helpers
â""â"â" flext_singer.py                 # Singer SDK integration
```

### Key Components

- **Execution Layer**: Subprocess-based Meltano CLI execution
- **Bridge Integration**: Go â" Python communication via `scripts/flext_meltano_bridge.py`
- **Enterprise Patterns**: Built on flext-core foundation (FlextResult, DI container)
- **Singer/DBT Support**: Full integration with Singer SDK and DBT Core

## ð Quick Start

### Installation

```bash
# Development setup
make setup                    # Complete development environment
make install                  # Install dependencies with Poetry
make validate                 # Run all quality gates
```

### Basic Usage

```python
import flext_meltano

# Execute Meltano pipeline
from flext_meltano.flext_meltano_execution import flext_meltano_execute_job
result = flext_meltano_execute_job("tap-csv", "target-csv")

# Check result
if result.success:
    print(f"Pipeline completed: {result.output}")
else:
    print(f"Pipeline failed: {result.error}")
```

### Bridge Integration (Go Services)

```bash
# Via bridge script (called from Go)
python scripts/flext_meltano_bridge.py version
python scripts/flext_meltano_bridge.py run_pipeline tap-csv target-csv
python scripts/flext_meltano_bridge.py add_plugin extractor tap-csv
```

## ð§ª Testing & Validation

### Quality Gates

```bash
# Zero tolerance quality enforcement
make validate                 # Complete validation (lint + type + security + test)
make check                   # Essential quality checks (pre-commit standard)
make lint                    # Ruff linting (ALL rules enabled)
make type-check              # MyPy strict mode type checking
make test                    # Run tests with 90% coverage minimum
```

### Test Organization

```bash
# Test specific functionality
pytest tests/test_flext_meltano_*.py -v    # Core functionality
pytest tests/test_helpers_execution.py -v  # Execution helpers
pytest tests/extensions/oracle_oic/ -v     # Extension-specific tests

# Test categories
pytest -m unit               # Unit tests only
pytest -m integration        # Integration tests only
pytest -m e2e                # End-to-end tests only
```

### Pipeline Testing

```bash
# Test basic ELT pipeline
make test-pipeline           # CSV â' CSV pipeline test
make meltano-run JOB=job-name    # Run specific Meltano job
make singer-validate TAP=tap-name    # Validate Singer output
```

## ð¢ FLEXT Ecosystem Integration

### Dependencies

- **flext-core**: Base patterns, FlextResult, dependency injection
- **flext-observability**: Monitoring and metrics (optional)
- **Meltano 3.0+**: ELT orchestration platform
- **Singer SDK 0.44+**: Data extraction/loading protocol
- **DBT Core 1.10.5+**: Data transformation framework

### External Integration Points

```python
# FlexCore Service (Go) â' FLEXT Meltano (Python)
# Via HTTP REST API and subprocess execution

# Available operations:
# - Pipeline execution
# - Plugin management
# - Catalog discovery
# - DBT transformations
# - State management
```

## ð Development Commands

### Essential Operations

```bash
# Complete development setup
make setup                   # Install tools, dependencies, pre-commit hooks
make dev-install             # Development environment setup

# Quality gates (run before committing)
make validate                # ALL quality gates must pass
make format                  # Auto-format code
make security                # Security scans (bandit + pip-audit)

# Meltano operations
make meltano-init            # Initialize Meltano project
make meltano-install         # Install Meltano plugins
make meltano-add-extractor NAME=tap-csv    # Add extractor
make meltano-add-loader NAME=target-csv    # Add loader
```

### Project Structure

```
flext-meltano/
â"â"â" src/flext_meltano/       # Core library modules
â"â"â" scripts/                 # Bridge scripts for Go integration
â"â"â" tests/                   # Comprehensive test suite (90%+ coverage)
â"â"â" docs/                    # Documentation and guides
â"â"â" dbt/                     # DBT project configurations
â"â"â" examples/                # Usage examples and demos
â"â"â" pyproject.toml           # Poetry configuration
â"â"â" Makefile                 # Development commands
â""â"â" README.md               # This file
```

## ð" Documentation

- [Architecture Guide](docs/architecture/) - Detailed architectural decisions
- [API Reference](docs/api/) - Complete API documentation
- [Examples](docs/examples/) - Usage examples and patterns
- [Deployment Guide](docs/deployment/) - Production deployment
- [CLAUDE.md](CLAUDE.md) - AI assistant guidance

## ð¡ï¸ Quality Standards

- **Coverage**: 90% minimum test coverage (enforced)
- **Type Safety**: MyPy strict mode with no untyped code
- **Linting**: Ruff with ALL rules enabled (zero tolerance)
- **Security**: Bandit + pip-audit scanning
- **Pre-commit**: Automated quality checks on every commit

## ð" Current Status

- â **Production Ready**: Enterprise-grade library with comprehensive testing
- â **Go Integration**: Bridge pattern for seamless Go â" Python communication
- â **FLEXT Ecosystem**: Full integration with flext-core patterns
- â **Singer Compliance**: Complete Singer SDK and Meltano integration
- â **Quality Assured**: Zero tolerance quality gates enforcement
- â **Type Safe**: Strict MyPy configuration with comprehensive type hints

**Version**: 2.0.0-enterprise
