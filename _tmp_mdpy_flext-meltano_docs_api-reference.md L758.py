# from flext-meltano/docs/api-reference.md:758
from __future__ import annotations


def execute_conditional_pipeline(
    self,
    condition: FlextMeltanoModels.Condition,
    pipeline: FlextMeltanoModels.PipelineConfig,
) -> p.Result[FlextMeltanoModels.PipelineResult | None]:
    """Execute pipeline based on condition evaluation.

    Args:
        condition: Condition to evaluate
        pipeline: Pipeline to execute if condition is met

    Returns:
        r containing execution result or None

    """```
______________________________________________________________________

## 📁 Project Management

### FlextProjectService

**Meltano project management service**

