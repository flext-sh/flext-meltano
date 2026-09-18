# from flext-meltano_docs/api-reference.md:222
from __future__ import annotations


def run_pipeline(
    self, tap_name: str, target_name: str, settings: m.Dict | None = None
) -> p.Result[FlextMeltanoModels.PipelineResult]:
    """Execute complete ELT pipeline from tap to target.

    Args:
        tap_name: Name of the tap to execute
        target_name: Name of the target to execute
        settings: Pipeline configuration dictionary

    Returns:
        r containing pipeline execution result

    """```
##### validate_project()

**Validate Meltano project configuration**

