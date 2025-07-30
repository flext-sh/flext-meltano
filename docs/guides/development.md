# FLEXT Meltano Development Guide

Complete guide for developing with and contributing to FLEXT Meltano.

## 🚀 Development Environment Setup

### Prerequisites

- **Python 3.13**: Strict requirement
- **Poetry 1.8+**: Dependency management
- **Git**: Version control
- **Make**: Build automation

### Initial Setup

```bash
# Clone the repository
git clone <repository-url>
cd flext-meltano

# Complete development setup
make setup                   # Full setup with dependencies and hooks
make dev-install             # Development environment only
make pre-commit              # Setup pre-commit hooks only
```

### Verify Installation

```bash
# Check all quality gates
make validate                # Must pass before development

# Individual checks
make check                   # Essential checks
make lint                    # Code linting
make type-check              # Type safety
make test                    # Test suite with coverage
```

## 🏗️ Architecture Understanding

### Module Organization

Understand the flat module structure in `src/flext_meltano/`:

```
src/flext_meltano/
├── __init__.py                      # Public API (249 exports)
├── base.py                          # Foundation classes
├── core.py                          # Enterprise services
├── flext_meltano_execution.py       # Primary execution API
├── flext_meltano_cli.py            # CLI interface
├── flext_meltano_discovery.py      # Plugin discovery
├── flext_meltano_installation.py   # Plugin management
├── flext_meltano_validation.py     # Validation layer
└── flext_singer.py                 # Singer integration
```

### Key Design Patterns

1. **FlextResult Pattern**: All functions return `FlextResult` for consistent error handling
2. **Factory Pattern**: Use `create_*()` functions for object creation
3. **Subprocess Pattern**: All Meltano operations via subprocess execution
4. **Enterprise Integration**: Built on flext-core foundation patterns

## 🧪 Testing Strategy

### Test Organization

```
tests/
├── test_*.py                    # Main functionality tests
├── unit/                        # Unit tests (isolated)
├── integration/                 # Integration tests (real dependencies)
├── e2e/                         # End-to-end tests (full pipeline)
├── extensions/oracle_oic/       # Extension-specific tests
└── fixtures/                    # Test data and configuration
```

### Running Tests

```bash
# All tests with coverage
make test                        # 90% coverage required

# Specific test types
pytest -m unit                   # Unit tests only
pytest -m integration            # Integration tests only
pytest -m e2e                    # End-to-end tests only
pytest -m "not slow"             # Skip slow tests

# Specific test files
pytest tests/test_flext_meltano_execution.py -v
pytest tests/test_helpers_*.py -v

# Coverage reporting
make coverage                    # Generate HTML coverage report
```

### Writing Tests

#### Test Structure

```python
"""Test module following FLEXT testing patterns."""

import pytest
from flext_meltano.flext_meltano_execution import flext_meltano_execute_job


class TestFlextMeltanoExecution:
    """Test class for execution functionality."""

    def test_execute_job_success(self):
        """Test successful job execution."""
        # Arrange
        extractor = "tap-csv"
        loader = "target-csv"

        # Act
        result = flext_meltano_execute_job(extractor, loader)

        # Assert
        assert result.success
        assert result.output
        assert result.returncode == 0

    @pytest.mark.integration
    def test_execute_job_with_real_meltano(self):
        """Integration test with real Meltano."""
        # Implementation
        pass

    @pytest.mark.slow
    def test_large_pipeline_execution(self):
        """Slow test for large pipeline."""
        # Implementation
        pass
```

#### Test Markers

Use pytest markers for test organization:

```python
@pytest.mark.unit           # Unit test
@pytest.mark.integration    # Integration test
@pytest.mark.e2e           # End-to-end test
@pytest.mark.slow          # Slow test
@pytest.mark.core          # Core functionality
```

## 🛡️ Quality Standards

### Zero Tolerance Quality Gates

All code must pass these gates:

1. **Linting**: `make lint` (Ruff with ALL rules)
2. **Type Checking**: `make type-check` (MyPy strict mode)
3. **Security**: `make security` (Bandit + pip-audit)
4. **Testing**: `make test` (90%+ coverage)
5. **Pre-commit**: Automated checks on commit

### Code Style

#### Type Hints

```python
from typing import Any, Dict, List, Optional
from flext_core import FlextResult

def flext_meltano_execute_job(
    extractor: str,
    loader: str,
    *,
    environment: Optional[str] = None,
    **kwargs: Any,
) -> FlextResult[str]:
    """Execute Meltano pipeline job.

    Args:
        extractor: Meltano extractor plugin name
        loader: Meltano loader plugin name
        environment: Optional environment name
        **kwargs: Additional execution arguments

    Returns:
        FlextResult containing execution output or error
    """
    # Implementation
```

#### Error Handling

```python
from flext_core import FlextResult

def safe_operation() -> FlextResult[str]:
    """Example of proper error handling."""
    try:
        # Operation logic
        result = perform_operation()
        return FlextResult.success(result)
    except Exception as e:
        return FlextResult.failure(f"Operation failed: {e}")
```

#### Configuration Classes

```python
from pydantic import BaseModel, Field

class FlextMeltanoConfig(BaseModel):
    """Configuration with validation."""

    meltano_project_root: str = Field(default=".")
    environment: str = Field(default="dev")

    class Config:
        """Pydantic configuration."""
        frozen = True
        extra = "forbid"
```

## 🔧 Development Workflow

### Feature Development

1. **Create Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Write Tests First** (TDD approach)

   ```bash
   # Add tests to appropriate directory
   # Run tests to ensure they fail initially
   pytest tests/test_your_feature.py -v
   ```

3. **Implement Feature**

   - Follow existing patterns in the codebase
   - Use type hints throughout
   - Add proper docstrings
   - Handle errors with FlextResult pattern

4. **Run Quality Gates**

   ```bash
   make validate                # All gates must pass
   ```

5. **Update Documentation**

   - Update API docs if needed
   - Add examples for new functionality
   - Update README.md if necessary

6. **Test Bridge Integration** (if applicable)

   ```bash
   python scripts/flext_meltano_bridge.py your_operation
   ```

### Code Review Checklist

Before submitting:

- [ ] All quality gates pass (`make validate`)
- [ ] Tests added with 90%+ coverage
- [ ] Type hints added (MyPy compliant)
- [ ] Documentation updated
- [ ] Bridge integration tested (if applicable)
- [ ] Error handling follows FlextResult pattern
- [ ] Code follows existing patterns
- [ ] Security considerations addressed

### Debugging

#### Local Debugging

```python
# Add debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Use pdb for interactive debugging
import pdb; pdb.set_trace()

# Or use breakpoint() (Python 3.7+)
breakpoint()
```

#### Test Debugging

```bash
# Run tests with debugger
pytest tests/test_file.py::test_function --pdb

# Verbose output
pytest tests/test_file.py -v -s

# Show local variables on failure
pytest tests/test_file.py --tb=long

# Run only failed tests
pytest --lf
```

## 🌉 Bridge Integration Development

### Testing Bridge Functionality

```bash
# Test bridge script directly
python scripts/flext_meltano_bridge.py version

# Test with parameters
python scripts/flext_meltano_bridge.py run_pipeline tap-csv target-csv

# Test error handling
python scripts/flext_meltano_bridge.py invalid_operation
```

### Adding New Bridge Operations

1. **Add operation to bridge script**:

   ```python
   # In scripts/flext_meltano_bridge.py
   elif operation == "new_operation":
       result = bridge.new_operation(sys.argv[2])
   ```

2. **Implement in bridge class**:

   ```python
   # In the bridge class
   def new_operation(self, parameter: str) -> FlextMeltanoResult:
       """New bridge operation."""
       return flext_meltano_some_function(parameter)
   ```

3. **Test integration**:

   ```bash
   python scripts/flext_meltano_bridge.py new_operation test_param
   ```

## 📦 Build & Distribution

### Building the Package

```bash
# Clean previous builds
make clean

# Build distribution packages
make build

# Verify build
ls dist/
```

### Local Installation

```bash
# Install in development mode
pip install -e .

# Or using Poetry
poetry install
```

## 🚨 Troubleshooting Development Issues

### Common Problems

**Import Errors:**

```bash
# Ensure PYTHONPATH is set
export PYTHONPATH=$(pwd)/src:$PYTHONPATH

# Or add to shell profile
echo 'export PYTHONPATH=$(pwd)/src:$PYTHONPATH' >> ~/.bashrc
```

**Poetry Issues:**

```bash
# Clear cache and reinstall
poetry cache clear pypi --all
rm -rf .venv
poetry install --all-extras
```

**Pre-commit Failures:**

```bash
# Run pre-commit manually
pre-commit run --all-files

# Update hooks
pre-commit autoupdate
```

**Test Failures:**

```bash
# Clear test cache
pytest --cache-clear

# Reinstall test dependencies
poetry install --extras test
```

**Type Checking Issues:**

```bash
# Clear MyPy cache
rm -rf .mypy_cache

# Run with verbose output
mypy src/ --verbose
```

### Performance Profiling

```python
# Profile function execution
import cProfile
cProfile.run('your_function()')

# Memory profiling
from memory_profiler import profile

@profile
def your_function():
    # Function implementation
    pass
```

## 📚 Resources

### Documentation

- [Architecture Guide](../architecture/README.md)
- [API Reference](../api/README.md)
- [Quick Start](../examples/quick-start.md)

### External Resources

- [Meltano Documentation](https://docs.meltano.com/)
- [Singer SDK Documentation](https://sdk.meltano.com/)
- [DBT Documentation](https://docs.getdbt.com/)
- [Poetry Documentation](https://python-poetry.org/docs/)

### FLEXT Ecosystem

- `flext-core`: Foundation patterns and utilities
- `flext-observability`: Monitoring and metrics
- FlexCore service: Go runtime container
- FLEXT service: Data processing service

---

_Development Guide - Version 2.0.0-enterprise_
_Last Updated: 2025-01-29_
