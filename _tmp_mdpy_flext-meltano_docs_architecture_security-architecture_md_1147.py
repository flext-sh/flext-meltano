# from flext-meltano_docs/architecture/security-architecture.md:1147
from __future__ import annotations


class SecurityDashboard:
    """Real-time security health monitoring."""

    def generate_security_report(self) -> SecurityHealthReport:
        """Generate comprehensive security health report."""
        # Authentication metrics
        auth_metrics = self._get_authentication_metrics()

        # Authorization metrics
        authz_metrics = self._get_authorization_metrics()

        # Data protection metrics
        data_metrics = self._get_data_protection_metrics()

        # Infrastructure metrics
        infra_metrics = self._get_infrastructure_metrics()

        # Threat detection metrics
        threat_metrics = self._get_threat_detection_metrics()

        # Calculate overall health score
        health_score = self._calculate_health_score([
            auth_metrics,
            authz_metrics,
            data_metrics,
            infra_metrics,
            threat_metrics,
        ])

        return SecurityHealthReport(
            timestamp=datetime.utcnow(),
            health_score=health_score,
            authentication=auth_metrics,
            authorization=authz_metrics,
            data_protection=data_metrics,
            infrastructure=infra_metrics,
            threat_detection=threat_metrics,
            recommendations=self._generate_recommendations(health_score),
        )```
______________________________________________________________________

**Security Architecture**: FLEXT-Meltano Enterprise Security Framework
_Comprehensive security architecture with defense-in-depth, compliance, and incident response_
