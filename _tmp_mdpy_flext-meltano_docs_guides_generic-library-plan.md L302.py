# from flext-meltano/docs/guides/generic-library-plan.md:302
from __future__ import annotations


def create_pipeline(settings: PipelineConfig) -> p.Result[Pipeline]:
    """Create pipeline configuration.

    Args:
        settings: Pipeline configuration with tap/target/transformer

    Returns:
        Configured pipeline ready for execution

    """```
#### Pipeline Execution API

