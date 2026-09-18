# from flext-meltano/docs/architecture/quality-attributes.md:3034
from __future__ import annotations


class APIHelpSystem:
    """Contextual help and guidance system."""

    def __init__(self):
        self.help_content = self._load_help_content()

    def get_contextual_help(
        self, endpoint: str, method: str, error_code: str = None
    ) -> Dict[str, t.JsonValue]:
        """Get contextual help for API endpoint."""
        help_info = {
            "endpoint": endpoint,
            "method": method,
            "description": self._get_endpoint_description(endpoint, method),
            "parameters": self._get_parameter_help(endpoint, method),
            "examples": self._get_usage_examples(endpoint, method),
            "troubleshooting": self._get_troubleshooting_tips(endpoint, method),
        }

        if error_code:
            help_info["error_help"] = self._get_error_help(error_code)

        return help_info

    def _get_endpoint_description(self, endpoint: str, method: str) -> str:
        """Get human-readable endpoint description."""
        descriptions = {
            "GET /api/v1/pipelines": "Retrieve a list of data pipelines",
            "POST /api/v1/pipelines": "Create a new data pipeline",
            "GET /api/v1/pipelines/{id}": "Get details of a specific pipeline",
            "PUT /api/v1/pipelines/{id}": "Update an existing pipeline",
            "DELETE /api/v1/pipelines/{id}": "Delete a pipeline",
        }

        key = f"{method} {endpoint}"
        return descriptions.get(key, f"API endpoint for {endpoint}")

    def _get_parameter_help(self, endpoint: str, method: str) -> Dict[str, t.JsonValue]:
        """Get parameter documentation."""
        if "pipelines" in endpoint:
            return {
                "name": {
                    "type": "string",
                    "required": True,
                    "description": "Unique pipeline name",
                    "example": "customer-data-sync",
                },
                "tap": {
                    "type": "object",
                    "required": True,
                    "description": "Source connector configuration",
                    "properties": {
                        "name": "tap-postgres",
                        "settings": {"host": "localhost", "database": "mydb"},
                    },
                },
                "target": {
                    "type": "object",
                    "required": True,
                    "description": "Destination connector configuration",
                },
            }

        return {}

    def _get_usage_examples(
        self, endpoint: str, method: str
    ) -> List[Dict[str, t.JsonValue]]:
        """Get usage examples for the endpoint."""
        examples = []

        if endpoint == "/api/v1/pipelines" and method == "POST":
            examples.append({
                "title": "Create a PostgreSQL to Snowflake pipeline",
                "description": "Basic pipeline creation example",
                "request": {
                    "name": "postgres-to-snowflake",
                    "tap": {
                        "name": "tap-postgres",
                        "settings": {
                            "host": "postgres.example.com",
                            "database": "analytics",
                            "user": "pipeline_user",
                            "password": "secure_password",
                        },
                    },
                    "target": {
                        "name": "target-snowflake",
                        "settings": {
                            "account": "company.snowflakecomputing.com",
                            "warehouse": "ANALYTICS_WH",
                            "database": "ANALYTICS_DB",
                        },
                    },
                },
                "response": {
                    "id": "pipeline-123",
                    "name": "postgres-to-snowflake",
                    "status": "created",
                    "created_at": "2026-04-14T10:00:00Z",
                },
            })

        return examples

    def _get_troubleshooting_tips(self, endpoint: str, method: str) -> t.StringList:
        """Get troubleshooting tips for the endpoint."""
        tips = [
            "Verify your authentication credentials",
            "Check that required parameters are provided",
            "Ensure configuration values are valid",
            "Review the API documentation for correct usage",
        ]

        if "pipelines" in endpoint:
            tips.extend([
                "Verify tap and target configurations are correct",
                "Ensure database connections are accessible",
                "Check that required permissions are granted",
                "Validate JSON schema compliance",
            ])

        return tips

    def _get_error_help(self, error_code: str) -> Dict[str, t.JsonValue]:
        """Get detailed help for specific error codes."""
        error_help = {
            "VALIDATION_ERROR": {
                "description": "Request data failed validation",
                "causes": [
                    "Missing required fields",
                    "Invalid data types",
                    "Value out of acceptable range",
                ],
                "solutions": [
                    "Review API documentation for required fields",
                    "Validate data types and formats",
                    "Check field constraints and limits",
                ],
            },
            "AUTHENTICATION_FAILED": {
                "description": "Authentication credentials are invalid",
                "causes": [
                    "Expired or invalid token",
                    "Incorrect API key",
                    "Insufficient permissions",
                ],
                "solutions": [
                    "Refresh authentication tokens",
                    "Verify API key configuration",
                    "Contact REDACTED_LDAP_BIND_PASSWORDistrator for permissions",
                ],
            },
            "RESOURCE_NOT_FOUND": {
                "description": "Requested resource does not exist",
                "causes": [
                    "Incorrect resource identifier",
                    "Resource was deleted",
                    "Typographical error in URL",
                ],
                "solutions": [
                    "Verify resource identifier",
                    "Check resource list for correct ID",
                    "Review API documentation for URL format",
                ],
            },
        }

        return error_help.get(
            error_code,
            {
                "description": "Unknown error occurred",
                "causes": ["Unexpected system behavior"],
                "solutions": ["Contact support with error details"],
            },
        )```
______________________________________________________________________

## 🧪 Testability

### Testing Architecture

