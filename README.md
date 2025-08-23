# flext-meltano - Enterprise Data Integration Library

**Type**: Level 3 - Technological Base | **Status**: Architectural Refactoring | **Dependencies**: flext-core, flext-cli

Enterprise data integration library providing native Meltano 3.9.1, Singer SDK 0.48.0, and DBT Core 1.10.5 integration using proper FLEXT architectural patterns.

> 🚧 **Current Status**: Undergoing architectural refactoring to eliminate violations and implement proper FLEXT patterns. MyPy: 100% clean, Ruff: 8 errors being fixed.

## Quick Start

```bash
# Use FLEXT workspace virtual environment
cd /path/to/flext
source .venv/bin/activate
cd flext-meltano

# Install dependencies
make install-dev

# Validate current status
make validate
```

## Architecture Position

### FLEXT Level 3 - Technological Base

```
┌─────────────────────────────────────────────────────────────────────┐
│ LEVEL 4 - MELTANO PLUGINS                                          │
│ 🔌 flext-tap-*, flext-target-*, flext-dbt-* (can import this)      │
├─────────────────────────────────────────────────────────────────────┤
│ LEVEL 3 - TECHNOLOGICAL BASES                                      │
│ 🛠️ [FLEXT-MELTANO] ← YOU ARE HERE                                 │
│ ✅ CAN import: flext-core (Level 1), flext-cli (Level 2)          │
│ ❌ CANNOT import: Level 4+ components                              │
├─────────────────────────────────────────────────────────────────────┤
│ LEVEL 2 - INTERMEDIATE SERVICES                                    │
│ ⚙️ flext-cli, flext-observability, flext-grpc (provides to this)   │
├─────────────────────────────────────────────────────────────────────┤
│ LEVEL 1 - ABSTRACT FOUNDATION                                      │
│ 🏗️ flext-core (provides foundation patterns)                      │
└─────────────────────────────────────────────────────────────────────┘
```

### Core Responsibilities

1. **Data Pipeline Orchestration**: Native integration with Meltano ecosystem
2. **Singer SDK Integration**: Complete tap/target/transformation support  
3. **DBT Integration**: Data transformation project management
4. **FLEXT Pattern Implementation**: Proper service patterns and DI support

## Current Refactoring Status

### ✅ What Works (Validated)

- **Type Safety**: MyPy 100% clean (0 errors)
- **Foundation**: flext-core integration working
- **Dependencies**: Poetry configuration correct
- **APIs**: Meltano 3.9.1, Singer SDK 0.48.0, DBT Core 1.10.5 integrated

### 🔄 Active Refactoring (In Progress)

- **Service Architecture**: Converting FlextDomainService → FlextServiceProcessor
- **Import Corrections**: Moving to root module imports only
- **CLI Integration**: Implementing flext-cli patterns
- **Quality Gates**: Fixing 8 ruff errors

### ❌ Known Issues (Being Fixed)

- **Ruff Errors**: 8 errors in utilities.py and executors_cli.py
- **Test Imports**: ImportError for create_meltano_tap_service  
- **Architecture**: Some violations of FLEXT dependency rules
- **Coverage**: Unknown (tests don't execute due to import errors)

## Proper Usage Patterns

### Service Implementation (New Architecture)

```python
# ✅ CORRECT: Using FlextServiceProcessor
from flext_meltano import FlextMeltanoTapService
from flext_core import FlextResult
from singer_sdk import Tap

class MyTapService(FlextMeltanoTapService):
    def __init__(self) -> None:
        super().__init__(tap_name="my-tap")
    
    def get_tap_class(self) -> type[Tap]:
        return MyTap
    
    def get_default_config(self) -> dict[str, Any]:
        return {"api_key": "required"}

# Usage with proper DI
service = MyTapService()
result = service.run_with_metrics("tap_processing", {"api_key": "test"})

if result.is_success:
    tap_info = result.value
    print(f"Tap ready: {tap_info['tap_name']}")
```

### Root Module Imports (Mandatory)

```python
# ✅ CORRECT: Root module imports
from flext_core import FlextResult, FlextServiceProcessor, get_logger
from flext_cli import CLICommand, FlextCliApi
from flext_meltano import FlextMeltanoTapService, FlextMeltanoConfig

# ❌ WRONG: Internal module imports (architectural violation)
from flext_meltano.base_services import FlextMeltanoTapService  # Use root import
from flext_core.internal.services import InternalService       # Forbidden
```

### Data Pipeline Operations

```python
# ✅ CORRECT: Using proper FLEXT patterns
from flext_meltano import execute_meltano_command, run_pipeline
from flext_core import FlextResult

# Execute Meltano command with FlextResult
result = execute_meltano_command(["--version"])
if result.is_success:
    print(f"Meltano version: {result.value}")
else:
    print(f"Error: {result.error}")

# Run pipeline with proper error handling
pipeline_result = run_pipeline("tap-csv", "target-csv")
if pipeline_result.is_success:
    print(f"Pipeline completed: {pipeline_result.value}")
```

## Development Commands

### Quality Gates (Zero Tolerance)

```bash
# Current status check
make lint                    # ❌ 8 errors (being fixed)
make type-check              # ✅ 0 errors (MyPy clean)
make test                    # ❌ ImportError (being fixed)

# After refactoring completion
make validate                # Complete validation
make check                   # Quick health check
make fix                     # Auto-fix linting issues
```

### Meltano Operations

```bash
# Meltano setup and operations
make meltano-init            # Initialize Meltano project
make meltano-install         # Install Meltano plugins
make meltano-run JOB=job-name    # Run specific pipeline
make meltano-test            # Test Meltano configuration
make test-pipeline           # Run basic CSV test pipeline
```

### Development Workflow

```bash
# Setup (use FLEXT workspace venv)
cd /path/to/flext && source .venv/bin/activate
cd flext-meltano && make install-dev

# Development cycle
make validate                # Check current state
# ... make changes following FLEXT patterns ...
make lint && make type-check # Validate changes
make test                    # Run tests (after fixing imports)
```

## Integration with FLEXT Ecosystem

### Dependencies (Level 1-2 Only)

```python
# ✅ ALLOWED: Level 1 (Foundation)
from flext_core import (
    FlextResult,
    FlextServiceProcessor, 
    FlextLogger,
    get_logger
)

# ✅ ALLOWED: Level 2 (Intermediate Services)  
from flext_cli import (
    CLICommand,
    FlextCliApi,
    cli_enhanced
)

# ❌ FORBIDDEN: Level 3+ (Same or higher levels)
from flext_ldap import SomeClass        # Same level - forbidden
from flext_tap_oracle import SomeTap    # Higher level - forbidden
```

### Provided to Higher Levels

```python
# Level 4 components can import from this library:
from flext_meltano import (
    FlextMeltanoTapService,      # Base for flext-tap-*
    FlextMeltanoTargetService,   # Base for flext-target-*
    FlextMeltanoDbtService,      # Base for flext-dbt-*
    FlextMeltanoConfig,          # Configuration patterns
    execute_meltano_command,     # Pipeline operations
    run_pipeline                 # ELT orchestration
)
```

## Configuration

### Environment Variables

```bash
# Meltano configuration
export MELTANO_ENVIRONMENT=dev
export MELTANO_PROJECT_ROOT=$(PWD)

# Python path setup (for development)
export PYTHONPATH=$(PWD)/src:$(PYTHONPATH)
```

### Dependencies

- **Python 3.13+** (strict requirement)
- **Meltano 3.9.1+** (ELT orchestration)
- **Singer SDK 0.48.0+** (data extraction/loading)
- **DBT Core 1.10.5** (data transformation)
- **flext-core** (foundation patterns)
- **flext-cli** (CLI patterns)

## Quality Standards

### FLEXT Requirements

- **Architecture**: Must follow Level 3 dependency rules
- **Imports**: Root module imports only
- **Patterns**: FlextServiceProcessor for services
- **Results**: FlextResult for all operations
- **Coverage**: 100% target with real APIs (no mocks)
- **Type Safety**: MyPy strict mode compliance

### Current Quality Status

```bash
# Quality metrics (current/target)
Lint Errors: 8/0            # 🔄 Being fixed
Type Errors: 0/0            # ✅ Already clean  
Test Coverage: ?/100%       # 🔄 Tests being fixed
Architecture: Violations/Clean  # 🔄 Being refactored
```

## Refactoring Progress

### Phase 1: Architectural Correction (In Progress)

- [x] Analyze violations and create strategy
- [x] Start service refactoring (FlextMeltanoTapService)
- [ ] Complete all service refactoring
- [ ] Fix CLI to use flext-cli patterns
- [ ] Correct all imports to root modules

### Phase 2: Quality Gates (Planned)

- [ ] Fix all ruff errors
- [ ] Fix broken test imports
- [ ] Achieve 100% test coverage
- [ ] Validate complete functionality

### Phase 3: Legacy Compatibility (Planned)

- [ ] Create compatibility layer for old APIs
- [ ] Add deprecation warnings
- [ ] Update all examples and documentation
- [ ] Final validation and cleanup

## Contributing

### Development Standards

1. **Follow FLEXT Architecture**: Respect Level 3 position in hierarchy
2. **Use Root Imports**: Never import internal modules
3. **Implement Proper Patterns**: FlextServiceProcessor, FlextResult
4. **Quality Gates**: All checks must pass
5. **Real API Integration**: No mocks, use actual Meltano/Singer/DBT
6. **Documentation**: Update both README.md and CLAUDE.md

### Architectural Rules

- ✅ **CAN import**: flext-core, flext-cli
- ❌ **CANNOT import**: flext-ldap, flext-tap-*, flext-target-*, etc.
- ✅ **PROVIDES to**: flext-tap-*, flext-target-*, flext-dbt-*
- ❌ **NEVER violate**: Dependency inversion rules

## Links

- **[FLEXT Workspace](../README.md)**: Ecosystem overview
- **[flext-core](../flext-core/README.md)**: Foundation patterns
- **[flext-cli](../flext-cli/README.md)**: CLI patterns  
- **[CLAUDE.md](CLAUDE.md)**: Development guidance for this component

---

**flext-meltano** - *Enterprise data integration with proper FLEXT architectural patterns*
