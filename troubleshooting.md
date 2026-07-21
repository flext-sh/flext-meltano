# Troubleshooting flext-meltano

<!-- TOC START -->
- [🚨 Architecture Compliance Issues](#architecture-compliance-issues)
  - [**Direct Import Violations**](#direct-import-violations)
- [🔧 Development Issues](#development-issues)
  - [**Import Errors**](#import-errors)
  - [**Type Check Failures**](#type-check-failures)
  - [**Test Failures**](#test-failures)
- [📦 Dependency Issues](#dependency-issues)
  - [**Poetry Lock Conflicts**](#poetry-lock-conflicts)
  - [**Virtual Environment Issues**](#virtual-environment-issues)
- [🧪 Testing Issues](#testing-issues)
  - [**Coverage Issues**](#coverage-issues)
  - [**Slow Tests**](#slow-tests)
- [🔍 Quality Gate Failures](#quality-gate-failures)
  - [**Linting Errors**](#linting-errors)
  - [**Security Issues**](#security-issues)
- [🚫 Common Mistakes](#common-mistakes)
  - [**r Pattern Violations**](#r-pattern-violations)
  - [**Service Pattern Violations**](#service-pattern-violations)
- [🆘 Getting Help](#getting-help)
  - [**Debug Information**](#debug-information)
  - [**Support Channels**](#support-channels)
- [📋 Debugging Checklist](#debugging-checklist)
<!-- TOC END -->

**Common issues and solutions** for flext-meltano development and usage.

______________________________________________________________________

## 🚨 Architecture Compliance Issues

### **Direct Import Violations**

**Problem**: Direct `meltano.core.*` imports in source code

```bash
# Check for violations
grep -r "import meltano\|from meltano" src/
```

**Solution**: Use flext-meltano abstractions only

```python notest
# ❌ Incorrect
from meltano.core.project import Project

# ✅ Correct
from flext_meltano import FlextMeltanoAdapter
```

______________________________________________________________________

## 🔧 Development Issues

### **Import Errors**

**Problem**: Module import failures

```
ImportError: cannot import name 'FlextMeltanoService' from 'flext_meltano'
```

**Solution**: Verify installation and environment

```bash
# Check installation
python -c "import flext_meltano; print(flext_meltano.__file__)"

# Reinstall if needed
poetry install --with dev,test
```

### **Type Check Failures**

**Problem**: MyPy errors in source code

```bash
# Run type checking
make type-check
```

**Solution**: Fix type annotations

```python notest
# Ensure proper type hints
from typing import Optional
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u


def process_data(data: dict) -> p.Result[Optional[m.Dict]]:
    # Implementation
    pass
```

### **Test Failures**

**Problem**: Tests failing during development

```bash
# Run tests with verbose output
pytest tests/ -v

# Run specific test categories
pytest tests/unit/ -v        # Unit tests only
pytest tests/integration/ -v  # Integration tests
```

**Solution**: Common test issues

1. **Missing test data**: Ensure test fixtures are available
1. **Environment setup**: Activate correct virtual environment
1. **Dependencies**: Run `poetry install --with dev,test`

______________________________________________________________________

## 📦 Dependency Issues

### **Poetry Lock Conflicts**

**Problem**: Dependency version conflicts

```bash
# Update dependencies
poetry update

# Resolve lock file issues
poetry lock --no-update
```

### **Virtual Environment Issues**

**Problem**: Wrong virtual environment or missing dependencies

```bash
# Verify environment
which python
python -m pip list | grep flext

# Use FLEXT workspace environment
cd ../..
source .venv/bin/activate
cd flext-meltano
```

______________________________________________________________________

## 🧪 Testing Issues

### **Coverage Issues**

**Problem**: Low test coverage or coverage failures

```bash
# Generate detailed coverage report
pytest --cov=src --cov-report=html

# View HTML report
open htmlcov/index.html
```

**Solution**: Focus on critical paths

1. **Core Services**: Ensure service classes have test coverage
1. **Error Handling**: Test r error paths
1. **Integration Points**: Test abstractions with real scenarios

### **Slow Tests**

**Problem**: Test suite running slowly

```bash
# Skip slow tests during development
pytest -m "not slow"

# Run only unit tests
pytest tests/unit/
```

______________________________________________________________________

## 🔍 Quality Gate Failures

### **Linting Errors**

**Problem**: Ruff linting failures

```bash
# Fix auto-fixable issues
make format

# Check remaining issues
make lint
```

**Common fixes**:

- **Import order**: Use ruff to auto-sort imports
- **Line length**: Break long lines appropriately
- **Unused imports**: Remove or add `# noqa` if intentional

### **Security Issues**

**Problem**: Bandit security warnings

```bash
# Run security scan
bandit -r src/

# Check specific issues
bandit -r src/ -f json
```

**Solution**: Address security concerns

- **Hardcoded passwords**: Use environment variables
- **SQL injection**: Use parameterized queries
- **Path traversal**: Validate file paths

______________________________________________________________________

## 🚫 Common Mistakes

### **r Pattern Violations**

**Problem**: Not using r for error handling

```python notest
# ❌ Incorrect
def risky_operation():
    try:
        # operation
        return data
    except Exception as e:
        return None  # Lost error information


# ✅ Correct
def safe_operation() -> p.Result[m.Dict]:
    try:
        # operation
        return r.ok(data)
    except Exception as e:
        return r.fail(f"Operation failed: {e}")
```

### **Service Pattern Violations**

**Problem**: Not following flext-core service patterns

```python notest
# ❌ Incorrect
class UtilityClass:
    @staticmethod
    def do_something():
        pass


# ✅ Correct
from flext_core import FlextBus
from flext_core import FlextSettings
from flext_core import FlextConstants
from flext_core import FlextContainer
from flext_core import FlextContext
from flext_core import d
from flext_core import FlextDispatcher
from flext_core import e
from flext_core import h
from flext_core import x
from flext_core import FlextModels
from flext_core import FlextProcessors
from flext_core import p
from flext_core import FlextRegistry
from flext_core import r, p
from flext_core import u
from flext_core import s
from flext_core import t
from flext_core import u


class FlextMeltanoUtilityService(s):
    def do_something(self) -> p.Result[m.Dict]:
        # Implementation with proper error handling
        pass
```

______________________________________________________________________

## 🆘 Getting Help

### **Debug Information**

When reporting issues, include:

```bash
# Environment information
python --version
poetry --version

# Package versions
poetry show flext-core flext-meltano

# Error details
make val 2>&1 | head -50
```

### **Support Channels**

- **Documentation**: Check [docs/](../docs/) first
- **Issues**: [GitHub Issues](https://github.com/flext-sh/flext/issues)
- **Architecture**: Review [architecture.md](architecture.md)

______________________________________________________________________

## 📋 Debugging Checklist

Before reporting issues:

- [ ] Verified correct virtual environment is active
- [ ] Ran `poetry install --with dev,test`
- [ ] Checked for direct import violations
- [ ] Ran `make val` to identify issues
- [ ] Reviewed error messages carefully
- [ ] Checked documentation for similar issues

______________________________________________________________________

**Need more help?** Check the [Development Guide](development.md) for detailed contributing guidelines.
