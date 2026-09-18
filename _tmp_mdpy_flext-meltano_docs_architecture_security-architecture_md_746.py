# from flext-meltano_docs/architecture/security-architecture.md:746
from __future__ import annotations


class SecurityAuditor:
    """Comprehensive security audit logging."""

    def __init__(self, log_shipper):
        self.log_shipper = log_shipper
        self.audit_levels = {
            "authentication": "INFO",
            "authorization": "INFO",
            "data_access": "WARN",
            "configuration_change": "WARN",
            "security_incident": "ERROR",
        }

    def log_security_event(
        self, event_type: str, details: Dict[str, t.JsonValue], severity: str = "INFO"
    ) -> None:
        """Log security event with structured data."""
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event_type": event_type,
            "severity": severity,
            "details": details,
            "source": "flext-meltano",
            "version": "1.0.0",
        }

        # Add user context if available
        if hasattr(self, "_current_user"):
            audit_entry["user_id"] = self._current_user.id
            audit_entry["user_role"] = self._current_user.role

        # Add request context
        if hasattr(self, "_current_request"):
            audit_entry.update({
                "request_id": self._current_request.id,
                "client_ip": self._current_request.client_ip,
                "user_agent": self._current_request.user_agent,
                "endpoint": self._current_request.endpoint,
            })

        # Ship to centralized logging
        self.log_shipper.ship_log(audit_entry)

        # Local logging for redundancy
        logger.log(severity, f"Security event: {event_type}", extra=audit_entry)```
______________________________________________________________________

## 📋 Compliance Framework

### Compliance Requirements

| Standard      | Requirements                               | Implementation Status |
| ------------- | ------------------------------------------ | --------------------- |
| **GDPR**      | Data protection, consent, right to erasure | ✅ Implemented         |
| **CCPA**      | Data portability, deletion rights          | ✅ Implemented         |
| **SOC 2**     | Security, availability, confidentiality    | 🚧 In Progress         |
| **ISO 27001** | Information security management            | ✅ Implemented         |
| **HIPAA**     | PHI protection (if applicable)             | ⚠️ Conditional        |

### Compliance Controls

#### Data Privacy Controls

