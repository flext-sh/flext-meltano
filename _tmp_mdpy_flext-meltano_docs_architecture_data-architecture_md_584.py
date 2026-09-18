# from flext-meltano_docs/architecture/data-architecture.md:584
from __future__ import annotations


class PipelineScaler:
    """Dynamic pipeline scaling based on workload."""

    def scale_pipeline(
        self, pipeline: Pipeline, metrics: SystemMetrics
    ) -> ScalingDecision:
        """Determine scaling requirements."""
        if metrics.queue_depth > self.queue_threshold:
            return ScalingDecision(scale_up=True, instances=2)
        if metrics.cpu_usage < self.cpu_threshold:
            return ScalingDecision(
                scale_down=True, instances=max(1, current_instances - 1)
            )
        return ScalingDecision(scale_up=False, scale_down=False)```
#### 2. **Data Partitioning**

