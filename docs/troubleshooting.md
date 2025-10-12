# Troubleshooting flext-meltano

**Common issues and solutions** for flext-meltano development and usage.

---

## 🚨 Architecture Compliance Issues

### **Direct Import Violations**

**Problem**: Direct `meltano.core.*` imports in source code

```bash
# Check for violations
grep -r "import meltano\|from meltano" src/
```

**Solution**: Use flext-meltano abstractions only

```python
# ❌ Incorrect
from meltano.core.project import Project

# ✅ Correct
from flext_meltano import FlextMeltanoAdapter
```

---

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

```python
# Ensure proper type hints
from typing import Optional
from flext_core import FlextCore

def process_data(data: dict) -> FlextCore.Result[Optional[FlextCore.Types.Dict]]:
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
2. **Environment setup**: Activate correct virtual environment
3. **Dependencies**: Run `poetry install --with dev,test`

---

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

---

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
2. **Error Handling**: Test FlextCore.Result error paths
3. **Integration Points**: Test abstractions with real scenarios

### **Slow Tests**

**Problem**: Test suite running slowly

```bash
# Skip slow tests during development
pytest -m "not slow"

# Run only unit tests
pytest tests/unit/
```

---

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

---

## 🚫 Common Mistakes

### **FlextCore.Result Pattern Violations**

**Problem**: Not using FlextCore.Result for error handling

```python
# ❌ Incorrect
def risky_operation():
    try:
        # operation
        return data
    except Exception as e:
        return None  # Lost error information

# ✅ Correct
def safe_operation() -> FlextCore.Result[FlextCore.Types.Dict]:
    try:
        # operation
        return FlextCore.Result.ok(data)
    except Exception as e:
        return FlextCore.Result.fail(f"Operation failed: {e}")
```

### **Service Pattern Violations**

**Problem**: Not following flext-core service patterns

```python
# ❌ Incorrect
class UtilityClass:
    @staticmethod
    def do_something():
        pass

# ✅ Correct
from flext_core import FlextCore

class FlextMeltanoUtilityService(FlextCore.Service):
    def do_something(self) -> FlextCore.Result[FlextCore.Types.Dict]:
        # Implementation with proper error handling
        pass
```

---

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
make validate 2>&1 | head -50
```

### **Support Channels**

- **Documentation**: Check [docs/](../docs/) first
- **Issues**: [GitHub Issues](https://github.com/flext-sh/flext/issues)
- **Architecture**: Review [architecture.md](architecture.md)

---

## 📋 Debugging Checklist

Before reporting issues:

- [ ] Verified correct virtual environment is active
- [ ] Ran `poetry install --with dev,test`
- [ ] Checked for direct import violations
- [ ] Ran `make validate` to identify issues
- [ ] Reviewed error messages carefully
- [ ] Checked documentation for similar issues

---

**Need more help?** Check the [Development Guide](development.md) for detailed contributing guidelines.
