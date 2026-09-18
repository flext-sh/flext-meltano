# from flext-meltano_docs/api-reference.md:207
from __future__ import annotations


class FlextMeltanoAdapter(s):
    """Adapter for Meltano CLI integration and execution."""

    def __init__(self, project_root: Path | str | None = None) -> None:
        """Initialize Meltano adapter."""```
#### Pipeline Operations

##### run_pipeline(tap_name, target_name, settings=None)

**Execute complete ELT pipeline**

