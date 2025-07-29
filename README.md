# FLEXT Meltano - Enterprise Data Integration Library

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://python.org)
[![Poetry](https://img.shields.io/badge/poetry-1.8+-blue.svg)](https://python-poetry.org)
[![Quality Gates](https://img.shields.io/badge/quality-zero%20tolerance-green.svg)](docs/quality-standards.md)
[![Coverage](https://img.shields.io/badge/coverage-90%25%2B-green.svg)](reports/coverage/index.html)

**STATUS**: ✅ **ENTERPRISE LIBRARY** - Production-ready Singer/Meltano/DBT integration

## 🎯 Overview

FLEXT Meltano is a **consolidated Python library** that provides enterprise-grade Singer, Meltano, and DBT integration within the FLEXT ecosystem. Built with Clean Architecture principles and designed for subprocess execution with Go bridge integration.

## 🏗️ Current Architecture

### Core Module Structure

```
src/flext_meltano/
├── __init__.py                      # Comprehensive public interface (249 exports)
├── base.py                          # Base classes and factory functions
├── core.py                          # Core enterprise functionality
├── flext_meltano_cli.py            # CLI interface and commands
├── flext_meltano_discovery.py      # Plugin discovery and catalog management
├── flext_meltano_execution.py      # Subprocess execution helpers
├── flext_meltano_installation.py   # Plugin installation utilities
├── flext_meltano_validation.py     # Pipeline validation helpers
└── flext_singer.py                 # Singer SDK integration
```

### Key Components

- **Execution Layer**: Subprocess-based Meltano CLI execution
- **Bridge Integration**: Go ↔ Python communication via `scripts/flext_meltano_bridge.py`
- **Enterprise Patterns**: Built on flext-core foundation (FlextResult, DI container)
- **Singer/DBT Support**: Full integration with Singer SDK and DBT Core

## 🚀 Quick Start

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

## 🧪 Testing & Validation

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
make test-pipeline           # CSV → CSV pipeline test
make meltano-run JOB=job-name    # Run specific Meltano job
make singer-validate TAP=tap-name    # Validate Singer output
```

## 🏢 FLEXT Ecosystem Integration

### Dependencies

- **flext-core**: Base patterns, FlextResult, dependency injection
- **flext-observability**: Monitoring and metrics (optional)
- **Meltano 3.0+**: ELT orchestration platform
- **Singer SDK 0.44+**: Data extraction/loading protocol
- **DBT Core 1.10.5+**: Data transformation framework

### External Integration Points

```python
# FlexCore Service (Go) → FLEXT Meltano (Python)
# Via HTTP REST API and subprocess execution

# Available operations:
# - Pipeline execution
# - Plugin management
# - Catalog discovery
# - DBT transformations
# - State management
```

## 🚀 Development Commands

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
├── src/flext_meltano/       # Core library modules
├── scripts/                 # Bridge scripts for Go integration
├── tests/                   # Comprehensive test suite (90%+ coverage)
├── docs/                    # Documentation and guides
├── dbt/                     # DBT project configurations
├── examples/                # Usage examples and demos
├── pyproject.toml           # Poetry configuration
├── Makefile                 # Development commands
└── README.md               # This file
```

## 📚 Documentation

- [Architecture Guide](docs/architecture/) - Detailed architectural decisions
- [API Reference](docs/api/) - Complete API documentation
- [Examples](docs/examples/) - Usage examples and patterns
- [Deployment Guide](docs/deployment/) - Production deployment
- [CLAUDE.md](CLAUDE.md) - AI assistant guidance

## 🛡️ Quality Standards

- **Coverage**: 90% minimum test coverage (enforced)
- **Type Safety**: MyPy strict mode with no untyped code
- **Linting**: Ruff with ALL rules enabled (zero tolerance)
- **Security**: Bandit + pip-audit scanning
- **Pre-commit**: Automated quality checks on every commit

## 📊 Current Status

- ✅ **Production Ready**: Enterprise-grade library with comprehensive testing
- ✅ **Go Integration**: Bridge pattern for seamless Go ↔ Python communication
- ✅ **FLEXT Ecosystem**: Full integration with flext-core patterns
- ✅ **Singer Compliance**: Complete Singer SDK and Meltano integration
- ✅ **Quality Assured**: Zero tolerance quality gates enforcement
- ✅ **Type Safe**: Strict MyPy configuration with comprehensive type hints

**Version**: 2.0.0-enterprise
