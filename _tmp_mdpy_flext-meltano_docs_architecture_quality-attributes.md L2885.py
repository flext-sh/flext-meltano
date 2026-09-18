# from flext-meltano/docs/architecture/quality-attributes.md:2885
from __future__ import annotations


class APIResponse:
    """Consistent API response format."""

    def __init__(
        self, data=None, error: str = None, metadata: Dict[str, t.JsonValue] = None
    ):
        self.success = error is None
        self.data = data
        self.error = error
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()
        self.request_id = self._generate_request_id()

    def to_dict(self) -> Dict[str, t.JsonValue]:
        """Convert response to dictionary format."""
        response = {
            "success": self.success,
            "timestamp": self.timestamp,
            "request_id": self.request_id,
        }

        if self.success:
            response["data"] = self.data
        else:
            response["error"] = {
                "message": self.error,
                "code": self._get_error_code(self.error),
                "suggestions": self._get_error_suggestions(self.error),
            }

        if self.metadata:
            response["metadata"] = self.metadata

        return response

    def _generate_request_id(self) -> str:
        """Generate unique request identifier."""
        return str(uuid.uuid4())

    def _get_error_code(self, error: str) -> str:
        """Map error message to error code."""
        error_codes = {
            "not_found": ["not found", "does not exist"],
            "unauthorized": ["unauthorized", "not authorized"],
            "validation_error": ["invalid", "validation failed"],
            "server_error": ["internal", "unexpected error"],
        }

        for code, patterns in error_codes.items():
            if any(pattern in error.lower() for pattern in patterns):
                return code

        return "unknown_error"

    def _get_error_suggestions(self, error: str) -> t.StringList:
        """Provide actionable suggestions for error resolution."""
        suggestions_map = {
            "not_found": [
                "Check the resource identifier",
                "Verify the resource exists",
                "Check your permissions",
            ],
            "unauthorized": [
                "Verify your authentication credentials",
                "Check your permissions for this resource",
                "Contact your REDACTED_LDAP_BIND_PASSWORDistrator",
            ],
            "validation_error": [
                "Review the API documentation",
                "Check parameter formats",
                "Validate required fields",
            ],
        }

        error_code = self._get_error_code(error)
        return suggestions_map.get(error_code, ["Review the API documentation"])```
#### 2. Progressive Disclosure

