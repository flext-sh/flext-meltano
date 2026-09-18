# from flext-meltano_docs/api-reference.md:432
from __future__ import annotations


def load_records(
    self, records: t.SequenceOf[m.Dict]
) -> p.Result[FlextMeltanoModels.LoadResult]:
    """Load records into the target.

    Args:
        records: List of records to load

    Returns:
        r containing load result or error

    """```
##### flush()

**Flush any buffered records**

