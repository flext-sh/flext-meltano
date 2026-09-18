# from flext-meltano_docs/api-reference.md:291
from __future__ import annotations


def execute_pipeline_advanced(
    self, options: FlextMeltanoModels.PipelineOptions
) -> p.Result[FlextMeltanoModels.PipelineResult]:
    """Execute pipeline with advanced configuration options.

    Args:
        options: Advanced pipeline execution options

    Returns:
        r containing execution result

    """```
##### execute_parallel_pipelines(pipelines)

**Execute multiple pipelines in parallel**

