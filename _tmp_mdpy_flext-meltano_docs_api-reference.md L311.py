# from flext-meltano/docs/api-reference.md:311
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
______________________________________________________________________

## 🔌 Singer Protocol Abstractions

### FlextSingerTap

**Singer tap implementation with enterprise features**

