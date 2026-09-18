# from flext-meltano/docs/api-reference.md:182
from __future__ import annotations


def execute_target(
    self,
    target_name: str,
    records: t.SequenceOf[m.Dict],
    settings: m.Dict | None = None,
) -> p.Result[FlextMeltanoModels.TargetExecutionResult]:
    """Execute a Singer target with records.

    Args:
        target_name: Name of the target to execute
        records: List of records to load
        settings: Target configuration dictionary

    Returns:
        r containing execution result or error

    """```
### FlextMeltanoAdapter

**Meltano CLI integration and execution adapter**

