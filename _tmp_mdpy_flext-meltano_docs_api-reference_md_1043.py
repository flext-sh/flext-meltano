# from flext-meltano_docs/api-reference.md:1043
from __future__ import annotations


class PipelineResult(FlextBaseModel):
    """Pipeline execution result model."""

    success: bool
    tap_result: TapExecutionResult | None = None
    target_result: TargetExecutionResult | None = None
    transformer_result: m.Dict | None = None
    execution_time: float = 0.0
    error: str | None = None```
______________________________________________________________________

## 🛡️ Exception Hierarchy

### FlextMeltanoException

**Base exception for FLEXT-Meltano**

