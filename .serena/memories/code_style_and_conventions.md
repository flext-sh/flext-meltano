# FLEXT Code Style and Conventions

## Mandatory Rules (Zero Tolerance)

- **Python 3.13+** and **Pydantic v2** only
- **One class per module** - unified classes with nested helpers
- **No helper functions outside classes** - use nested classes
- **No try/except fallback mechanisms** - use explicit FlextResult
- **No # type: ignore** without specific error codes
- **No object types** - use proper type annotations

## Import Strategy (ROOT-LEVEL ONLY)

```python
# ✅ CORRECT
from flext_core import (
    FlextResult, FlextLogger, FlextContainer,
    FlextModels, FlextConfig, FlextConstants,
    FlextUtilities, FlextService
)
from flext_cli import FlextCli, FlextCliCommands  # CLI projects only

# ❌ FORBIDDEN
from flext_core.result import FlextResult  # Internal imports prohibited
import click  # Direct CLI imports prohibited - use flext-cli
import rich  # Direct Rich imports prohibited - use flext-cli
```

## Class Structure Pattern

```python
class UnifiedProjectService(FlextService):
    """Single responsibility class with nested helpers."""

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._container = FlextContainer.get_global()
        self._logger = FlextLogger(__name__)

    class _ValidationHelper:
        """Nested helper class - no loose functions."""
        @staticmethod
        def validate_business_rules(data: dict) -> FlextResult[dict]:
            pass
```

## Error Handling Pattern

- **ALL operations return FlextResult[T]**
- **Use .unwrap() for safe extraction**
- **Use .is_failure for checks**
- **NO try/except fallbacks**

## Naming Conventions

- **FlextXxx prefix** for all public exports
- **Descriptive names** in English
- **No abbreviations** unless well-established
- **PascalCase** for classes
- **snake_case** for functions and variables

## Docstrings

- **Google style** for all public APIs
- **Required for ALL public APIs**
- **Include examples** for complex functions
- **Professional English** throughout
