# from flext-meltano_docs/architecture/quality-attributes.md:653
from __future__ import annotations


class HorizontalScaler:
    """Horizontal scaling management for API and worker services."""

    def __init__(self, orchestrator_client, scaling_config: ScalingConfig):
        self.orchestrator = orchestrator_client
        self.settings = scaling_config
        self.current_instances = {}
        self.scaling_history = []

    def evaluate_scaling_needs(self, metrics: SystemMetrics) -> List[ScalingAction]:
        """Evaluate current metrics and determine scaling actions."""
        actions = []

        # Check each service
        for service_name, service_config in self.settings.services.items():
            current_count = self.current_instances.get(
                service_name, service_config.min_instances
            )
            service_metrics = metrics.get_service_metrics(service_name)

            # CPU-based scaling
            if service_metrics.cpu_percent > service_config.scale_up_cpu_threshold:
                new_count = min(
                    current_count * 2,  # Double current count
                    service_config.max_instances,
                )
                if new_count > current_count:
                    actions.append(
                        ScalingAction(
                            service_name=service_name,
                            action="scale_up",
                            current_instances=current_count,
                            target_instances=new_count,
                            reason=f"High CPU: {service_metrics.cpu_percent:.1f}%",
                        )
                    )

            elif service_metrics.cpu_percent < service_config.scale_down_cpu_threshold:
                new_count = max(
                    current_count // 2,  # Halve current count
                    service_config.min_instances,
                )
                if new_count < current_count:
                    actions.append(
                        ScalingAction(
                            service_name=service_name,
                            action="scale_down",
                            current_instances=current_count,
                            target_instances=new_count,
                            reason=f"Low CPU: {service_metrics.cpu_percent:.1f}%",
                        )
                    )

            # Queue-based scaling for workers
            if service_name in self.settings.worker_services:
                queue_depth = service_metrics.queue_depth
                if queue_depth > service_config.queue_threshold:
                    new_count = min(
                        current_count + 2,  # Add 2 workers
                        service_config.max_instances,
                    )
                    if new_count > current_count:
                        actions.append(
                            ScalingAction(
                                service_name=service_name,
                                action="scale_up",
                                current_instances=current_count,
                                target_instances=new_count,
                                reason=f"Queue depth: {queue_depth}",
                            )
                        )

        return actions

    def execute_scaling_actions(
        self, actions: List[ScalingAction]
    ) -> List[ScalingResult]:
        """Execute scaling actions and track results."""
        results = []

        for action in actions:
            try:
                if action.action == "scale_up":
                    self.orchestrator.scale_up_service(
                        action.service_name, action.target_instances
                    )
                elif action.action == "scale_down":
                    self.orchestrator.scale_down_service(
                        action.service_name, action.target_instances
                    )

                # Update current instance count
                self.current_instances[action.service_name] = action.target_instances

                # Record scaling event
                self.scaling_history.append({
                    "timestamp": datetime.utcnow(),
                    "service": action.service_name,
                    "action": action.action,
                    "from_instances": action.current_instances,
                    "to_instances": action.target_instances,
                    "reason": action.reason,
                })

                results.append(
                    ScalingResult(
                        action=action,
                        success=True,
                        message=f"Successfully scaled {action.service_name}",
                    )
                )

            except Exception as e:
                results.append(
                    ScalingResult(
                        action=action,
                        success=False,
                        message=f"Scaling failed: {e!s}",
                    )
                )

        return results

    def get_scaling_recommendations(
        self, metrics: SystemMetrics
    ) -> List[ScalingRecommendation]:
        """Provide scaling recommendations without executing them."""
        recommendations = []

        for service_name, service_config in self.settings.services.items():
            service_metrics = metrics.get_service_metrics(service_name)

            # Cost optimization recommendations
            if service_metrics.utilization < 30 and service_metrics.cost_per_hour > 0:
                savings_per_month = service_metrics.cost_per_hour * 24 * 30 * 0.5
                recommendations.append(
                    ScalingRecommendation(
                        service_name=service_name,
                        recommendation="reduce_instances",
                        reason=f"Low utilization: {service_metrics.utilization:.1f}%",
                        potential_savings=savings_per_month,
                        confidence="high",
                    )
                )

            # Performance optimization recommendations
            if service_metrics.latency_p95 > service_config.target_latency:
                recommendations.append(
                    ScalingRecommendation(
                        service_name=service_name,
                        recommendation="increase_instances",
                        reason=f"High latency: {service_metrics.latency_p95:.0f}ms",
                        performance_impact=f"Reduce latency by ~{service_metrics.latency_p95 * 0.3:.0f}ms",
                        confidence="medium",
                    )
                )

        return recommendations```
#### 2. Data Scaling

