# from flext-meltano/docs/architecture/data-architecture.md:546
from __future__ import annotations


@dataclass
class RetentionPolicy:
    """Data retention policy configuration."""

    data_type: str
    retention_period_days: int
    archive_strategy: str  # 'delete', 'archive', 'anonymize'
    compliance_requirements: t.StringList

    def should_retain(self, data_age_days: int) -> bool:
        """Determine if data should be retained."""
        return data_age_days <= self.retention_period_days

    def get_archive_action(self) -> str:
        """Get appropriate archive action."""
        return self.archive_strategy```
______________________________________________________________________

## ⚡ Performance and Scalability

### Performance Characteristics

| Operation                  | Target Latency | Throughput    | Scaling Strategy   |
| -------------------------- | -------------- | ------------- | ------------------ |
| **Schema Discovery**       | \<30s          | N/A           | Parallel discovery |
| **Data Extraction**        | \<5min         | 1000 rec/sec  | Horizontal scaling |
| **Data Loading**           | \<10min        | 5000 rec/sec  | Batch optimization |
| **DBT Transformation**     | \<15min        | Variable      | Query optimization |
| **Pipeline Orchestration** | \<1min         | 10 concurrent | Load balancing     |

### Scalability Patterns

#### 1. **Horizontal Scaling**

