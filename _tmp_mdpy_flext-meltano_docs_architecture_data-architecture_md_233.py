# from flext-meltano_docs/architecture/data-architecture.md:233
from __future__ import annotations


class RecordBuffer:
    """In-memory buffer for batch processing."""

    records: List[dict]
    max_size: int
    flush_threshold: float

    def add_record(self, record: dict) -> bool:
        """Add record to buffer, return True if flush needed."""
        self.records.append(record)
        return len(self.records) >= self.max_size * self.flush_threshold```
#### 3. **Error Handling Storage**

