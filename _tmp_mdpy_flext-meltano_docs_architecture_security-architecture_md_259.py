# from flext-meltano_docs/architecture/security-architecture.md:259
from __future__ import annotations


@dataclass
class AccessRequest:
    """Access request with context attributes."""

    subject: User
    action: str  # 'read', 'write', 'execute', 'delete'
    resource: str  # 'pipeline:123', 'source:github', etc.
    context: Dict[str, t.JsonValue]  # environment, time, location, etc.


class ABACPolicy:
    """Attribute-based access control policy."""

    def evaluate(self, request: AccessRequest) -> bool:
        """Evaluate access request against policy rules."""
        # Time-based restrictions
        if request.context.get("time_hour", 0) not in range(9, 18):
            return False  # Business hours only

        # Location-based restrictions
        if request.context.get("country") not in ["US", "CA", "GB"]:
            return False  # Allowed countries only

        # Resource ownership
        if request.resource.startswith("pipeline:"):
            pipeline_id = request.resource.split(":")[1]
            if not self._user_owns_pipeline(request.subject, pipeline_id):
                return False

        return True```
### Session Management

