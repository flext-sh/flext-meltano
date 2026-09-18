# from flext-meltano_docs/api-reference.md:991
from __future__ import annotations


class PipelineConfig(FlextBaseModel):
    """Pipeline configuration model."""

    name: str
    tap: str
    target: str | None = None
    transformer: str | None = None
    schedule: str | None = None
    incremental: bool = False
    parallelism: int = 1```
### Execution Models

#### FlextMeltanoModels.TapExecutionResult

**Tap execution result model**

