# from flext-meltano_docs/api-reference.md:160
from __future__ import annotations


def execute_tap(
    self, tap_name: str, settings: m.Dict | None = None, state: m.Dict | None = None
) -> p.Result[FlextMeltanoModels.TapExecutionResult]:
    """Execute a Singer tap with configuration and state.

    Args:
        tap_name: Name of the tap to execute
        settings: Tap configuration dictionary
        state: Tap state dictionary for incremental sync

    Returns:
        r containing execution result or error

    """```
##### execute_target(target_name, records, settings=None)

**Execute a Singer target**

