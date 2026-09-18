# from flext-meltano_docs/api-reference.md:486
from __future__ import annotations


class FlextPluginService(s):
    """Service for plugin lifecycle management and operations."""

    def __init__(self, project_root: Path | str | None = None) -> None:
        """Initialize plugin service."""```
#### Plugin Lifecycle

##### discover_plugins()

**Discover all plugins in the project**

