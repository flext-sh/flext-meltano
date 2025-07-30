# FLEXT Meltano Quality Standards

Comprehensive quality standards and enforcement for the FLEXT Meltano enterprise library.

## 🛡️ Zero Tolerance Quality Gates

All code contributions **must pass** these quality gates before acceptance. No exceptions.

### 1. Linting (Ruff - ALL Rules)

```bash
make lint                    # Must pass with zero issues
poetry run ruff check src/ tests/ --fix --unsafe-fixes
```

**Enforcement:**

- **ALL** Ruff rules enabled (no cherry-picking)
- Zero warnings or errors tolerated
- Automatic fixes applied where possible
- Manual fixes required for complex issues

**Specific Rules:**

- Line length: 88 characters
- Import sorting: Combined as imports, split on trailing comma
- Docstring format: Google style
- Type annotations: Required for all functions

### 2. Type Checking (MyPy Strict Mode)

```bash
make type-check              # Must pass with zero errors
poetry run mypy src/ tests/ --strict
```

**Requirements:**

- **Strict mode** - no untyped definitions allowed
- All functions must have type hints
- No `Any` types except where absolutely necessary
- Generic types properly specified
- Return types explicit for all functions

**Example:**

```python
from typing import Optional, List, Dict, Any
from flext_core import FlextResult

def flext_meltano_execute_job(
    extractor: str,
    loader: str,
    *,
    environment: Optional[str] = None,
    **kwargs: Any,
) -> FlextResult[str]:
    """Execute Meltano pipeline job with proper typing."""
    # Implementation
```

### 3. Security Scanning

```bash
make security                # Must pass all scans
poetry run bandit -r src/ --severity-level medium --confidence-level medium
poetry run pip-audit --ignore-vuln PYSEC-2022-42969
```

**Security Requirements:**

- Bandit security scan with medium+ severity
- pip-audit for known vulnerabilities
- No hardcoded secrets or credentials
- Secure subprocess execution patterns
- Input validation for all external data

### 4. Test Coverage (90% Minimum)

```bash
make test                    # Must achieve 90%+ coverage
pytest tests/ --cov=src/flext_meltano --cov-fail-under=90
```

**Coverage Requirements:**

- **90% minimum** line coverage (enforced)
- Branch coverage tracking
- No coverage exclusions without justification
- All public APIs must be tested
- Bridge integration tests required

**Test Organization:**

```bash
pytest -m unit               # Unit tests (isolated)
pytest -m integration        # Integration tests (real dependencies)
pytest -m e2e               # End-to-end tests (full pipeline)
```

### 5. Pre-commit Hooks

```bash
make pre-commit              # Install and run hooks
pre-commit run --all-files   # Manual execution
```

**Automated Checks:**

- Code formatting (Ruff)
- Import sorting
- Trailing whitespace removal
- Large file detection
- Secret detection
- YAML/JSON validation

## 📊 Quality Metrics

### Code Quality Metrics

| Metric        | Requirement      | Current Status        |
| ------------- | ---------------- | --------------------- |
| Test Coverage | ≥90%             | ✅ Enforced           |
| Type Coverage | 100%             | ✅ MyPy Strict        |
| Linting       | Zero Issues      | ✅ ALL Rules          |
| Security      | No Medium+       | ✅ Bandit + pip-audit |
| Complexity    | <10 per function | ✅ Ruff C901          |

### Performance Standards

```python
# Function execution time limits
def performance_test():
    """Performance benchmarks."""
    # Bridge operations: <1s
    # Pipeline execution: <30s (depends on data)
    # CLI commands: <5s
    # Discovery operations: <10s
```

### Documentation Standards

- **API Documentation**: All public functions documented
- **Type Hints**: Complete type annotations
- **Examples**: Usage examples for all major features
- **Architecture**: Up-to-date architectural documentation
- **README**: Accurate project overview and quick start

## 🧪 Testing Standards

### Test Categories

#### Unit Tests (`pytest -m unit`)

```python
@pytest.mark.unit
def test_function_logic():
    """Test isolated function logic with mocks."""
    # Fast execution (<100ms per test)
    # No external dependencies
    # High coverage of edge cases
```

#### Integration Tests (`pytest -m integration`)

```python
@pytest.mark.integration
def test_meltano_integration():
    """Test with real Meltano CLI."""
    # Real subprocess execution
    # Actual Meltano operations
    # Moderate execution time (<5s per test)
```

#### End-to-End Tests (`pytest -m e2e`)

```python
@pytest.mark.e2e
def test_complete_pipeline():
    """Test complete pipeline execution."""
    # Full data pipeline
    # Real plugins and data
    # Longer execution time acceptable
```

### Test Quality Requirements

- **Descriptive Names**: Test function names describe what is being tested
- **AAA Pattern**: Arrange, Act, Assert structure
- **Isolation**: Tests don't depend on each other
- **Deterministic**: Tests produce consistent results
- **Fast Feedback**: Unit tests run quickly

## 🔧 Code Style Standards

### Python Code Style

#### Function Definitions

```python
def function_name(
    required_param: str,
    optional_param: Optional[int] = None,
    *,
    keyword_only: bool = False,
    **kwargs: Any,
) -> FlextResult[ReturnType]:
    """Function docstring following Google style.

    Args:
        required_param: Description of required parameter
        optional_param: Description of optional parameter
        keyword_only: Keyword-only parameter description
        **kwargs: Additional keyword arguments

    Returns:
        FlextResult containing the operation result

    Raises:
        ValueError: When invalid parameters are provided
    """
    # Implementation
```

#### Class Definitions

```python
class FlextMeltanoService:
    """Service class following enterprise patterns.

    This class provides enterprise-grade functionality for
    Meltano operations within the FLEXT ecosystem.

    Attributes:
        config: Service configuration
        logger: Structured logger instance
    """

    def __init__(self, config: FlextMeltanoConfig) -> None:
        """Initialize service with configuration."""
        self.config = config
        self.logger = structlog.get_logger(__name__)

    def public_method(self) -> FlextResult[str]:
        """Public method with proper typing and documentation."""
        # Implementation
```

#### Error Handling

```python
# Use FlextResult pattern for all operations
def safe_operation() -> FlextResult[str]:
    """Operation with proper error handling."""
    try:
        result = perform_operation()
        return FlextResult.success(result)
    except SpecificException as e:
        return FlextResult.failure(f"Specific error: {e}")
    except Exception as e:
        return FlextResult.failure(f"Unexpected error: {e}")
```

### Import Organization

```python
"""Module docstring."""

# Standard library imports
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

# Third-party imports
import pydantic
from meltano.core import Project

# FLEXT imports
from flext_core import FlextResult

# Local imports
from flext_meltano.base import FlextMeltanoConfig
```

## 🚀 Performance Standards

### Execution Time Limits

| Operation Type       | Maximum Time | Measurement              |
| -------------------- | ------------ | ------------------------ |
| Bridge Operations    | 1 second     | Response time            |
| CLI Commands         | 5 seconds    | Command execution        |
| Discovery Operations | 10 seconds   | Plugin/catalog discovery |
| Pipeline Execution   | Variable     | Depends on data volume   |

### Memory Usage

- **Base Memory**: <100MB for library import
- **Execution Memory**: <500MB for typical operations
- **Memory Leaks**: Zero tolerance for memory leaks
- **Garbage Collection**: Proper cleanup of resources

### Resource Optimization

```python
# Resource management patterns
import contextlib
from typing import Iterator

@contextlib.contextmanager
def managed_resource() -> Iterator[Resource]:
    """Context manager for proper resource cleanup."""
    resource = acquire_resource()
    try:
        yield resource
    finally:
        release_resource(resource)
```

## 🔒 Security Standards

### Input Validation

```python
from pydantic import BaseModel, validator

class InputModel(BaseModel):
    """Input validation model."""

    plugin_name: str

    @validator('plugin_name')
    def validate_plugin_name(cls, v):
        """Validate plugin name for security."""
        if not v.isalnum() and '-' not in v:
            raise ValueError("Invalid plugin name")
        return v
```

### Subprocess Security

```python
import subprocess
from typing import List

def secure_subprocess(command: List[str]) -> subprocess.CompletedProcess:
    """Secure subprocess execution."""
    # Validate command components
    validated_command = validate_command(command)

    # Execute with security measures
    return subprocess.run(
        validated_command,
        capture_output=True,
        text=True,
        check=False,
        timeout=300,  # Prevent hanging
        env=clean_environment(),  # Clean environment
    )
```

### Secret Management

- **No hardcoded secrets** in code
- **Environment variables** for configuration
- **Secret scanning** in pre-commit hooks
- **Audit logging** for sensitive operations

## 📋 Compliance Checklist

### Pre-commit Checklist

- [ ] All quality gates pass (`make validate`)
- [ ] Tests added for new functionality
- [ ] Type hints added to all functions
- [ ] Documentation updated
- [ ] Security considerations addressed
- [ ] Performance impact assessed
- [ ] Bridge integration tested (if applicable)

### Code Review Checklist

- [ ] Code follows established patterns
- [ ] Error handling uses FlextResult pattern
- [ ] Resource cleanup properly implemented
- [ ] Security best practices followed
- [ ] Performance requirements met
- [ ] Documentation is accurate and complete

### Release Checklist

- [ ] All quality gates pass on CI/CD
- [ ] Integration tests pass
- [ ] Documentation updated
- [ ] Version numbers updated
- [ ] Change log updated
- [ ] Security scan clean
- [ ] Performance benchmarks meet standards

## 🎯 Continuous Improvement

### Quality Metrics Tracking

```python
# Example quality tracking
QUALITY_METRICS = {
    "test_coverage": 95.2,  # Current coverage percentage
    "type_coverage": 100.0,  # MyPy coverage
    "security_issues": 0,    # Bandit findings
    "performance_score": 8.5, # Performance rating
}
```

### Regular Reviews

- **Weekly**: Quality metrics review
- **Monthly**: Standards update review
- **Quarterly**: Performance benchmark review
- **Semi-annually**: Security audit

### Tool Updates

- **Ruff**: Latest version for new rule categories
- **MyPy**: Latest version for improved type checking
- **Bandit**: Updated security patterns
- **pytest**: Latest testing features

---

_Quality Standards - Version 2.0.0-enterprise_
_Last Updated: 2025-01-29_
_Enforced by: Zero Tolerance Policy_
