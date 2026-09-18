# from flext-meltano_docs/guides/generic-library-plan.md:256
from __future__ import annotations


def execute_tap(
    tap_name: str,
    settings: m.Dict,
    state: m.Dict | None = None,
    streams: t.StringList | None = None,
) -> p.Result[TapExecutionResult]:
    """Execute Singer tap with configuration.

    Args:
        tap_name: Name of the tap to execute
        settings: Tap configuration dictionary
        state: Initial state for incremental sync
        streams: Specific streams to sync

    Returns:
        Execution result with records and state

    """```
#### Target Execution API

