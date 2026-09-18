# from flext-meltano/docs/architecture/data-architecture.md:624
from __future__ import annotations


class PipelineCache:
    """Multi-level caching for performance optimization."""

    def __init__(self):
        self.schema_cache = {}  # Schema metadata cache
        self.config_cache = {}  # Configuration cache
        self.result_cache = {}  # Computation result cache

    def get_cached_schema(self, stream_name: str) -> Optional[dict]:
        """Get cached schema with TTL validation."""
        if stream_name in self.schema_cache:
            cached_item = self.schema_cache[stream_name]
            if not self._is_expired(cached_item):
                return cached_item["schema"]
        return None```
### Monitoring and Observability

#### Key Metrics

- **Throughput**: Records processed per second
- **Latency**: End-to-end pipeline execution time
- **Error Rate**: Percentage of failed operations
- **Resource Usage**: CPU, memory, disk I/O
- **Data Quality**: Validation success rate

#### Alerting Rules

