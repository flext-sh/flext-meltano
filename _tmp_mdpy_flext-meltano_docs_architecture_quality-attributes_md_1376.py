# from flext-meltano_docs/architecture/quality-attributes.md:1376
from __future__ import annotations


class ReliabilityMonitor:
    """Monitor system reliability and trigger alerts."""

    def __init__(self, metrics_collector, alert_manager):
        self.metrics = metrics_collector
        self.alerts = alert_manager
        self.reliability_thresholds = {
            "error_rate_threshold": 0.05,  # 5%
            "circuit_breaker_threshold": 0.8,  # 80% of services
            "mean_time_between_failures": 7200,  # 2 hours
        }

    def monitor_error_rates(self) -> None:
        """Monitor error rates across the system."""
        # Get error rates by service
        service_error_rates = self.metrics.get_error_rates_by_service()

        high_error_services = []
        for service, error_rate in service_error_rates.items():
            if error_rate > self.reliability_thresholds["error_rate_threshold"]:
                high_error_services.append((service, error_rate))

        if high_error_services:
            # Sort by error rate descending
            high_error_services.sort(key=lambda x: x[1], reverse=True)

            message = "High error rates detected:\\n"
            for service, error_rate in high_error_services:
                message += f"- {service}: {error_rate:.2%}\\n"

            self.alerts.send_alert(
                "HighErrorRates",
                message,
                severity="error",
                affected_services=[s[0] for s in high_error_services],
            )

    def monitor_circuit_breakers(self) -> None:
        """Monitor circuit breaker states."""
        circuit_breaker_states = self.metrics.get_circuit_breaker_states()

        open_breakers = [
            service
            for service, state in circuit_breaker_states.items()
            if state == "open"
        ]

        if (
            len(open_breakers)
            > len(circuit_breaker_states)
            * self.reliability_thresholds["circuit_breaker_threshold"]
        ):
            self.alerts.send_alert(
                "MultipleCircuitBreakersOpen",
                f"Multiple circuit breakers open: {', '.join(open_breakers)}",
                severity="critical",
                affected_services=open_breakers,
            )

    def calculate_mtbf(self) -> float:
        """Calculate Mean Time Between Failures."""
        # Get failure events from the last 24 hours
        failure_events = self.metrics.get_failure_events(hours=24)

        if len(failure_events) < 2:
            return float("inf")  # Not enough data

        # Calculate time between failures
        failure_times = [event.timestamp for event in failure_events]
        time_differences = []

        for i in range(1, len(failure_times)):
            time_diff = (failure_times[i] - failure_times[i - 1]).total_seconds()
            time_differences.append(time_diff)

        if not time_differences:
            return float("inf")

        mtbf = sum(time_differences) / len(time_differences)

        # Alert if MTBF is below threshold
        if mtbf < self.reliability_thresholds["mean_time_between_failures"]:
            self.alerts.send_alert(
                "LowMTBF",
                f"Mean Time Between Failures: {mtbf:.0f} seconds "
                f"(threshold: {self.reliability_thresholds['mean_time_between_failures']} seconds)",
                severity="warning",
            )

        return mtbf

    def generate_reliability_report(self) -> ReliabilityReport:
        """Generate comprehensive reliability report."""
        error_rates = self.metrics.get_error_rates_by_service()
        circuit_breaker_states = self.metrics.get_circuit_breaker_states()
        mtbf = self.calculate_mtbf()
        uptime_percentages = self.metrics.get_uptime_percentages(hours=24)

        # Calculate overall reliability score
        reliability_score = self._calculate_reliability_score(
            error_rates, circuit_breaker_states, uptime_percentages
        )

        return ReliabilityReport(
            timestamp=datetime.utcnow(),
            reliability_score=reliability_score,
            error_rates=error_rates,
            circuit_breaker_states=circuit_breaker_states,
            mean_time_between_failures=mtbf,
            uptime_percentages=uptime_percentages,
            recommendations=self._generate_reliability_recommendations(
                error_rates, circuit_breaker_states, mtbf
            ),
        )

    def _calculate_reliability_score(
        self,
        error_rates: Dict[str, float],
        circuit_breaker_states: Dict[str, str],
        uptime_percentages: Dict[str, float],
    ) -> float:
        """Calculate overall reliability score (0-100)."""
        scores = []

        # Error rate score (40% weight)
        avg_error_rate = (
            sum(error_rates.values()) / len(error_rates) if error_rates else 0
        )
        error_score = max(0, 100 - (avg_error_rate * 2000))  # Penalty for errors
        scores.append(("error_rate", error_score, 40))

        # Circuit breaker score (30% weight)
        open_breakers = sum(
            1 for state in circuit_breaker_states.values() if state == "open"
        )
        breaker_score = max(
            0, 100 - (open_breakers / len(circuit_breaker_states) * 100)
        )
        scores.append(("circuit_breakers", breaker_score, 30))

        # Uptime score (30% weight)
        avg_uptime = (
            sum(uptime_percentages.values()) / len(uptime_percentages)
            if uptime_percentages
            else 100
        )
        uptime_score = avg_uptime
        scores.append(("uptime", uptime_score, 30))

        # Calculate weighted average
        total_score = sum(score * weight for _, score, weight in scores)
        total_weight = sum(weight for _, _, weight in scores)

        return round(total_score / total_weight, 1)

    def _generate_reliability_recommendations(
        self,
        error_rates: Dict[str, float],
        circuit_breaker_states: Dict[str, str],
        mtbf: float,
    ) -> t.StringList:
        """Generate reliability improvement recommendations."""
        recommendations = []

        # High error rate recommendations
        high_error_services = [
            service
            for service, rate in error_rates.items()
            if rate > self.reliability_thresholds["error_rate_threshold"]
        ]
        if high_error_services:
            recommendations.append(
                f"Investigate high error rates in services: {', '.join(high_error_services)}"
            )

        # Circuit breaker recommendations
        open_breakers = [
            service
            for service, state in circuit_breaker_states.items()
            if state == "open"
        ]
        if open_breakers:
            recommendations.append(
                f"Address open circuit breakers for services: {', '.join(open_breakers)}"
            )

        # MTBF recommendations
        if mtbf < self.reliability_thresholds["mean_time_between_failures"]:
            recommendations.append(
                f"Improve system stability - current MTBF: {mtbf:.0f} seconds"
            )

        # General recommendations
        if not recommendations:
            recommendations.append("System reliability is within acceptable parameters")
            recommendations.append(
                "Continue monitoring and maintaining current reliability practices"
            )

        return recommendations```
______________________________________________________________________

## ⏱️ Availability

### Availability Architecture

