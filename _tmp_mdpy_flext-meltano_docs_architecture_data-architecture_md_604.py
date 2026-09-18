# from flext-meltano_docs/architecture/data-architecture.md:604
from __future__ import annotations


class DataPartitioner:
    """Intelligent data partitioning for parallel processing."""

    def partition_data(
        self, records: List[dict], partition_key: str
    ) -> Dict[str, List[dict]]:
        """Partition data for parallel processing."""
        partitions = defaultdict(list)

        for record in records:
            key = record.get(partition_key, "default")
            partitions[key].append(record)

        return t.JsonMapping(partitions)```
#### 3. **Caching Strategy**

