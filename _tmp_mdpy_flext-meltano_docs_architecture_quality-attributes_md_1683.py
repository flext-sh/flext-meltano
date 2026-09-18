# from flext-meltano_docs/architecture/quality-attributes.md:1683
from __future__ import annotations


class AvailabilityManager:
    """Manage high availability and failover across multiple availability zones."""

    def __init__(self, orchestrator_client, availability_config: AvailabilityConfig):
        self.orchestrator = orchestrator_client
        self.settings = availability_config
        self.current_primary_zone = None
        self.health_monitor = HealthMonitor()

    def deploy_multi_az(self, service_name: str) -> MultiAZDeployment:
        """Deploy service across multiple availability zones."""
        deployment_zones = self._select_deployment_zones(service_name)
        deployment_result = MultiAZDeployment(service_name=service_name)

        for zone in deployment_zones:
            try:
                # Deploy to zone
                zone_deployment = self.orchestrator.deploy_to_zone(
                    service_name, zone, self.settings.instance_count_per_zone
                )

                deployment_result.zone_deployments[zone] = zone_deployment

                # Configure load balancer
                self._configure_load_balancer(service_name, zone, zone_deployment)

                # Set up health checks
                self.health_monitor.add_health_check(
                    service_name, zone, zone_deployment.endpoints
                )

            except Exception as e:
                deployment_result.failures[zone] = str(e)

        # Configure failover
        self._configure_failover(service_name, deployment_zones)

        # Set primary zone
        self.current_primary_zone = deployment_zones[0]

        return deployment_result

    def monitor_availability(self) -> AvailabilityStatus:
        """Monitor availability across all zones."""
        zone_statuses = {}
        overall_healthy = True

        for service_name in self.settings.monitored_services:
            service_zones = self._get_service_zones(service_name)
            service_healthy = True

            for zone in service_zones:
                zone_health = self.health_monitor.check_zone_health(service_name, zone)

                if not zone_health.healthy:
                    service_healthy = False
                    overall_healthy = False

                    # Check if failover needed
                    if zone == self.current_primary_zone:
                        self._initiate_failover(service_name, service_zones)

                zone_statuses[f"{service_name}:{zone}"] = zone_health

        return AvailabilityStatus(
            timestamp=datetime.utcnow(),
            overall_healthy=overall_healthy,
            zone_statuses=zone_statuses,
            current_primary_zone=self.current_primary_zone,
        )

    def _initiate_failover(
        self, service_name: str, available_zones: t.StringList
    ) -> None:
        """Initiate failover to healthy zone."""
        # Find healthiest available zone
        health_scores = {}
        for zone in available_zones:
            if zone != self.current_primary_zone:
                zone_health = self.health_monitor.check_zone_health(service_name, zone)
                health_scores[zone] = zone_health.score

        if health_scores:
            # Select zone with highest health score
            new_primary_zone = max(health_scores, key=health_scores.get)

            # Execute failover
            failover_result = self.orchestrator.failover_service(
                service_name, self.current_primary_zone, new_primary_zone
            )

            if failover_result.success:
                self.current_primary_zone = new_primary_zone
                self._send_failover_notification(service_name, new_primary_zone)
            else:
                self._send_failover_failure_notification(
                    service_name, failover_result.error
                )

    def _configure_failover(self, service_name: str, zones: t.StringList) -> None:
        """Configure automatic failover policies."""
        failover_policy = {
            "service": service_name,
            "zones": zones,
            "failover_strategy": "automatic",
            "health_check_interval": 30,  # seconds
            "failover_timeout": 300,  # seconds
            "rollback_on_failure": True,
            "notification_channels": ["email", "slack", "pagerduty"],
        }

        self.orchestrator.set_failover_policy(service_name, failover_policy)

    def get_availability_metrics(self) -> AvailabilityMetrics:
        """Get comprehensive availability metrics."""
        # Calculate uptime percentages
        uptime_metrics = self._calculate_uptime_percentages()

        # Calculate MTTR (Mean Time To Recovery)
        mttr_metrics = self._calculate_mttr()

        # Calculate availability SLA compliance
        sla_compliance = self._calculate_sla_compliance(uptime_metrics)

        return AvailabilityMetrics(
            timestamp=datetime.utcnow(),
            uptime_percentages=uptime_metrics,
            mttr=mttr_metrics,
            sla_compliance=sla_compliance,
            recommendations=self._generate_availability_recommendations(
                uptime_metrics, mttr_metrics
            ),
        )

    def _calculate_uptime_percentages(self) -> Dict[str, float]:
        """Calculate uptime percentages for all services."""
        uptime_data = {}

        for service_name in self.settings.monitored_services:
            service_zones = self._get_service_zones(service_name)

            # Get health check data for last 30 days
            health_data = self.health_monitor.get_health_history(service_name, days=30)

            # Calculate uptime percentage
            total_checks = len(health_data)
            healthy_checks = sum(1 for check in health_data if check.healthy)

            uptime_percentage = (
                (healthy_checks / total_checks * 100) if total_checks > 0 else 100.0
            )
            uptime_data[service_name] = uptime_percentage

        return uptime_data

    def _calculate_mttr(self) -> Dict[str, float]:
        """Calculate Mean Time To Recovery for incidents."""
        mttr_data = {}

        for service_name in self.settings.monitored_services:
            # Get incident data for last 90 days
            incidents = self._get_incident_history(service_name, days=90)

            if incidents:
                total_recovery_time = sum(
                    (incident.resolved_at - incident.started_at).total_seconds()
                    for incident in incidents
                    if incident.resolved_at
                )

                mttr_seconds = total_recovery_time / len(incidents)
                mttr_data[service_name] = mttr_seconds
            else:
                mttr_data[service_name] = 0.0  # No incidents

        return mttr_data

    def _calculate_sla_compliance(
        self, uptime_metrics: Dict[str, float]
    ) -> Dict[str, bool]:
        """Calculate SLA compliance for each service."""
        sla_compliance = {}

        for service_name, uptime_percentage in uptime_metrics.items():
            target_sla = self.settings.service_slas.get(service_name, 99.9)
            sla_compliance[service_name] = uptime_percentage >= target_sla

        return sla_compliance

    def _generate_availability_recommendations(
        self, uptime_metrics: Dict[str, float], mttr_metrics: Dict[str, float]
    ) -> t.StringList:
        """Generate availability improvement recommendations."""
        recommendations = []

        # SLA compliance recommendations
        non_compliant_services = [
            service
            for service, compliant in self._calculate_sla_compliance(
                uptime_metrics
            ).items()
            if not compliant
        ]

        if non_compliant_services:
            recommendations.append(
                f"Improve uptime for SLA non-compliant services: {', '.join(non_compliant_services)}"
            )

        # MTTR recommendations
        high_mttr_services = [
            service
            for service, mttr in mttr_metrics.items()
            if mttr > self.settings.target_mttr_seconds
        ]

        if high_mttr_services:
            recommendations.append(
                f"Reduce recovery time for services with high MTTR: {', '.join(high_mttr_services)}"
            )

        # General recommendations
        if not recommendations:
            recommendations.append(
                "Availability metrics are within acceptable parameters"
            )
            recommendations.append(
                "Continue monitoring and maintaining high availability practices"
            )

        return recommendations```
#### 2. Disaster Recovery Implementation

