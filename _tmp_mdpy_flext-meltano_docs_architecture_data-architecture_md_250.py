# from flext-meltano_docs/architecture/data-architecture.md:250
from __future__ import annotations


class ErrorStore:
    """Storage for failed records and error context."""

    errors: List[ErrorRecord]

    @dataclass
    class ErrorRecord:
        record: dict
        error_message: str
        timestamp: datetime
        retry_count: int
        pipeline_stage: str```
______________________________________________________________________

## 📊 Data Models and Schemas

### Core Data Models

#### Pipeline Configuration Model

