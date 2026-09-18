# from flext-meltano/docs/architecture/system-context.md:385
from __future__ import annotations
# External system integration via adapters
class ExternalSystemAdapter(Protocol):
    """Protocol for external system adapters."""

    def connect(self) -> p.Result[Connection]:
        """Establish connection to external system."""
        ...

    def execute_operation(self, operation: Operation) -> p.Result[Result]:
        """Execute operation on external system."""
        ...

    def disconnect(self) -> p.Result[bool]:
        """Clean up connection to external system."""
        ...

# Concrete adapter implementations
class MeltanoAdapter(ExternalSystemAdapter):
    """Meltano CLI adapter."""

class FlextMeltanoAdapter.Dbt(ExternalSystemAdapter):
    """DBT adapter."""

class FlextMeltanoAdapter.Singer(ExternalSystemAdapter):
    """Singer protocol adapter."""```
#### Plugin Architecture for Extensibility

