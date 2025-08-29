# flext-meltano - Enterprise Data Integration Library

**Version**: 0.9.0-dev | **Status**: ARCHITECTURAL REFACTORING | **Updated**: 2025-08-23

Enterprise Python library providing native integration with Meltano, Singer SDK, and DBT ecosystem for the FLEXT Enterprise Data Integration Platform. Serves as the technological foundation for data pipeline orchestration and processing.

> **Current Status**: Active architectural refactoring to implement SOLID principles and eliminate code duplication. Core functionality validated with 35% test coverage using 100% real APIs. Quality gates require resolution before production readiness.

## Position in FLEXT Ecosystem

**Architecture Level**: Level 3 - Technological Base

```
┌─────────────────────────────────────────────────────────────────────┐
│ LEVEL 4 - MELTANO PLUGINS                                          │
│ 🔌 flext-tap-*, flext-target-*, flext-dbt-* (import from this)     │
├─────────────────────────────────────────────────────────────────────┤
│ LEVEL 3 - TECHNOLOGICAL BASES                                      │
│ 🛠️ [FLEXT-MELTANO] ← THIS PROJECT                                 │
│ ✅ Imports: flext-core (Level 1), flext-cli (Level 2)             │
│ ❌ Cannot import: Same level or higher components                  │
├─────────────────────────────────────────────────────────────────────┤
│ LEVEL 2 - INTERMEDIATE SERVICES                                    │
│ ⚙️ flext-cli, flext-observability, flext-grpc                     │
├─────────────────────────────────────────────────────────────────────┤
│ LEVEL 1 - ABSTRACT FOUNDATION                                      │
│ 🏗️ flext-core (provides FlextResult, DI, service patterns)       │
└─────────────────────────────────────────────────────────────────────┘
```

### Core Responsibilities

1. **Data Pipeline Orchestration**: Native integration with Meltano 3.9.1 ecosystem
2. **Singer Protocol Support**: Complete tap/target/transformation workflow management
3. **DBT Integration**: Data transformation project lifecycle management
4. **Go Bridge Communication**: Python ↔ Go service interoperability via JSON API

## Quick Start

### Installation & Setup

```bash
# Use FLEXT workspace virtual environment
cd /path/to/flext
source .venv/bin/activate
cd flext-meltano

# Install dependencies
make install-dev

# Check current status
make check
```

### Basic Usage

```python
# Import from root module (mandatory pattern)
from flext_meltano import FlextMeltanoConfig, execute_meltano_command
from flext_core import FlextResult

# Execute Meltano operations with FlextResult pattern
result = execute_meltano_command(["--version"])
if result.success:
    print(f"Meltano version: {result.data}")
else:
    print(f"Error: {result.error}")
```

## Current Status (2025-08-23)

### ✅ Validated Functionality

- **Core APIs**: Native Meltano 3.9.1, Singer SDK 0.48.0, DBT Core 1.10.5 integration
- **Bridge Communication**: Go ↔ Python JSON API working via `scripts/flext_meltano_bridge.py`
- **Test Coverage**: 35% with 116 tests using 100% real APIs (zero mocks)
- **Data Processing**: Complete ELT pipeline functionality validated
- **Dependencies**: Poetry configuration with correct version constraints

### 🚨 Critical Issues Requiring Resolution

- **Quality Gates**: MyPy 7 errors, Ruff 11 errors preventing compilation
- **Architecture**: Massive SOLID violations requiring complete reorganization
- **Import Dependencies**: Missing FlextDomainService imports breaking test execution
- **Code Duplication**: Significant duplication of flext-core functionality
- **PEP8 Compliance**: Non-standard naming conventions throughout codebase

### 📊 Quality Metrics

```bash
# Current Status (2025-08-23)
Lint Errors: 11/0           # PLR0911, FBT001, E721, F821 violations
Type Errors: 7/0            # FlextDomainService undefined, explicit object issues
Test Coverage: 35%/100%     # 116 real API tests, systematic improvement needed
Architecture: Major Violations/SOLID Clean  # Complete reorganization required
```

## Architecture & Design

### Service Implementation Pattern

```python
# Target architecture (after refactoring)
from flext_meltano import FlextMeltanoTapService
from flext_core import FlextResult
from singer_sdk import Tap

class MyTapService(FlextMeltanoTapService):
    def __init__(self) -> None:
        super().__init__(tap_name="my-tap")

    def get_tap_class(self) -> type[Tap]:
        return MyCustomTap

    def get_default_config(self) -> dict[str, object]:
        return {"api_key": "required"}

# Usage with dependency injection
service = MyTapService()
result = service.run_with_metrics("tap_processing", {"api_key": "test"})
```

### Import Rules (Mandatory)

```python
# ✅ CORRECT: Root module imports only
from flext_core import FlextResult, FlextServiceProcessor, FlextLogger
from flext_cli import CLICommand, FlextCliApi
from flext_meltano import FlextMeltanoConfig, execute_meltano_command

# ❌ PROHIBITED: Internal module imports (architectural violation)
from flext_meltano.base_services import FlextMeltanoTapService  # Use root import
from flext_core.internal.services import InternalService       # Forbidden pattern
```

## Development Commands

### Essential Commands

```bash
# Quality validation
make validate                # Complete validation (all quality gates)
make check                   # Quick health check (lint + type-check)
make lint                    # Ruff linting
make type-check              # MyPy strict type checking
make test                    # Test suite with coverage
make format                  # Auto-format code

# Meltano operations
make meltano-init            # Initialize Meltano project
make meltano-install         # Install plugins
make meltano-run JOB=job     # Execute specific pipeline
make test-pipeline           # Run basic CSV test pipeline
```

### Current Quality Status

```bash
# Status as of 2025-08-23 (requires fixing before proceeding)
make lint                    # ❌ 11 errors (PLR0911, FBT001, E721, F821)
make type-check              # ❌ 7 errors (FlextDomainService undefined, explicit object)
make test                    # ❌ NameError: FlextDomainService not defined
```

## Dependencies & Requirements

### Core Dependencies

- **Python 3.13+** (strict requirement)
- **Meltano 3.9.1+** (ELT orchestration platform)
- **Singer SDK 0.48.0+** (data extraction/loading protocol)
- **DBT Core 1.10.5** (data transformation framework)
- **flext-core** (foundation patterns and service architecture)
- **flext-cli** (CLI patterns and command processing)

### Environment Configuration

```bash
# Required environment variables
export MELTANO_ENVIRONMENT=dev
export MELTANO_PROJECT_ROOT=$(PWD)
export PYTHONPATH=$(PWD)/src:$(PYTHONPATH)
```

## Integration Points

### FLEXT Ecosystem Dependencies

```python
# Allowed dependencies (Level 1-2 only)
from flext_core import (
    FlextResult,                # Railway-oriented programming
    FlextServiceProcessor,      # Service base classes
    FlextLogger,               # Structured logging
    FlextLogger                 # Logger factory
)

from flext_cli import (
    CLICommand,                # Command implementation
    FlextCliApi,              # CLI API patterns
    cli_enhanced              # Enhanced CLI utilities
)
```

### External Ecosystem Integration

- **Meltano Hub**: Plugin discovery and installation
- **Singer Protocol**: Tap/target specification compliance
- **DBT Projects**: Transformation project management
- **PostgreSQL/Redis**: Data storage and caching (via FLEXT platform)

## Production API

### Bridge Integration (Go ↔ Python)

```bash
# JSON API for Go service integration
python scripts/flext_meltano_bridge.py version
# {"success": true, "data": {"meltano": "3.9.1", "python": "3.13.5"}}

python scripts/flext_meltano_bridge.py list_plugins
# {"success": true, "data": [...]}

python scripts/flext_meltano_bridge.py run_pipeline tap-csv target-csv
# {"success": true, "data": {"status": "completed", "records": 1000}}
```

### Core Library API

```python
# Primary APIs (after architectural refactoring)
from flext_meltano import (
    # Configuration
    FlextMeltanoConfig,

    # Service base classes
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
    FlextMeltanoDbtService,

    # Execution functions
    execute_meltano_command,
    run_pipeline,

    # Singer SDK re-exports
    Stream, Tap, Target, Sink,

    # Exception hierarchy
    FlextMeltanoError,
    FlextMeltanoValidationError
)
```

## Development Standards

### Architecture Compliance

1. **Dependency Inversion**: Follow FLEXT hierarchical architecture (Level 3)
2. **Root Module Imports**: Never import internal modules directly
3. **Service Patterns**: Use FlextServiceProcessor for all service implementations
4. **Result Handling**: FlextResult pattern for all operations
5. **Real API Integration**: No mocks in tests, use actual Meltano/Singer/DBT APIs

### Code Quality Requirements

- **Type Safety**: MyPy strict mode with comprehensive type annotations
- **Linting**: Ruff with all rules enabled (zero tolerance)
- **Testing**: Minimum 90% coverage with real API integration
- **Documentation**: Keep README.md and architectural docs updated
- **SOLID Principles**: Single responsibility, dependency inversion throughout

### Refactoring Phase Requirements

1. **Phase 1**: Fix critical quality gate failures (MyPy, Ruff errors)
2. **Phase 2**: Implement proper SOLID architecture and eliminate duplication
3. **Phase 3**: Achieve 90%+ test coverage with comprehensive validation
4. **Phase 4**: Create backward compatibility layer for existing consumers

## Contributing

### Before Contributing

1. **Quality Gates**: All quality checks must pass (`make validate`)
2. **Architecture Review**: Follow FLEXT Level 3 dependency rules
3. **Real API Testing**: Use actual Meltano/Singer/DBT APIs in tests
4. **Documentation**: Update both README.md and integration docs

### Prohibited Patterns

- ❌ Internal module imports (violates architectural boundaries)
- ❌ Mock/subprocess patterns in tests (use real APIs)
- ❌ Code duplication (use flext-core functionality)
- ❌ Non-SOLID implementations (single responsibility violation)
- ❌ Direct database access (use FLEXT service patterns)

## Links & Resources

- **[FLEXT Platform Overview](../README.md)** - Complete ecosystem documentation
- **[flext-core Foundation](../flext-core/README.md)** - Base patterns and service architecture
- **[flext-cli Patterns](../flext-cli/README.md)** - CLI implementation standards
- **[Architecture Documentation](../docs/architecture/)** - System design and integration patterns

---

**flext-meltano** - *Enterprise data integration foundation for the FLEXT ecosystem*
