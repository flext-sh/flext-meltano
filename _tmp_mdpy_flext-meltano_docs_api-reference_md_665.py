# from flext-meltano_docs/api-reference.md:665
from __future__ import annotations


def create_pipeline(
    self, settings: FlextMeltanoModels.PipelineConfig
) -> p.Result[FlextMeltanoModels.Pipeline]:
    """Create a new pipeline configuration.

    Args:
        settings: Pipeline configuration

    Returns:
        r containing created pipeline

    """```
##### execute_pipeline(pipeline_name, options=None)

**Execute a configured pipeline**

