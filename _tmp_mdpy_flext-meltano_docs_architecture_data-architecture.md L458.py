# from flext-meltano/docs/architecture/data-architecture.md:458
from __future__ import annotations


class DataQualityMetrics:
    """Track data quality throughout pipeline."""

    def __init__(self):
        self.total_records = 0
        self.valid_records = 0
        self.invalid_records = 0
        self.duplicate_records = 0
        self.schema_errors = 0
        self.business_rule_violations = 0

    def calculate_quality_score(self) -> float:
        """Calculate overall data quality score."""
        if self.total_records == 0:
            return 100.0

        valid_percentage = (self.valid_records / self.total_records) * 100
        error_penalty = min((self.invalid_records / self.total_records) * 50, 25)

        return max(0, valid_percentage - error_penalty)```
### Error Handling Strategies

#### 1. **Schema Validation Errors**

- Log error details with record context
- Continue processing other records
- Aggregate error statistics
- Optional: Store invalid records in error table

#### 2. **Business Rule Violations**

- Categorize violation types
- Apply configurable actions (reject/warn/transform)
- Maintain violation audit trail
- Support rule configuration updates

#### 3. **System Errors**

- Implement retry logic with exponential backoff
- Circuit breaker pattern for external systems
- Graceful degradation strategies
- Alert escalation for critical failures

______________________________________________________________________

## 🎯 Data Governance

### Data Lineage Tracking

