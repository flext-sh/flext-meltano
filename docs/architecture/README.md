# FLEXT Meltano Architecture

This document provides a comprehensive overview of the FLEXT Meltano library architecture after the recent consolidation and reorganization.

## 🏗️ Architectural Overview

FLEXT Meltano is a **consolidated Python library** that provides enterprise-grade Singer, Meltano, and DBT integration within the FLEXT ecosystem. The architecture follows Clean Architecture principles with a simplified, flat module organization.

### Core Design Principles

1. **Consolidated Structure**: Simplified flat module organization in `src/flext_meltano/`
2. **Enterprise Integration**: Built on flext-core foundation patterns
3. **Subprocess-Based Execution**: Direct Meltano CLI execution through subprocess calls
4. **Go Bridge Pattern**: Python library callable from Go services via bridge interface
5. **Zero Tolerance Quality**: Comprehensive testing and quality gates

## 📦 Module Architecture

### Current Structure

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

### Module Responsibilities

#### `__init__.py` - Public Interface

- **249 exports** providing comprehensive API surface
- Base classes, core services, and utility functions
- Singer SDK re-exports (Stream, Tap, Target, etc.)
- DBT integration components
- Legacy compatibility aliases

#### `base.py` - Foundation Classes

- `FlextMeltanoConfig`: Configuration management
- `FlextMeltanoTap`, `FlextMeltanoTarget`, `FlextMeltanoDbt`: Base Singer/DBT classes
- Factory functions: `create_tap()`, `create_target()`, `create_dbt_service()`
- Enterprise pattern implementations

#### `core.py` - Enterprise Services

- `FlextMeltanoOrchestrationService`: Pipeline orchestration
- `FlextMeltanoDbtService`: DBT operations and project management
- `FlextMeltanoSingerService`: Singer protocol handling
- Enterprise patterns with flext-core integration
- Domain-driven design components

#### `flext_meltano_execution.py` - Execution Layer

- `flext_meltano_execute_job()`: Primary pipeline execution function
- `flext_meltano_run_command()`: Generic Meltano command execution
- `FlextMeltanoResult`: Result handling with success/error states
- Subprocess-based Meltano CLI integration

#### `flext_meltano_cli.py` - CLI Interface

- `FlextMeltanoCli`: CLI command wrapper
- `flext_meltano_run_cli()`: Direct CLI execution
- Command parsing and argument handling

#### `flext_meltano_discovery.py` - Plugin Discovery

- `flext_meltano_discover_catalog()`: Schema discovery
- `flext_meltano_discover_plugins()`: Available plugin enumeration
- Catalog management and metadata handling

#### `flext_meltano_installation.py` - Plugin Management

- `FlextMeltanoInstaller`: Plugin installation service
- `flext_meltano_install_plugin()`: Plugin installation function
- Configuration and dependency management

#### `flext_meltano_validation.py` - Validation Layer

- `flext_meltano_validate_project()`: Project validation
- `flext_meltano_validate_tap_config()`: Tap configuration validation
- `flext_meltano_test_tap_connection()`: Connection testing
- Pipeline validation and health checks

#### `flext_singer.py` - Singer Integration

- Singer SDK integration and protocol handling
- Stream and schema management
- Singer-specific utilities and helpers

## 🌉 Bridge Integration Architecture

### Go ↔ Python Communication

```
┌─────────────────┐    HTTP/JSON    ┌─────────────────────┐
│   FlexCore      │◄──────────────► │   FLEXT Service     │
│   (Go - 8080)   │                 │   (Go/Python - 8081)│
└─────────────────┘                 └─────────────────────┘
                                              │
                                    subprocess│
                                              ▼
                                    ┌─────────────────────┐
                                    │  flext_meltano      │
                                    │  bridge script      │
                                    │  (Python)           │
                                    └─────────────────────┘
                                              │
                                    library   │ import
                                              ▼
                                    ┌─────────────────────┐
                                    │  FLEXT Meltano      │
                                    │  Library            │
                                    │  (Python)           │
                                    └─────────────────────┘
```

### Bridge Components

1. **FlexCore Service** (Go): Runtime container service
2. **FLEXT Service** (Go/Python): Data processing service with Python bridge
3. **Bridge Script** (`scripts/flext_meltano_bridge.py`): CLI interface for Go integration
4. **FLEXT Meltano Library**: Core Python library with enterprise functionality

## 🏢 Enterprise Integration

### FLEXT Ecosystem Integration

- **flext-core**: Base patterns, FlextResult, dependency injection container
- **flext-observability**: Monitoring, metrics, health checks (optional)
- **FlexCore Service**: Go service integration via bridge pattern
- **FLEXT Service**: Python bridge execution for Meltano operations

### External Dependencies

- **Meltano 3.0+**: ELT orchestration platform
- **Singer SDK 0.44+**: Data extraction/loading protocol
- **DBT Core 1.10.5+**: Data transformation framework
- **Pydantic 2.11+**: Configuration and validation

## 📊 Data Flow Architecture

### Pipeline Execution Flow

```
1. Go Service Request
   ↓
2. Bridge Script Invocation
   ↓
3. Library Function Call
   ↓
4. Subprocess Meltano CLI
   ↓
5. Singer/DBT Execution
   ↓
6. Result Processing
   ↓
7. JSON Response to Go
```

### Key Data Structures

- **FlextMeltanoResult**: Success/error state with output/error details
- **FlextMeltanoConfig**: Configuration management with validation
- **FlextMeltanoPipelineEvent**: Event-driven pipeline state
- **FlextMeltanoExecutionState**: Pipeline execution tracking

## 🔧 Configuration Architecture

### Environment Variables

```bash
MELTANO_PROJECT_ROOT=$(PWD)          # Project root directory
MELTANO_ENVIRONMENT=dev              # Default environment
PYTHONPATH=$(PWD)/src:$(PYTHONPATH)  # Python path setup
```

### Configuration Layers

1. **Environment Variables**: Runtime configuration
2. **Meltano Project**: `meltano.yml` configuration (initialized on demand)
3. **Poetry Configuration**: `pyproject.toml` dependencies and settings
4. **FLEXT Configuration**: Enterprise patterns and quality gates

## 🧪 Testing Architecture

### Test Organization

```
tests/
├── test_*.py                    # Main functionality tests
├── unit/                        # Unit tests with mocks
├── integration/                 # Integration tests with real dependencies
├── e2e/                         # End-to-end pipeline tests
├── extensions/oracle_oic/       # Extension-specific tests
└── fixtures/                    # Test data and configuration
```

### Quality Gates

- **90% Coverage**: Enforced by pytest configuration
- **Type Safety**: MyPy strict mode with comprehensive type hints
- **Linting**: Ruff with ALL rules enabled
- **Security**: Bandit + pip-audit scanning
- **Pre-commit**: Automated quality checks

## 🚀 Deployment Architecture

### Library Distribution

- **Poetry Build**: Standard Python package distribution
- **Docker Integration**: Container-based deployment support
- **Go Service Integration**: Bridge pattern for Go service consumption

### Production Considerations

- **Error Handling**: FlextResult pattern for consistent error management
- **Logging**: Structured logging with correlation IDs
- **Monitoring**: Integration with FLEXT observability stack
- **Security**: Enterprise security patterns and vulnerability scanning

---

_Architecture Document - Version 2.0.0-enterprise_
_Last Updated: 2025-01-29_
