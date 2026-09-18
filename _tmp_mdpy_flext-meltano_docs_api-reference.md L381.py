# from flext-meltano/docs/api-reference.md:381
from __future__ import annotations


def sync(
    self, streams: t.StringList | None = None, state: m.Dict | None = None
) -> p.Result[FlextMeltanoModels.SyncResult]:
    """Execute tap synchronization.

    Args:
        streams: List of streams to sync (None for all)
        state: State dictionary for incremental sync

    Returns:
        r containing sync result or error

    """```
##### validate_config()

**Validate tap configuration**

