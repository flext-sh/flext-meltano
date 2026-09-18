# from flext-meltano_docs/api-reference.md:335
from __future__ import annotations


class FlextSingerTap(s):
    """Singer tap implementation with discovery, sync, and state management."""

    def __init__(
        self, tap_name: str, settings: m.Dict, state: m.Dict | None = None
    ) -> None:
        """Initialize Singer tap.

        Args:
            tap_name: Name of the tap plugin
            settings: Tap configuration dictionary
            state: Initial state for incremental sync

        """```
#### Tap Operations

##### discover()

**Discover Singer catalog for the tap**

