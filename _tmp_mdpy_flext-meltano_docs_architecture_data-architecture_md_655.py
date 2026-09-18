# from flext-meltano_docs/architecture/data-architecture.md:655
from __future__ import annotations


@dataclass
class AlertRule:
    """Monitoring alert configuration."""

    metric_name: str
    condition: str  # '>', '<', '==', '!='
    threshold: float
    severity: str  # 'info', 'warning', 'error', 'critical'
    cooldown_minutes: int

    def should_alert(self, current_value: float, last_alert: datetime) -> bool:
        """Determine if alert should be triggered."""
        condition_met = self._check_condition(current_value)
        cooldown_expired = self._is_cooldown_expired(last_alert)

        return condition_met and cooldown_expired```
______________________________________________________________________

## 📈 Architecture Evolution

### Current Limitations

- Single-threaded processing for some operations
- Memory-bound for very large datasets
- Limited support for complex data transformations
- Basic error recovery mechanisms

### Future Enhancements

- **Streaming Architecture**: Real-time data processing
- **Distributed Processing**: Cluster-based execution
- **Advanced Caching**: Multi-level caching strategies
- **AI/ML Integration**: Intelligent data quality assessment
- **Event-Driven Processing**: Asynchronous pipeline execution

______________________________________________________________________

**Data Architecture**: FLEXT-Meltano Enterprise Data Processing
_Comprehensive data flow, storage, and processing architecture documentation_
