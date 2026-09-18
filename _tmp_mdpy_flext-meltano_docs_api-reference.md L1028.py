# from flext-meltano/docs/api-reference.md:1028
from __future__ import annotations


class TargetExecutionResult(FlextBaseModel):
    """Target execution result model."""

    success: bool
    records_loaded: int = 0
    execution_time: float = 0.0
    error: str | None = None```
#### FlextMeltanoModels.PipelineResult

**Pipeline execution result model**

