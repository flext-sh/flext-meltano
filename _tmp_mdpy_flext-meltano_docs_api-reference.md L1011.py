# from flext-meltano/docs/api-reference.md:1011
from __future__ import annotations


class TapExecutionResult(FlextBaseModel):
    """Tap execution result model."""

    success: bool
    records_extracted: int = 0
    streams_discovered: int = 0
    execution_time: float = 0.0
    state: m.Dict | None = None
    error: str | None = None```
#### FlextMeltanoModels.TargetExecutionResult

**Target execution result model**

