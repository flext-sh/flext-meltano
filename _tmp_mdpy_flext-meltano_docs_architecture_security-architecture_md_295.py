# from flext-meltano_docs/architecture/security-architecture.md:295
from __future__ import annotations


class SessionManager:
    """Secure session management with automatic expiration."""

    def __init__(self, redis_client, session_timeout: int = 3600):
        self.redis = redis_client
        self.session_timeout = session_timeout

    def create_session(self, user_id: str, metadata: Dict[str, t.JsonValue]) -> str:
        """Create new user session."""
        session_id = self._generate_secure_session_id()
        session_data = {
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_activity": datetime.utcnow().isoformat(),
            "metadata": metadata,
            "ip_address": metadata.get("ip"),
            "user_agent": metadata.get("user_agent"),
        }

        # Store in Redis with expiration
        self.redis.setex(
            f"session:{session_id}", self.session_timeout, json.dumps(session_data)
        )

        return session_id

    def validate_session(
        self, session_id: str, ip_address: str
    ) -> Optional[Dict[str, t.JsonValue]]:
        """Validate session and update activity."""
        session_key = f"session:{session_id}"
        session_data = self.redis.get(session_key)

        if not session_data:
            return None

        session = json.loads(session_data)

        # Check IP consistency (optional security feature)
        if session.get("ip_address") != ip_address:
            self.invalidate_session(session_id)
            return None

        # Update last activity
        session["last_activity"] = datetime.utcnow().isoformat()
        self.redis.setex(session_key, self.session_timeout, json.dumps(session))

        return session```
______________________________________________________________________

## 🔒 Data Protection and Encryption

### Data Encryption Strategy

