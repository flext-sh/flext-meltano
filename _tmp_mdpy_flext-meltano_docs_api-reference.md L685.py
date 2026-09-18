# from flext-meltano/docs/api-reference.md:685
from __future__ import annotations


def execute_pipeline(
    self, pipeline_name: str, options: FlextMeltanoModels.PipelineOptions | None = None
) -> p.Result[FlextMeltanoModels.PipelineResult]:
    """Execute a configured pipeline.

    Args:
        pipeline_name: Name of the pipeline to execute
        options: Execution options

    Returns:
        r containing execution result

    """```
##### monitor_pipeline(pipeline_id)

**Monitor pipeline execution**

