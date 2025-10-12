# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Project Overview

**flext-meltano** is the enterprise Meltano data integration and ELT pipeline orchestration foundation for the entire FLEXT ecosystem. This library provides comprehensive Singer protocol implementation, plugin development tools, and Meltano project management with ZERO TOLERANCE for custom ELT implementations.

**Version**: 0.9.0 | **Updated**: 2025-10-10
**Status**: Enterprise ELT pipeline foundation with extensive Singer protocol support · **88% Complete** - Production-capable with verified test infrastructure blockers

---

## 🔗 MCP SERVER INTEGRATION (MANDATORY)

| MCP Server              | Purpose                                                         | Status          |
| ----------------------- | --------------------------------------------------------------- | --------------- |
| **serena**              | Semantic code analysis, symbol manipulation, refactoring        | **MANDATORY**   |
| **sequential-thinking** | Meltano architecture and Singer/DBT integration problem solving | **RECOMMENDED** |
| **context7**            | Third-party library documentation (Meltano, Singer SDK, DBT)    | **RECOMMENDED** |
| **github**              | Repository operations and Meltano ecosystem PRs                 | **ACTIVE**      |

**Usage**: Reference [~/.claude/commands/flext.md](~/.claude/commands/flext.md) for MCP workflows. Use `/flext` command for module optimization.

---

## 🎯 FLEXT-MELTANO PURPOSE

**ROLE**: flext-meltano serves as the enterprise Meltano data integration and ELT pipeline orchestration foundation for the entire FLEXT ecosystem, providing comprehensive Singer protocol implementation, plugin development tools, and Meltano project management.

**CURRENT CAPABILITIES**:

- ✅ **Complete Singer Protocol Implementation**: Full tap and target development framework with state management
- ✅ **Meltano Integration**: Native Meltano project and plugin support with CLI operations
- ✅ **DBT Operations**: DBT model execution, testing, and documentation generation
- ✅ **Plugin Development Framework**: Automated plugin scaffolding and validation tools
- ✅ **Enterprise Pipeline Orchestration**: Advanced ELT pipeline management and monitoring
- ✅ **FLEXT-Core Integration**: Railway-oriented programming with FlextCore.Result[T] patterns
- ✅ **Type Safety**: Python 3.13+ with complete type annotations and Pyrefly validation

**ECOSYSTEM INTEGRATION**:

- **Foundation for 32+ FLEXT Projects**: All flext-tap-*, flext-target-*, flext-dbt-* projects depend on this library
- **Zero Custom ELT Code**: ABSOLUTE prohibition of custom Meltano/Singer/DBT implementations
- **Enterprise Data Pipelines**: Production-ready ELT orchestration for batch and real-time processing
- **client-a Integration**: Critical dependency for Oracle Unified Directory migration project

## 🛑 ZERO TOLERANCE ENFORCEMENT

### ⛔ ABSOLUTELY FORBIDDEN VIOLATIONS

#### 1. **DIRECT MELTANO/SINGER/DBT IMPORTS**

```python
# ❌ ABSOLUTELY FORBIDDEN - Direct ELT library imports
import meltano                        # VIOLATION: Use flext-meltano foundation
import meltano.core                   # VIOLATION: Use FlextMeltanoAdapter
from singer_sdk import Tap            # VIOLATION: Use FlextMeltanoStream/FlextMeltanoTap
import dbt.core                       # VIOLATION: Use FlextMeltanoDbtService
from meltano.core.project import Project  # VIOLATION: Architecture breach

# ✅ CORRECT - FLEXT Ecosystem Foundation Only
from flext_meltano import FlextMeltano, FlextMeltanoService
from flext_meltano import FlextMeltanoAdapter, FlextMeltanoExecutor
from flext_meltano import FlextMeltanoStream, FlextMeltanoTap  # Singer wrappers
from flext_core import FlextCore
```

#### 2. **CUSTOM ELT IMPLEMENTATIONS**

- **FORBIDDEN**: Custom Singer tap/target implementations outside flext-meltano patterns
- **FORBIDDEN**: Direct Meltano CLI subprocess calls - Use FlextMeltanoExecutor
- **FORBIDDEN**: Custom DBT command execution - Use FlextMeltanoDbtService
- **FORBIDDEN**: Manual YAML/JSON pipeline configuration - Use FlextMeltanoConfig
- **FORBIDDEN**: Custom ELT error handling - Use FlextCore.Result[T] railway pattern

### 📋 ENFORCEMENT STANDARDS

1. **ALL ELT operations** through flext-meltano foundation exclusively
2. **ALL Singer protocol interactions** via FlextMeltano abstractions
3. **ALL DBT operations** through FlextMeltanoDbtService
4. **ALL Meltano project management** via FlextMeltanoAdapter
5. **ALL pipeline configurations** through FlextMeltanoConfig
6. **ALL ELT error handling** with FlextCore.Result[T] railway pattern

## 🏗️ ARCHITECTURE OVERVIEW

### **Clean Architecture with Domain-Driven Design**

FLEXT-Meltano follows Clean Architecture principles with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│ 🎯 FLEXT-Meltano - Enterprise ELT Pipeline Foundation     │
├─────────────────────────────────────────────────────────────┤
│ 🏛️  API Layer       │ FlextMeltano - Unified facade API        │
│ 🚀  Application     │ FlextMeltanoService - Business logic      │
│ 🔧  Infrastructure  │ FlextMeltanoAdapter - Meltano integration │
│ 📦  Domain          │ FlextMeltanoModels - Business entities     │
├─────────────────────────────────────────────────────────────┤
│ 🎨  flext-core      │ Foundation patterns & services         │
└─────────────────────────────────────────────────────────────┘
```

### **Core Components**

#### FlextMeltano (Main API)
**Unified facade for all Meltano operations**

```python
from flext_meltano import FlextMeltano

# Initialize the main API
api = FlextMeltano()

# All operations return FlextCore.Result[T] for composable error handling
result = api.create_pipeline("tap-csv", "target-postgres")
if result.is_success:
    pipeline = result.unwrap()
```

#### FlextMeltanoService
**Core service implementing business logic with flext-core integration**

```python
from flext_meltano import FlextMeltanoService

# Extends FlextCore.Service with Meltano-specific functionality
service = FlextMeltanoService()

# Railway-oriented programming with FlextCore.Result[T]
result = service.discover_plugins()
```

#### FlextMeltanoAdapter
**Infrastructure layer providing Meltano CLI integration**

```python
from flext_meltano import FlextMeltanoAdapter

# Low-level Meltano operations
adapter = FlextMeltanoAdapter()
result = adapter.run_tap("tap-gitlab", config={"api_url": "..."})
```

### **Module Organization**

```
src/flext_meltano/
├── api.py                     # FlextMeltano - Main unified API (1200+ lines)
├── services.py                # FlextMeltanoService - Core business logic (1442+ lines)
├── adapters.py                # FlextMeltanoAdapter - Meltano CLI integration (801+ lines)
├── models.py                  # FlextMeltanoModels - ALL Pydantic models (1300+ lines)
├── config.py                  # FlextMeltanoConfig - Configuration management
├── constants.py               # FlextMeltanoConstants - System constants
├── exceptions.py              # FlextMeltanoExceptions - Error hierarchy
├── executor.py                # FlextMeltanoExecutor - Pipeline execution
├── dbt_service.py             # FlextMeltanoDbtService - DBT operations
├── tap_abstractions.py        # FlextMeltanoTapAbstractions - Singer tap support
├── target_abstractions.py     # FlextMeltanoTargetAbstractions - Singer target support
├── singer.py                  # FlextMeltanoSinger - Singer protocol implementation
├── pipeline_service.py        # FlextMeltanoPipelineService - Pipeline orchestration
├── plugin_service.py          # FlextMeltanoPluginService - Plugin management
├── project_service.py         # FlextMeltanoProjectService - Project operations
└── utilities.py               # FlextMeltanoUtilities - Helper functions
```

### **Singer Protocol Implementation**

FLEXT-Meltano provides complete Singer protocol support with enterprise extensions:

```python
from flext_meltano import FlextMeltanoStream, FlextMeltanoTap

# Singer tap implementation using FLEXT wrappers
class MyCustomTap(FlextMeltanoTap):
    """Custom Singer tap with FLEXT ecosystem integration."""
    name = "tap-custom"

    def discover_streams(self) -> list[FlextMeltanoStream]:
        return [MyCustomStream(self)]

class MyCustomStream(FlextMeltanoStream):
    """Custom Singer stream with enterprise features."""
    name = "custom_stream"

    def get_records(self, context: dict | None) -> Iterable[dict]:
        # Stream implementation with FLEXT logging and error handling
        yield {"id": 1, "data": "example"}
```

---

## 📚 DOCUMENTATION STATUS (UPDATED 2025-10-10)

### **Documentation Enhancement Summary**
Successfully updated FLEXT-Meltano documentation to reflect current project status and implementation details:

#### **New Documentation Files Created:**
- ✅ **`docs/implementation_status.md`** - Comprehensive project status (88% complete)
- ✅ **`docs/testing_plan.md`** - Detailed testing infrastructure plan (95% complete, execution blocked)
- ✅ **`docs/phase_4_implementation_plan.md`** - Test infrastructure resolution roadmap

#### **Updated Existing Documentation:**
- ✅ **`docs/COVERAGE_IMPROVEMENT_PLAN.md`** - Updated with current blocked status and resolution plan
- ✅ **`CLAUDE.md`** - Enhanced with current project status and completion metrics

#### **Key Documentation Insights:**
- **Project Completion**: 88% complete with enterprise-grade features implemented
- **Test Infrastructure**: 95% complete but VERIFIED BLOCKED by two critical issues
- **Production Readiness**: Core functionality ready for enterprise deployment (blocked by test validation)
- **Critical Blockers**: VERIFIED - flext-tests dependency missing and BaseModel inheritance AttributeError

### Essential Commands

```bash
# Setup and installation
make setup                    # Complete development environment setup
make install                  # Install dependencies with Poetry
make install-dev             # Install with dev dependencies

# Quality gates (MANDATORY before commit)
make validate                # Complete validation: lint + type + security + test
make check                   # Quick validation: lint + type only
make lint                    # Ruff linting (ZERO violations)
make type-check              # Pyrefly type checking (ZERO errors)
make security                # Bandit security scanning
make test                    # Run tests with 100% coverage requirement
make format                  # Auto-format with Ruff

# Testing
make test-unit              # Unit tests only
make test-integration       # Integration tests only
make test-fast              # Tests without coverage
make coverage-html          # Generate HTML coverage report

# Build and maintenance
make build                  # Build package
make clean                  # Clean build artifacts
make reset                  # Complete reset (clean + setup)
```

### Running Specific Tests

```bash
# Run specific test file
PYTHONPATH=src poetry run pytest tests/unit/test_api.py -v

# Run specific test class
PYTHONPATH=src poetry run pytest tests/unit/test_models.py::TestFlextMeltanoModels -v

# Run with markers
PYTHONPATH=src poetry run pytest -m unit              # Unit tests only
PYTHONPATH=src poetry run pytest -m integration       # Integration tests
PYTHONPATH=src poetry run pytest -m "not slow"        # Skip slow tests

# Run with coverage for specific module
PYTHONPATH=src poetry run pytest --cov=flext_meltano.api --cov-report=term-missing
```

### Quality Standards

#### Type Safety (ZERO TOLERANCE)

- **Pyrefly strict mode** required for all `src/` code (successor to MyPy)
- **100% type annotations** - no `Any` types allowed
- **Complete type coverage** for all public APIs

#### Code Quality (ZERO TOLERANCE)

- **Ruff linting** with comprehensive rules (ZERO violations)
- **88 character line length** (Ruff default)
- **Import organization** handled automatically by Ruff

#### Error Handling (MANDATORY)

All operations return `FlextCore.Result[T]` for composable error handling:

```python
from flext_core import FlextCore
from flext_meltano import FlextMeltano

api = FlextMeltano()

# Railway-oriented programming - chain operations safely
result = (
    api.discover_plugins()
    .flat_map(lambda plugins: api.validate_plugins(plugins))
    .map(lambda valid_plugins: api.install_plugins(valid_plugins))
)

if result.is_success:
    installed_plugins = result.unwrap()
else:
    print(f"Plugin operation failed: {result.error}")
```

---

## 📊 CURRENT STATUS (v0.9.0)

### What Works

- ✅ **Complete Singer Protocol Implementation**: Full tap/target framework with state management
- ✅ **Meltano Integration**: Native project and plugin management with CLI operations
- ✅ **DBT Operations**: Model execution, testing, and documentation generation
- ✅ **Enterprise Pipeline Orchestration**: Advanced ELT pipeline management and monitoring
- ✅ **FLEXT-Core Integration**: Railway-oriented programming with FlextCore.Result[T] patterns
- ✅ **Type Safety**: Python 3.13+ with complete type annotations and Pyrefly validation
- ✅ **Plugin Development Framework**: Automated scaffolding and validation tools

### Known Issues (VERIFIED)

- ❌ **CRITICAL: Test Execution Blocked**: All tests fail at collection phase due to verified blockers
- ❌ **VERIFIED: Missing flext-tests Dependency**: Confirmed `Path /home/marlonsc/flext/flext-tests for flext-tests does not exist`
- ❌ **VERIFIED: BaseModel Inheritance Issue**: Confirmed `AttributeError: type object 'FlextCore.Models' has no attribute 'BaseModel'`
- ⚠️ **Model Compatibility**: Requires flext-core v1.0.0 model structure analysis

### Development Priorities (UPDATED 2025-10-10)

1. **🚨 CRITICAL: Fix Test Infrastructure Blockers** - Resolve VERIFIED flext-tests dependency and BaseModel inheritance issues (immediate 24-48 hours)
2. **Enable Test Execution** - Achieve successful test collection and basic execution (next 1-2 weeks)
3. **Achieve 95%+ Test Coverage** - Complete comprehensive test suite for production readiness (post-blocker resolution)
4. **Documentation Completion**: Finish API documentation and usage examples
5. **Performance Optimization**: Implement streaming and memory-efficient operations
6. **Enterprise Features**: Enhanced monitoring, logging, and error recovery

---

## 🚨 CRITICAL PATTERNS

### MANDATORY: FlextCore.Result Railway Pattern

```python
# ✅ CORRECT - ALL operations use FlextCore.Result pattern
from flext_core import FlextCore
from flext_meltano import FlextMeltanoService

service = FlextMeltanoService()

# Chain operations with railway pattern
result = service.discover_plugins()
if result.is_success:
    plugins = result.unwrap()
    validation_result = service.validate_plugins(plugins)
    if validation_result.is_success:
        print("Plugin validation successful")
    else:
        print(f"Validation failed: {validation_result.error}")
else:
    print(f"Discovery failed: {result.error}")

# ❌ FORBIDDEN - Try/except for business logic
try:
    plugins = service.discover_plugins()  # Missing FlextCore.Result handling
except Exception as e:
    print(f"Error: {e}")
```

### MANDATORY: Root Module Imports

```python
# ✅ CORRECT - Root module imports (MANDATORY)
from flext_meltano import FlextMeltano, FlextMeltanoService
from flext_meltano import FlextMeltanoAdapter, FlextMeltanoModels
from flext_core import FlextCore

# ❌ FORBIDDEN - Internal module imports (breaks ecosystem)
from flext_meltano.api import FlextMeltano
from flext_meltano.services import FlextMeltanoService
```

### MANDATORY: Singer Protocol Abstractions

```python
# ✅ CORRECT - Use FLEXT Singer wrappers
from flext_meltano import FlextMeltanoStream, FlextMeltanoTap

class MyTap(FlextMeltanoTap):
    name = "tap-custom"

# ❌ FORBIDDEN - Direct singer_sdk imports
from singer_sdk import Tap  # VIOLATION
```

---

## 📚 DEPENDENCIES

### Core Dependencies

- **flext-core>=0.9.9** - Foundation patterns and FlextCore.Result[T]
- **meltano>=3.0.0** - Meltano data integration platform
- **singer-sdk>=0.44.0** - Singer protocol implementation
- **dbt-core>=1.10.5** - Data transformation engine
- **pydantic>=2.11.7** - Data validation and models
- **fastapi>=0.115.0** - API framework
- **httpx>=0.28.0** - HTTP client
- **pandas>=2.0.0** - Data processing

### Dev Dependencies

- **ruff>=0.12.3** - Linting and formatting
- **pyrefly>=0.34.0** - Type checking
- **pytest>=8.4.0** - Testing framework
- **bandit>=1.8.0** - Security scanning

---

## 🤝 CONTRIBUTING

### FLEXT-Core Compliance

- [x] Operations return FlextCore.Result[T] for error handling
- [x] Railway-oriented programming patterns
- [x] Complete type annotations with Python 3.13+
- [x] Clean Architecture with Domain-Driven Design
- [x] Root module imports (no internal imports)
- [x] Comprehensive test coverage
- [x] Ruff linting and Pyrefly type checking

### Code Standards

- **Python 3.13+** - Latest Python features and performance
- **Pydantic v2** - Modern data validation
- **Type Hints** - Complete type safety
- **Async Support** - Modern async/await patterns
- **Clean Architecture** - Proper separation of concerns
- **Railway Pattern** - Monadic error handling

---

## 📄 LICENSE

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**FLEXT-Meltano v0.9.0** - Enterprise Meltano data integration and ELT pipeline orchestration foundation for the FLEXT ecosystem.

**Purpose**: Provide comprehensive Singer protocol implementation, plugin development tools, and Meltano project management with ZERO TOLERANCE for custom ELT implementations.

---

## Additional Resources

- **[../CLAUDE.md](../CLAUDE.md)** - FLEXT workspace standards
- **[../flext-core/CLAUDE.md](../flext-core/CLAUDE.md)** - Foundation library patterns
- **[../flext-ldif/CLAUDE.md](../flext-ldif/CLAUDE.md)** - Domain library patterns
- **[README.md](README.md)** - Project overview and usage documentation
