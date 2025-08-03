# FLEXT Meltano Development Guide

**⚠️ CRITICAL**: This project has **3 critical issues** that must be resolved before development can proceed. See [../TODO.md](../TODO.md) for immediate fixes required.

## 🚨 Development Status

**BEFORE STARTING DEVELOPMENT**:

1. **Bridge Integration Broken**: `FlextMeltanoBridge` class missing
2. **Quality Gates Failing**: 3 MyPy errors, 1 test failure
3. **Type Safety Compromised**: Cannot merge code until fixes applied

```bash
# Current development state verification:
make validate                 # ❌ FAILING - must fix before proceeding
```

## 🔧 Development Setup

### **Prerequisites**

| Requirement | Version | Status      | Notes                      |
| ----------- | ------- | ----------- | -------------------------- |
| **Python**  | 3.13+   | ✅ Required | Strict version requirement |
| **Poetry**  | 1.8+    | ✅ Required | Dependency management      |
| **Make**    | Any     | ✅ Required | Development commands       |
| **Git**     | 2.0+    | ✅ Required | Pre-commit hooks           |

### **Initial Setup**

```bash
# 1. Clone and navigate
cd /path/to/flext-meltano

# 2. Complete development setup
make setup                    # Install everything + pre-commit hooks

# 3. Verify installation (WILL FAIL until issues fixed)
make validate                 # ❌ Expected failures - see TODO.md

# 4. Check specific problems
make type-check              # Shows 3 MyPy errors
make test                    # Shows 1 test failure
python scripts/flext_meltano_bridge.py version  # ImportError
```

### **Environment Configuration**

```bash
# Required environment variables
export MELTANO_ENVIRONMENT=dev
export MELTANO_PROJECT_ROOT=$(pwd)
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# Optional: Configure Poetry virtual environment
poetry config virtualenvs.in-project true
poetry config virtualenvs.create true
```

## 🔄 Development Workflow

### **Daily Development Cycle** (After Critical Fixes)

```bash
# 1. Start with health check
make doctor                  # Project diagnostics
make diagnose               # Environment check

# 2. Code quality cycle
make format                 # Auto-format code (Ruff)
make lint                   # Check quality (✅ currently passing)
make type-check             # Check types (❌ currently failing)
make test                   # Run tests (❌ currently failing)

# 3. Complete validation
make validate               # All quality gates (❌ currently failing)
```

### **Pre-commit Workflow**

```bash
# Automatic quality checks before commit
git add .
git commit -m "feature: implement something"
# → Pre-commit hooks run automatically
# → Will BLOCK commit until quality gates pass
```

### **Branch Strategy**

```bash
# Feature development
git checkout -b feature/implement-missing-bridge
# → Work on critical fixes first
# → Ensure quality gates pass before PR

# Hotfix development
git checkout -b hotfix/fix-bridge-integration
# → For critical issues like current bridge problem
```

## 🧪 Testing Strategy

### **Test Organization (20 Files)**

```
tests/
├── conftest.py                      # Pytest configuration and fixtures
├── test_*.py                        # Main functionality tests (12 files)
├── unit/                            # Unit tests with mocks
├── integration/                     # Integration tests with real dependencies
├── e2e/                             # End-to-end pipeline tests
├── extensions/oracle_oic/           # Extension-specific tests
└── fixtures/                        # Test data and configuration
```

### **Test Commands**

```bash
# Essential test patterns
make test                    # Full suite with 90% coverage (❌ failing)
make test-unit               # Unit tests only
make test-integration        # Integration tests only
make test-fast               # Tests without coverage for quick feedback

# Pytest markers (from pyproject.toml)
pytest -m unit               # Unit tests only
pytest -m integration        # Integration tests
pytest -m e2e                # End-to-end tests
pytest -m slow               # Slow tests (for CI/CD)
pytest -m smoke              # Smoke tests for health check

# Specific test execution
pytest tests/test_flext_singer.py -v                   # Singer integration
pytest tests/test_dbt_integration.py -v                # DBT integration
pytest tests/test_singer_integration.py -v             # ❌ Currently failing
pytest tests/extensions/ -v                            # Extension tests
```

### **Coverage Requirements**

```bash
# Coverage enforcement (90% minimum)
make coverage-html           # HTML report in reports/coverage/
pytest --cov=src/flext_meltano --cov-report=term-missing --cov-fail-under=90

# Current metrics:
# - Target: 90%+ enforced
# - Files: 18,026 LOC Python
# - Test Files: 20 (may need more for enterprise standards)
```

## 🛡️ Quality Gates

### **Quality Standards Enforcement**

```bash
# Complete validation pipeline (must pass before merge)
make validate                # ❌ FAILING (3 critical issues)
├── make lint               # ✅ PASSING (Ruff ALL rules enabled)
├── make type-check         # ❌ FAILING (3 MyPy errors)
├── make security           # ⚠️ UNKNOWN (needs testing)
└── make test               # ❌ FAILING (1 test failure)
```

### **Individual Quality Checks**

```bash
# Linting (Ruff with ALL rules enabled)
make lint                   # ✅ Currently passing
make format                 # Auto-format code
make fix                    # Auto-fix linting issues

# Type checking (MyPy strict mode)
make type-check             # ❌ 3 errors in cli.py:157, validation.py:250,344

# Security scanning
make security               # Bandit + pip-audit
make deps-audit             # Dependency vulnerability scanning

# Pre-commit hooks
make pre-commit             # Run all hooks manually
pre-commit run --all-files  # Alternative command
```

### **Quality Gate Failures (Current)**

#### **1. MyPy Type Errors** 🔴

```python
# src/flext_meltano/cli.py:157
version = result.data["stdout"].strip() if result.data else "unknown"
# Error: "object" has no attribute "strip"

# src/flext_meltano/validation.py:250
dict[str, str | int | None] vs dict[str, object]

# src/flext_meltano/validation.py:344
dict[str, Sequence[str]] vs dict[str, object]
```

#### **2. Test Failure** 🔴

```python
# tests/test_singer_integration.py:135
FAILED tests/test_singer_integration.py::TestTargetServiceIntegration::test_target_service_creation
AssertionError: assert False
FlextResult(data=None, is_success=False, error='Target service initialization failed: Target class not configured')
```

## 📦 Meltano Development Operations

### **Meltano Project Setup** (After Fixes)

```bash
# Initialize Meltano project (creates meltano.yml)
make meltano-init            # One-time setup

# Plugin management
make meltano-install         # Install configured plugins
make meltano-discover TAP=tap-csv    # Discover schema from tap
make meltano-ui              # Start Meltano UI (port 5000)

# Pipeline testing
make test-pipeline           # Basic CSV ↔ CSV pipeline test
make meltano-run JOB=job-name    # Run specific pipeline job
```

### **Singer Development Workflow**

```bash
# Singer validation
make singer-validate TAP=tap-csv    # Validate Singer output

# Plugin development cycle
pytest tests/test_flext_singer.py -v           # Test Singer integration
pytest tests/test_singer_integration.py -v     # ❌ Currently failing
```

## 🔗 Bridge Development (CRITICAL)

### **Current Bridge Issue**

```python
# scripts/flext_meltano_bridge.py:11
from flext_meltano.simple_bridge import FlextMeltanoBridge
#                    ^^^^^^^^^^^^^ MODULE DOES NOT EXIST

# Results in:
# ImportError: No module named 'flext_meltano.simple_bridge'
```

### **Bridge Implementation Required**

```python
# MISSING: src/flext_meltano/simple_bridge.py
"""Bridge interface for Go ↔ Python integration."""

class FlextMeltanoBridge:
    """Bridge class for Go service integration."""

    def get_version(self) -> None:
        """Get Meltano version."""
        # Implementation needed

    def list_plugins(self) -> None:
        """List available plugins."""
        # Implementation needed

    def add_plugin(self, plugin_type: str, name: str) -> None:
        """Add plugin to project."""
        # Implementation needed

    def discover_catalog(self, tap_name: str) -> None:
        """Discover catalog from tap."""
        # Implementation needed

    def run_pipeline(self, tap: str, target: str) -> None:
        """Execute pipeline between tap and target."""
        # Implementation needed

    def invoke_dbt(self, command: str, *args: str) -> None:
        """Execute DBT command."""
        # Implementation needed
```

### **Bridge Testing** (After Implementation)

```bash
# Test bridge operations
python scripts/flext_meltano_bridge.py version                    # Version check
python scripts/flext_meltano_bridge.py list_plugins               # Plugin list
python scripts/flext_meltano_bridge.py run_pipeline tap-csv target-csv  # Pipeline

# Integration from Go (subprocess simulation)
subprocess.run(["python", "scripts/flext_meltano_bridge.py", "version"])
```

## 🏗️ Module Development Patterns

### **Current Module Structure** (17 Modules)

```python
# Enterprise-grade patterns to follow:

# 1. Base classes (base.py)
from flext_meltano.base import FlextMeltanoTapService, FlextMeltanoConfig

# 2. Core services (core.py)
from flext_meltano.core import FlextMeltanoOrchestrationService

# 3. Execution layer (execution.py)
from flext_meltano.execution import execute_meltano_command, run_pipeline

# 4. Discovery system (discovery.py)
from flext_meltano.discovery import discover_plugins, discover_catalog
```

### **Adding New Functionality**

```python
# 1. Follow existing patterns
class NewFlextMeltanoService(FlextMeltanoBaseService):
    """New service following enterprise patterns."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        super().__init__(config)

    def new_operation(self) -> FlextResult[str]:
        """Implement using FlextResult pattern."""
        try:
            # Implementation
            return FlextResult.success("Operation completed")
        except Exception as e:
            return FlextResult.failure(f"Operation failed: {e}")

# 2. Add to appropriate module (not __init__.py directly)

# 3. Export through module __init__.py
# 4. Add to main __init__.py __all__ list (carefully - already 290+ exports)
```

### **Testing New Features**

```python
# tests/test_new_feature.py
import pytest
from flext_meltano.new_module import NewFlextMeltanoService

class TestNewFeature:
    """Test new feature following existing patterns."""

    def test_new_operation_success(self):
        """Test successful operation."""
        service = NewFlextMeltanoService(mock_config)
        result = service.new_operation()
        assert result.is_success

    def test_new_operation_failure(self):
        """Test failure handling."""
        service = NewFlextMeltanoService(invalid_config)
        result = service.new_operation()
        assert not result.is_success
```

## 🔧 Debugging & Diagnostics

### **Common Issues & Solutions**

#### **ImportError: simple_bridge** 🔴

```bash
# Problem: Bridge module missing
# Solution: Implement src/flext_meltano/simple_bridge.py
touch src/flext_meltano/simple_bridge.py
# Add FlextMeltanoBridge class implementation
```

#### **MyPy Type Errors** 🔴

```bash
# Problem: Type annotations incompatible
# Solution: Fix specific type issues
make type-check  # Shows exact locations and fixes needed
```

#### **Test Failures** 🔴

```bash
# Problem: Test configuration issues
# Solution: Review failing test and fix underlying issue
pytest tests/test_singer_integration.py::TestTargetServiceIntegration::test_target_service_creation -v -s
```

### **Development Diagnostics**

```bash
# Project health check
make doctor                  # Complete project diagnostics
make diagnose               # Environment and dependency check

# Dependency issues
poetry check                # Verify poetry configuration
poetry show --tree          # Show dependency tree
make deps-audit             # Security audit

# Environment issues
python --version            # Should be 3.13+
poetry --version            # Should be 1.8+
which python               # Should point to poetry venv
```

## 📋 Development Priorities

### **Phase 1: Critical Fixes** (1-2 days)

**MANDATORY BEFORE OTHER DEVELOPMENT**

1. **Implement `FlextMeltanoBridge`**:

   ```bash
   touch src/flext_meltano/simple_bridge.py
   # Implement complete bridge interface
   ```

2. **Fix MyPy errors**:

   ```python
   # Fix cli.py:157, validation.py:250,344
   ```

3. **Resolve test failure**:

   ```python
   # Fix test_singer_integration.py:135
   ```

4. **Verify quality gates**:

   ```bash
   make validate  # Must pass before proceeding
   ```

### **Phase 2: Development Standards** (1-2 weeks)

1. **Refactor overloaded `__init__.py`** (290+ exports → manageable modules)
2. **Standardize naming conventions** (FlextMeltano*vs Flext* inconsistencies)
3. **Improve error handling** (consistent FlextResult usage)
4. **Increase test coverage** (20 files may be insufficient for 18k LOC)

### **Phase 3: Advanced Development** (2-4 weeks)

1. **Performance optimization** (bridge communication, subprocess efficiency)
2. **Monitoring integration** (observability patterns)
3. **Security hardening** (secure subprocess execution)
4. **Documentation completion** (API docs, examples)

## 🚀 Contribution Guidelines

### **Code Contribution Workflow**

1. **Pre-contribution checklist**:

   - [ ] All critical issues from TODO.md resolved
   - [ ] `make validate` passes completely
   - [ ] Feature/bugfix branch created
   - [ ] Tests written for new functionality

2. **Development cycle**:

   ```bash
   # Create feature branch
   git checkout -b feature/your-feature

   # Implement changes
   # ... code changes ...

   # Quality checks
   make format && make validate

   # Commit with quality gates
   git add . && git commit -m "feat: implement feature"
   ```

3. **Pull request requirements**:
   - [ ] Quality gates passing (`make validate`)
   - [ ] Test coverage maintained (90%+)
   - [ ] Documentation updated
   - [ ] Bridge integration tested (if applicable)

### **Code Style Standards**

```python
# Follow enterprise patterns:
from flext_core import FlextResult
from flext_meltano.base import FlextMeltanoConfig

class ExampleService:
    """Enterprise service example."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        self._config = config

    def process_data(self, data: dict[str, Any]) -> FlextResult[str]:
        """Process data with proper error handling."""
        try:
            # Process data
            return FlextResult.success("Processing completed")
        except Exception as e:
            return FlextResult.failure(f"Processing failed: {e}")
```

## 🆘 Getting Help

### **For Critical Issues**

1. **Start with [../TODO.md](../TODO.md)** - detailed problem analysis
2. **Use diagnostics**: `make doctor`, `make diagnose`
3. **Check quality gates**: `make validate`

### **For Development Support**

1. **Review architecture**: [../architecture/README.md](../architecture/README.md)
2. **Check API documentation**: [../api/README.md](../api/README.md)
3. **Examine existing patterns**: Study `base.py`, `core.py`, `execution.py`

### **Emergency Debugging**

```bash
# Quick problem identification
make type-check             # Shows type errors with line numbers
make test                   # Shows test failures with details
python scripts/flext_meltano_bridge.py version  # Shows import errors

# Environment debugging
poetry env info             # Show virtual environment info
poetry show                # Show installed packages
make deps-audit             # Check for security issues
```

---

**⚠️ IMPORTANT**: Development is **BLOCKED** until critical issues from [../TODO.md](../TODO.md) are resolved. All workflows above assume these fixes have been implemented.

**Last Updated**: 2025-08-01  
**Status**: Requires Critical Fixes Before Development  
**Next Action**: Implement `FlextMeltanoBridge` + fix type errors + resolve test failure
