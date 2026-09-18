# from flext-meltano/docs/api-reference.md:706
from __future__ import annotations


def monitor_pipeline(
    self, pipeline_id: str
) -> p.Result[FlextMeltanoModels.PipelineStatus]:
    """Monitor pipeline execution status.

    Args:
        pipeline_id: ID of the pipeline to monitor

    Returns:
        r containing pipeline status

    """```
### FlextMeltanoExecutor

**Advanced pipeline execution engine**

