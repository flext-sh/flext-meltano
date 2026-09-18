# from flext-meltano/docs/architecture/quality-attributes.md:439
from __future__ import annotations


class PerformanceMonitor:
    """Comprehensive performance monitoring and alerting."""

    def __init__(self, metrics_collector, alert_manager):
        self.metrics = metrics_collector
        self.alerts = alert_manager
        self.performance_thresholds = {
            "api_response_time": 1000,  # ms
            "pipeline_execution_time": 600000,  # 10 minutes
            "memory_usage": 0.8,  # 80%
            "cpu_usage": 0.8,  # 80%
            "error_rate": 0.05,  # 5%
        }

    def record_api_call(
        self, endpoint: str, response_time: float, status_code: int
    ) -> None:
        """Record API call performance metrics."""
        # Record response time
        self.metrics.histogram(
            "api_response_time",
            response_time,
            tags={"endpoint": endpoint, "status": status_code},
        )

        # Check thresholds
        if response_time > self.performance_thresholds["api_response_time"]:
            self.alerts.send_alert(
                "SlowAPIResponse",
                f"API {endpoint} response time: {response_time:.2f}ms",
                severity="warning",
            )

        # Record success/failure rates
        if status_code >= 400:
            self.metrics.increment("api_errors", tags={"endpoint": endpoint})

    def monitor_pipeline_execution(
        self, pipeline_id: str, execution_time: float, success: bool
    ) -> None:
        """Monitor pipeline execution performance."""
        # Record execution time
        self.metrics.histogram(
            "pipeline_execution_time",
            execution_time,
            tags={"pipeline_id": pipeline_id, "success": success},
        )

        # Check for slow pipelines
        if execution_time > self.performance_thresholds["pipeline_execution_time"]:
            self.alerts.send_alert(
                "SlowPipelineExecution",
                f"Pipeline {pipeline_id} took {execution_time / 1000:.1f}s",
                severity="warning",
            )

        # Track success rates
        self.metrics.increment("pipeline_executions", tags={"success": success})

    def monitor_resource_usage(self) -> None:
        """Monitor system resource usage."""
        import psutil

        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        self.metrics.gauge("cpu_usage_percent", cpu_percent)

        if cpu_percent > self.performance_thresholds["cpu_usage"] * 100:
            self.alerts.send_alert(
                "HighCPUUsage", f"CPU usage: {cpu_percent:.1f}%", severity="warning"
            )

        # Memory usage
        memory = psutil.virtual_memory()
        memory_percent = memory.percent
        self.metrics.gauge("memory_usage_percent", memory_percent)

        if memory_percent > self.performance_thresholds["memory_usage"] * 100:
            self.alerts.send_alert(
                "HighMemoryUsage",
                f"Memory usage: {memory_percent:.1f}%",
                severity="warning",
            )

    def calculate_error_rate(self, time_window_minutes: int = 5) -> float:
        """Calculate error rate over time window."""
        # Get error count and total requests
        errors = self.metrics.get_counter_value("api_errors", time_window_minutes)
        total_requests = self.metrics.get_counter_value(
            "api_requests", time_window_minutes
        )

        if total_requests == 0:
            return 0.0

        error_rate = errors / total_requests

        if error_rate > self.performance_thresholds["error_rate"]:
            self.alerts.send_alert(
                "HighErrorRate",
                f"Error rate: {error_rate:.2%} over {time_window_minutes}min",
                severity="error",
            )

        return error_rate```
______________________________________________________________________

## 📈 Scalability

### Scalability Architecture

