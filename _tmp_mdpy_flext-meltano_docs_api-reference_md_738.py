# from flext-meltano_docs/api-reference.md:738
from __future__ import annotations


def execute_parallel_pipelines(
    self, pipelines: t.SequenceOf[FlextMeltanoModels.PipelineConfig]
) -> p.Result[Sequence[FlextMeltanoModels.PipelineResult]]:
    """Execute multiple pipelines in parallel.

    Args:
        pipelines: List of pipeline configurations

    Returns:
        r containing list of execution results

    """```
##### execute_conditional_pipeline(condition, pipeline)

**Execute pipeline based on condition**

