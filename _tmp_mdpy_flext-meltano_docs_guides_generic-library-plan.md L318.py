# from flext-meltano/docs/guides/generic-library-plan.md:318
from __future__ import annotations


def execute_pipeline(
    pipeline: Pipeline | str, options: PipelineOptions | None = None
) -> p.Result[PipelineResult]:
    """Execute configured pipeline.

    Args:
        pipeline: Pipeline configuration or pipeline name
        options: Execution options (parallelism, retries, etc.)

    Returns:
        Execution result with timing and statistics

    """```
## Migration Plan

### Backward Compatibility Strategy

**Maintain Compatibility:**

- Existing CLI integration continues to work
- Meltano project support preserved
- Plugin installation through existing methods
- Configuration file compatibility maintained

**New Generic APIs:**

- `FlextMeltanoService` for generic operations
- `FlextPluginService` for plugin management
- `FlextSingerService` for protocol operations
- `FlextMeltanoService` for orchestration

### Testing Strategy

#### Compatibility Testing

