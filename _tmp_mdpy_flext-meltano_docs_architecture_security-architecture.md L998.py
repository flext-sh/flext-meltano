# from flext-meltano/docs/architecture/security-architecture.md:998
from __future__ import annotations


class IncidentDetector:
    """Automated incident detection and initial analysis."""

    def detect_security_incident(self, event: SecurityEvent) -> IncidentResponse:
        """Analyze security event and determine response."""
        # Assess severity
        severity = self._assess_severity(event)

        # Determine incident type
        incident_type = self._classify_incident(event)

        # Calculate business impact
        impact = self._calculate_business_impact(event)

        # Determine response actions
        response_actions = self._determine_response_actions(
            severity, incident_type, impact
        )

        return IncidentResponse(
            incident_id=str(uuid.uuid4()),
            severity=severity,
            incident_type=incident_type,
            impact=impact,
            response_actions=response_actions,
            detection_time=datetime.utcnow(),
            assigned_team=self._get_responsible_team(incident_type),
        )```
#### 2. Containment and Eradication

