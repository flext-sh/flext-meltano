# from flext-meltano_docs/guides/generic-library-plan.md:280
from __future__ import annotations


def execute_target(
    target_name: str, records: t.SequenceOf[m.Dict], settings: m.Dict
) -> p.Result[TargetExecutionResult]:
    """Execute Singer target with records.

    Args:
        target_name: Name of the target to execute
        records: Records to load into the target
        settings: Target configuration dictionary

    Returns:
        Execution result with load statistics

    """```
### Pipeline Orchestration API

#### Pipeline Configuration API

