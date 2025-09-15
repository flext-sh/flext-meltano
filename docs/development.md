# flext-meltano Development Guide

**Development workflow and guidelines for FLEXT ecosystem ELT foundation library**

> **⚠️ DEVELOPMENT STATUS**: Current implementation requires abstraction layer for full FLEXT compliance. See compliance issues below.

---

## 🎯 Development Overview

flext-meltano serves as the comprehensive ELT foundation library for the FLEXT ecosystem, providing:

- **Enterprise Meltano Integration** - Production-grade project management
- **Singer Protocol Abstractions** - Complete tap/target workflow support
- **dbt Transformation Services** - Data transformation orchestration
- **FLEXT Pattern Compliance** - Railway-oriented programming with FlextResult
- **Quality Standards** - Zero-tolerance quality gates and type safety

**Development Focus**: Maintaining enterprise-grade ELT operations while addressing current architecture compliance gaps.

---

## 📋 Prerequisites

### Development Environment

```bash
# Required tools
- Python 3.13+
- Poetry for dependency management
- Git for version control
- Access to FLEXT workspace virtual environment

# Environment setup
cd /home/marlonsc/flext
source .venv/bin/activate
cd flext-meltano
poetry install --with dev,test
```

### Understanding the Codebase

**Essential files to understand**:
- `src/flext_meltano/services.py` - Core ELT orchestration service
- `src/flext_meltano/adapters.py` - Meltano Core integration (compliance issues here)
- `src/flext_meltano/tap_abstractions.py` - Singer protocol abstractions
- `src/flext_meltano/service_implementations.py` - Service implementations

**Architecture metrics**:
- **20 Python modules** with 7,354 total lines
- **600+ FlextResult usages** across 174 methods
- **Single class per module** following FLEXT patterns
- **75% FLEXT compliance** (blocked by direct imports)

---

## 🚀 Development Workflow

### 1. Quality Gates (Mandatory)

**Before any changes:**

```bash
# Quick validation
make check                    # lint + type-check
make test-fast               # tests without coverage

# Complete validation
make validate                # lint + type + security + test
```

**Quality gate status**:
- **Linting**: ✅ Passes (Ruff with zero tolerance)
- **Type Checking**: ✅ Passes (MyPy strict mode)
- **Testing**: ✅ Functional (90%+ coverage target)
- **Architecture**: 🔴 Compliance violations (direct imports)

### 2. Development Commands

```bash
# Essential development commands
make lint                    # Ruff linting (zero tolerance policy)
make type-check             # MyPy strict mode validation
make test                   # Complete test suite with coverage
make format                 # Auto-format code

# Quick aliases
make l                      # lint
make t                      # test
make tc                     # type-check
make v                      # validate
```

### 3. Code Standards

**FlextResult Pattern** (Mandatory):
```python
from flext_core import FlextResult

def safe_operation() -> FlextResult[dict]:
    try:
        # Perform operation
        return FlextResult.ok({"status": "success"})
    except Exception as e:
        return FlextResult.fail(f"Operation failed: {e}")
```

**Service Pattern** (Required):
```python
from flext_core import FlextDomainService

class CustomELTService(FlextDomainService):
    def __init__(self):
        super().__init__()
        self._logger = self.get_logger()

    def process_data(self) -> FlextResult[dict]:
        # Implementation with proper error handling
        pass
```

---

## 🔧 Architecture Guidelines

### Current Architecture Status

**Functional Components** ✅:
- FlextResult pattern implementation (600+ usages)
- Service inheritance from FlextDomainService
- Single class per module structure
- Type safety with MyPy strict mode
- Comprehensive error handling

**Compliance Issues** 🔴:
- Direct meltano.core imports in adapters.py (lines 17-25)
- dbt integration placeholder implementation
- Missing modern 2025 ELT patterns

### Code Organization

**Module Structure**:
```
src/flext_meltano/
├── __init__.py              # Root-level exports only
├── services.py              # Primary ELT orchestration
├── adapters.py              # Meltano Core integration (compliance issues)
├── service_implementations.py # Service implementations
├── tap_abstractions.py      # Singer tap abstractions
├── target_abstractions.py   # Singer target abstractions
├── executors.py             # Command execution
├── config.py                # Configuration management
├── utilities.py             # Helper utilities
└── validators.py            # Data validation
```

**Import Standards**:
```python
# ✅ CORRECT - Root-level imports only
from flext_meltano import FlextMeltanoService, FlextMeltanoAdapter
from flext_core import FlextResult, FlextDomainService

# ❌ FORBIDDEN - Internal module imports
from flext_meltano.services import FlextMeltanoService
from flext_meltano.adapters import FlextMeltanoAdapter
```

---

## 🧪 Testing Strategy

### Test Structure

```
tests/
├── unit/                   # Unit tests (isolated components)
├── integration/            # Integration tests (real APIs)
├── e2e/                   # End-to-end pipeline tests
└── conftest.py            # Test configuration
```

### Testing Commands

```bash
# Complete test suite
make test                   # Full suite with 90%+ coverage target

# Specific test categories
pytest tests/unit/          # Unit tests only
pytest tests/integration/   # Integration tests with real APIs
pytest tests/e2e/          # End-to-end pipeline tests

# Coverage analysis
pytest --cov=src --cov-report=term-missing
pytest --cov=src --cov-report=html
```

### Testing Standards

**Real API Integration** (Preferred):
```python
import pytest
from flext_meltano import FlextMeltanoAdapter

@pytest.mark.integration
async def test_meltano_adapter_real_api():
    """Test with real Meltano APIs where possible."""
    adapter = FlextMeltanoAdapter()
    result = await adapter.validate_project()
    assert result.is_success
```

**Mocking Only When Necessary**:
```python
@pytest.mark.unit
def test_service_logic():
    """Unit test for service logic without external dependencies."""
    # Mock only external dependencies, not internal logic
    pass
```

---

## 🔍 Debugging and Troubleshooting

### Common Development Issues

**1. Import Compliance Failures**
```bash
# Check for direct imports
grep -r "from meltano.core" src/

# Expected output: Shows violations in adapters.py
# Resolution: Use abstractions until wrapper implemented
```

**2. FlextResult Pattern Violations**
```bash
# Check FlextResult usage
grep -r "FlextResult" src/ | wc -l

# Should show 600+ usages
# Ensure all new code follows pattern
```

**3. Type Checking Issues**
```bash
# Run MyPy for detailed errors
make type-check

# Common issues:
# - Missing type annotations
# - Any types instead of specific types
# - Missing return type annotations
```

### Debugging Tools

```bash
# Python debugging
python -m pdb script.py     # Debugger
python -v script.py         # Verbose output
PYTHONPATH=src python -m module

# Environment debugging
which python                # Check Python path
poetry env info            # Virtual environment info
poetry show flext-core     # Check dependencies
```

---

## 🔧 Development Best Practices

### Code Quality

**1. Type Safety** (Mandatory):
```python
from typing import Dict, List, Optional
from flext_core import FlextResult

def typed_function(
    config: Dict[str, str],
    optional_param: Optional[List[str]] = None
) -> FlextResult[Dict[str, int]]:
    """Always include complete type annotations."""
    pass
```

**2. Error Handling** (Required):
```python
# ✅ CORRECT - FlextResult pattern
def safe_operation() -> FlextResult[str]:
    try:
        # Operation logic
        return FlextResult.ok("success")
    except Exception as e:
        return FlextResult.fail(f"Operation failed: {e}")

# ❌ FORBIDDEN - Try/except fallbacks
def unsafe_operation():
    try:
        # Operation logic
        return "success"
    except Exception:
        return None  # Loss of error information
```

**3. Service Patterns** (Mandatory):
```python
from flext_core import FlextDomainService

class ELTProcessingService(FlextDomainService):
    def __init__(self):
        super().__init__()
        self._logger = self.get_logger()

    def process_data(self) -> FlextResult[dict]:
        self._logger.info("Starting ELT processing")
        # Implementation
```

### Development Guidelines

**1. FLEXT Integration**:
- Always use flext-core base classes
- Follow FlextResult pattern for all operations
- Use flext-cli for any CLI operations
- Integrate with flext-observability for monitoring

**2. ELT-Specific Patterns**:
- Use Singer protocol abstractions
- Implement proper Meltano project management
- Follow dbt transformation patterns
- Maintain pipeline configuration standards

**3. Quality Assurance**:
- Run quality gates before each commit
- Maintain 90%+ test coverage
- Use real APIs in tests where possible
- Follow type safety requirements

---

## 🚨 Current Limitations and Workarounds

### Architecture Compliance Issues

**Issue 1: Direct meltano.core Imports**
- **Location**: `src/flext_meltano/adapters.py` lines 17-25
- **Impact**: Violates FLEXT zero-tolerance policy
- **Workaround**: Use existing abstractions, avoid direct usage
- **Resolution**: Abstraction layer implementation (4-6 weeks)

**Issue 2: dbt Integration Placeholder**
- **Current**: Returns static data
- **Expected**: Real dbt transformation execution
- **Workaround**: Acknowledge limitation in tests
- **Resolution**: dbt programmatic API integration (3-4 weeks)

### Development Constraints

Due to compliance issues:
1. **Production Use**: Not recommended until resolution
2. **Full Integration**: Limited ecosystem compatibility
3. **Modern Patterns**: Missing 2025 ELT best practices

### Working Within Constraints

**Recommended Approach**:
1. Use functional abstractions (FlextTapAbstractions, FlextTargetAbstractions)
2. Follow FlextResult patterns consistently
3. Maintain test coverage with available APIs
4. Document limitations clearly
5. Plan for abstraction layer adoption

---

## 🔄 Contributing Guidelines

### Pull Request Process

1. **Create Feature Branch**:
```bash
git checkout -b feature/description
```

2. **Development**:
```bash
# Make changes following standards
make validate              # Ensure quality gates pass
```

3. **Testing**:
```bash
make test                 # Ensure tests pass
pytest --cov=src --cov-report=term  # Check coverage
```

4. **Quality Check**:
```bash
make lint                 # Zero tolerance linting
make type-check          # Type safety validation
```

### Code Review Checklist

- [ ] FlextResult pattern used consistently
- [ ] Type annotations complete and accurate
- [ ] Tests included with good coverage
- [ ] Quality gates pass without errors
- [ ] Documentation updated if needed
- [ ] No new compliance violations introduced

---

## 📊 Metrics and Monitoring

### Development Metrics

**Code Quality**:
- **Lines of Code**: 7,354 across 20 modules
- **FlextResult Usage**: 600+ instances, 174 methods
- **Type Coverage**: 100% with MyPy strict mode
- **Test Coverage**: 90%+ target with real API testing

**Quality Gates**:
- **Linting**: Zero errors (Ruff)
- **Type Checking**: Zero errors (MyPy strict)
- **Testing**: All tests passing
- **Security**: No vulnerabilities detected

### Progress Tracking

**Compliance Status**:
- **FLEXT Patterns**: 75% compliant
- **Service Implementation**: ✅ Complete
- **Error Handling**: ✅ Comprehensive
- **Architecture**: 🔴 Blocked (direct imports)

---

**Development Guide v0.9.0** - Comprehensive development workflow reflecting current capabilities and compliance gaps requiring systematic resolution for full FLEXT ecosystem integration.
