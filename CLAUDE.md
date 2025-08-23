# CLAUDE.md - FLEXT Meltano

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

FLEXT Meltano is a **production-ready Python library** that serves as the enterprise data integration component within the FLEXT Enterprise Data Integration Platform. This library provides native integration with Meltano 3.9.1, Singer SDK 0.48.0, and DBT Core 1.10.5 using proper FLEXT architectural patterns.

**Status**: 🚧 **ACTIVE ARCHITECTURAL REFACTORING** - Implementing proper FLEXT patterns and eliminating architectural violations

**Architecture**: Clean Architecture with proper DI, protocols, and service patterns from flext-core

### Position in FLEXT Ecosystem

FLEXT Meltano is a **LEVEL 3 - BASES TECNOLÓGICAS** component in the FLEXT hierarchical architecture:

- **Parent Ecosystem**: FLEXT Enterprise Data Integration Platform ([../README.md](../README.md))
- **Architecture Level**: Level 3 - Can import from flext-core (Level 1) and flext-cli (Level 2)
- **Integration Role**: Bridge between Go services and Python data processing ecosystem
- **Dependency Rules**: MUST use root module imports from flext-* libraries

## 🎯 CURRENT REFACTORING STATUS (2025-01-XX)

### ✅ ANALYSIS COMPLETED

**What Works and is Validated:**
- **MyPy**: 100% clean - 0 type errors
- **Base Architecture**: flext-core with protocols, services, result patterns working
- **Dependencies**: Poetry configured correctly with flext-core, flext-cli
- **APIs**: Meltano 3.9.1, Singer SDK 0.48.0, DBT Core 1.10.5 integrated

### ❌ CRITICAL ARCHITECTURAL VIOLATIONS IDENTIFIED

1. **GRAVE ARCHITECTURAL VIOLATIONS:**
   - Classes duplicating flext-core functionality (FlextDomainService misuse)
   - Incorrect imports (not using root modules)
   - Missing use of flext-core protocols
   - CLI not using flext-cli patterns

2. **QUALITY PROBLEMS:**
   - 8 ruff errors (PLR0911, FBT001, E721)
   - Broken tests (ImportError: create_meltano_tap_service)
   - Unknown coverage (tests don't execute)

3. **FUNCTIONALITY DUPLICATION:**
   - FlextDomainService being reimplemented
   - Custom CLI patterns instead of flext-cli
   - Custom validation instead of flext-core

### 🔧 SYSTEMATIC REFACTORING STRATEGY

**PHASE 1: ARCHITECTURAL CORRECTION** (IN PROGRESS)
1. ✅ Fix imports to use flext-core root modules
2. 🔄 Refactor services to use FlextServiceProcessor (CURRENT)
3. ⏳ Refactor CLI to use flext-cli patterns
4. ⏳ Eliminate duplications and use protocols

**PHASE 2: QUALITY GATES**
5. ⏳ Fix all ruff and mypy issues
6. ⏳ Fix broken tests and imports

**PHASE 3: TEST COVERAGE**
7. ⏳ Increase coverage to 100% using real APIs
8. ⏳ Validate complete functionality

**PHASE 4: LEGACY COMPATIBILITY**
9. ⏳ Create compatibility layer for old APIs
10. ⏳ Final validation and cleanup

### 🚧 CURRENT REFACTORING PROGRESS

**Files Being Refactored:**
- `base_services.py`: ✅ Started - Converting FlextDomainService to FlextServiceProcessor
- `executors_cli.py`: ⏳ Pending - Will use flext-cli patterns
- `utilities.py`: ⏳ Pending - Remove duplicated functionality
- `__init__.py`: ⏳ Pending - Update exports for new architecture

**Key Changes Made:**
1. **FlextMeltanoTapService**: 
   - ❌ OLD: `FlextDomainService[dict[str, object]]` (frozen=True conflicts)
   - ✅ NEW: `FlextServiceProcessor[dict[str, Any], Tap, dict[str, Any]]`
   - ✅ Proper constructor with dependency injection
   - ✅ Correct process() and build() methods

**Next Steps:**
1. Complete FlextMeltanoTapService refactoring
2. Refactor FlextMeltanoTargetService and FlextMeltanoDbtService
3. Fix CLI to use flext-cli patterns
4. Update all imports to use root modules
5. Create legacy compatibility layer

## Architecture Principles (FLEXT Standards)

### 1. DEPENDENCY INVERSION (DI) MANDATORY

**Hierarchical Layers (Bottom-Up):**

- **LEVEL 1 - ABSTRACT BASE**: flext-core (most abstract)
- **LEVEL 2 - INTERMEDIATE**: flext-cli, flext-observability, etc.
- **LEVEL 3 - TECHNOLOGICAL BASES**: flext-meltano (THIS PROJECT)
- **LEVEL 4 - MELTANO PLUGINS**: flext-tap-*, flext-target-*, flext-dbt-*

### 2. ROOT MODULE IMPORT RULES

**✅ CORRECT PATTERN - Root Module Imports:**
```python
# ✅ CORRECT: Import from root module
from flext_core import ServiceResult, ConfigBase, FlextServiceProcessor
from flext_cli import CLICommand, CLIHandler
```

**❌ ANTI-PATTERN - Direct Submodule Imports:**
```python
# ❌ WRONG: Direct submodule imports
from flext_core.internal.hidden_module import HiddenClass
from flext_cli.internal.commands.secret import SecretCommand
```

### 3. SERVICE PATTERNS

**✅ CORRECT - Using FlextServiceProcessor:**
```python
class FlextMeltanoTapService(
    FlextServiceProcessor[dict[str, Any], Tap, dict[str, Any]], ABC
):
    def __init__(self, tap_name: str) -> None:
        super().__init__()
        self.tap_name = tap_name
    
    def process(self, request: dict[str, Any]) -> FlextResult[Tap]:
        # Process configuration and create Tap instance
        pass
    
    def build(self, domain: Tap, *, correlation_id: str) -> dict[str, Any]:
        # Build final result
        pass
```

**❌ WRONG - Misusing FlextDomainService:**
```python
# ❌ WRONG: FlextDomainService with frozen=True + mutable fields
class FlextMeltanoTapService(FlextDomainService[dict[str, object]], ABC):
    tap_name: str  # Conflicts with frozen=True
    wrapper_singer: MeltanoSingerWrapper = MeltanoSingerWrapper()  # Mutable default
```

## Development Commands

### Essential Quality Gates

```bash
# Current Status Check
make lint                    # ❌ 8 errors (PLR0911, FBT001, E721)
make type-check              # ✅ 0 errors (MyPy clean)
make test                    # ❌ ImportError: create_meltano_tap_service

# Quality Gates (After Refactoring)
make validate                # Complete validation (lint + type + security + test)
make check                   # Quick health check (lint + type-check only)
make fix                     # Auto-fix linting issues
```

### Development Setup

```bash
# Setup (Use existing venv)
source ../.venv/bin/activate  # Use flext workspace venv
make install-dev             # Install dev dependencies
make setup                   # Complete development setup
```

### Testing Commands

```bash
# Testing (After fixing imports)
make test                    # Full test suite with 90% coverage requirement
make test-unit               # Unit tests only
make test-integration        # Integration tests only
make test-fast               # Tests without coverage
make coverage-html           # HTML coverage report
```

## Core APIs and Usage

### Library Import Pattern (After Refactoring)

```python
# ✅ CORRECT: Root module imports
from flext_meltano import (
    FlextMeltanoTapService,
    FlextMeltanoTargetService, 
    FlextMeltanoDbtService,
    FlextMeltanoConfig,
    FlextMeltanoError
)

# ✅ CORRECT: Singer SDK re-exports
from flext_meltano import Stream, Tap, Target, Sink

# ✅ CORRECT: CLI integration (after refactoring)
from flext_meltano import FlextMeltanoCli
```

### Service Usage Pattern (New Architecture)

```python
from flext_meltano import FlextMeltanoTapService
from flext_core import FlextResult

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
else:
    print(f"Error: {result.error}")
```

## Current Implementation Status

### ✅ Working Components

- **Base Architecture**: flext-core integration working
- **Dependencies**: Poetry configuration correct
- **Type Safety**: MyPy 100% clean
- **APIs**: Meltano, Singer SDK, DBT Core integrated

### 🔄 Components Being Refactored

- **Services**: Converting to FlextServiceProcessor pattern
- **CLI**: Will use flext-cli patterns
- **Imports**: Converting to root module imports
- **Tests**: Fixing broken imports and increasing coverage

### ❌ Known Issues (Being Fixed)

- **Ruff Errors**: 8 errors in utilities.py and executors_cli.py
- **Test Imports**: ImportError for create_meltano_tap_service
- **Architecture**: Violations of FLEXT dependency rules
- **Coverage**: Unknown (tests don't execute due to import errors)

## Quality Standards

### Zero Tolerance Quality Gates

- **Linting**: Ruff with strict rules
- **Type Checking**: MyPy strict mode (currently clean)
- **Architecture**: FLEXT dependency inversion rules
- **Coverage**: 100% target with real APIs (no mocks)
- **Imports**: Root module imports only

### Code Style Requirements

- **Python 3.13** with advanced type hints
- **Pydantic** for configuration and validation
- **SOLID principles** enforcement
- **Clean Architecture** with proper DI
- **FlextResult** patterns throughout

## Integration Points

### FLEXT Ecosystem Integration

- **flext-core**: Base patterns, protocols, services, result handling
- **flext-cli**: CLI patterns and command handling
- **FlexCore Service**: Go service integration via bridge pattern

### External Dependencies

- **Meltano 3.9.1**: ELT orchestration platform
- **Singer SDK 0.48.0**: Data extraction/loading protocol  
- **DBT Core 1.10.5**: Data transformation framework
- **Pydantic 2.11+**: Configuration and validation

## Development Best Practices

### Architectural Rules (MANDATORY)

1. **ALWAYS use root module imports** from flext-* libraries
2. **NEVER duplicate functionality** that exists in flext-core
3. **ALWAYS use FlextServiceProcessor** for service implementations
4. **NEVER use FlextDomainService** with mutable fields
5. **ALWAYS follow FLEXT dependency hierarchy**

### Quality Requirements

6. **Run quality gates** before committing: `make validate`
7. **100% test coverage** with real APIs (no mocks)
8. **Zero ruff/mypy errors** tolerance
9. **Proper DI patterns** throughout
10. **FlextResult patterns** for all operations

### Testing Requirements

11. **Real API integration**: Use actual Meltano/Singer/DBT APIs
12. **No mocks/subprocess**: Direct Python API integration
13. **Comprehensive coverage**: Unit, integration, e2e tests
14. **Railway-oriented programming**: FlextResult patterns

## Current Focus Areas

### 🚨 IMMEDIATE PRIORITIES

1. **Complete Service Refactoring**: Finish FlextMeltanoTapService, TargetService, DbtService
2. **Fix CLI Integration**: Use flext-cli patterns properly
3. **Correct All Imports**: Root module imports throughout
4. **Fix Test Imports**: Resolve ImportError issues
5. **Quality Gates**: Get all quality checks passing

### 📋 REFACTORING CHECKLIST

- [ ] Complete base_services.py refactoring
- [ ] Refactor executors_cli.py to use flext-cli
- [ ] Fix utilities.py duplications
- [ ] Update __init__.py exports
- [ ] Fix all test imports
- [ ] Create legacy compatibility layer
- [ ] Achieve 100% test coverage
- [ ] Validate complete functionality

### 🎯 SUCCESS CRITERIA

- ✅ Zero architectural violations
- ✅ Zero ruff/mypy errors  
- ✅ 100% test coverage with real APIs
- ✅ All functionality preserved
- ✅ Proper FLEXT patterns throughout
- ✅ Legacy compatibility maintained

---

**IMPORTANT**: This refactoring follows FLEXT enterprise standards with maximum attention to architectural integrity. Any shortcuts or inadequate implementations compromise the project's architectural foundation.
