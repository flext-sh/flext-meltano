"""Test configuration for flext-oracle-oic-ext.

Provides pytest fixtures and configuration for testing Oracle OIC extension functionality
using real Oracle Integration Cloud connections and flext-core patterns.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator


# Test environment setup
@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "debug"
    os.environ["OIC_TEST_MODE"] = "true"
    yield
    # Cleanup
    os.environ.pop("FLEXT_ENV", None)
    os.environ.pop("FLEXT_LOG_LEVEL", None)
    os.environ.pop("OIC_TEST_MODE", None)


# Oracle OIC connection fixtures
@pytest.fixture
def oic_connection_config() -> dict[str, Any]:
    """Oracle OIC connection configuration for testing."""
    return {
        "host": "test-oic.oraclecloud.com",
        "username": "test_user",
        "password": "test_pass",
        "identity_domain": "test_domain",
        "timeout": 30,
        "verify_ssl": False,  # For testing only
        "api_version": "v1",
    }


@pytest.fixture
def oic_client(oic_connection_config: dict[str, Any]) -> Any:
    """Oracle OIC extension for testing."""
    from flext_oracle_oic_ext.extension import OracleOICExtension

    extension = OracleOICExtension()
    extension.config = oic_connection_config
    return extension


# OIC integration fixtures
@pytest.fixture
def integration_definition() -> dict[str, Any]:
    """Integration definition for testing."""
    return {
        "id": "TEST_INTEGRATION_001",
        "name": "Test Integration",
        "description": "Test integration for OIC extension",
        "version": "1.0.0",
        "pattern": "orchestration",
        "style": "scheduled",
        "connections": [
            {
                "id": "source_conn",
                "name": "Source Connection",
                "type": "rest",
                "role": "trigger",
            },
            {
                "id": "target_conn",
                "name": "Target Connection",
                "type": "database",
                "role": "invoke",
            },
        ],
    }


@pytest.fixture
def connection_definition() -> dict[str, Any]:
    """Connection definition for testing."""
    return {
        "id": "TEST_CONNECTION_001",
        "name": "Test Database Connection",
        "description": "Test database connection for OIC",
        "type": "oracle_database",
        "properties": {
            "host": "localhost",
            "port": 1521,
            "database": "TESTDB",
            "username": "test_user",
            "password": "test_pass",
        },
        "security_policy": "basic",
        "pool_size": 5,
    }


# OIC artifact fixtures
@pytest.fixture
def package_definition() -> dict[str, Any]:
    """Package definition for testing."""
    return {
        "id": "TEST_PACKAGE_001",
        "name": "Test Package",
        "description": "Test package for OIC deployment",
        "version": "1.0.0",
        "integrations": ["TEST_INTEGRATION_001"],
        "connections": ["TEST_CONNECTION_001"],
        "libraries": [],
        "certificates": [],
    }


@pytest.fixture
def runtime_config() -> dict[str, Any]:
    """Runtime configuration for testing."""
    return {
        "environment": "test",
        "instance_count": 1,
        "heap_size": "512M",
        "monitoring": {
            "enabled": True,
            "level": "debug",
            "tracking": ["payload", "headers"],
        },
        "error_handling": {
            "retry_count": 3,
            "retry_interval": 5,
            "fault_policy": "default",
        },
    }


# REST API fixtures
@pytest.fixture
def rest_endpoint_config() -> dict[str, Any]:
    """REST endpoint configuration for testing."""
    return {
        "base_url": "https://test-oic.oraclecloud.com",
        "endpoints": {
            "integrations": "/ic/api/integration/v1/integrations",
            "connections": "/ic/api/integration/v1/connections",
            "packages": "/ic/api/integration/v1/packages",
            "instances": "/ic/api/integration/v1/instances",
            "monitoring": "/ic/api/integration/v1/monitoring",
        },
        "auth": {
            "type": "basic",
            "username": "test_user",
            "password": "test_pass",
        },
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    }


@pytest.fixture
def sample_payload_data() -> dict[str, Any]:
    """Sample payload data for testing."""
    return {
        "request": {
            "header": {
                "message_id": "MSG_001",
                "timestamp": "2023-01-01T12:00:00Z",
                "source": "test_source",
            },
            "body": {
                "operation": "create_record",
                "data": {
                    "id": "REC_001",
                    "name": "Test Record",
                    "value": 123.45,
                    "status": "active",
                },
            },
        },
        "response": {
            "header": {
                "message_id": "MSG_001",
                "correlation_id": "CORR_001",
                "timestamp": "2023-01-01T12:00:05Z",
                "status": "success",
            },
            "body": {
                "result": "created",
                "record_id": "REC_001",
                "processing_time": 5.2,
            },
        },
    }


# Deployment fixtures
@pytest.fixture
def deployment_config() -> dict[str, Any]:
    """Deployment configuration for testing."""
    return {
        "target_environment": "test",
        "deployment_plan": {
            "pre_deployment": [
                "validate_connections",
                "check_dependencies",
            ],
            "deployment": [
                "deploy_connections",
                "deploy_integrations",
                "activate_integrations",
            ],
            "post_deployment": [
                "run_smoke_tests",
                "update_monitoring",
            ],
        },
        "rollback_plan": {
            "enabled": True,
            "automatic": False,
            "conditions": ["deployment_failure", "health_check_failure"],
        },
    }


# Monitoring fixtures
@pytest.fixture
def monitoring_config() -> dict[str, Any]:
    """Monitoring configuration for testing."""
    return {
        "metrics": {
            "enabled": True,
            "collection_interval": 60,
            "retention_days": 30,
            "thresholds": {
                "error_rate": 5.0,
                "response_time": 10.0,
                "throughput": 100,
            },
        },
        "alerts": {
            "enabled": True,
            "channels": ["email", "webhook"],
            "escalation": {
                "levels": 3,
                "interval": 15,
            },
        },
        "logging": {
            "level": "info",
            "include_payload": False,
            "include_headers": True,
            "retention_days": 14,
        },
    }


@pytest.fixture
def integration_instance_data() -> dict[str, Any]:
    """Integration instance data for testing."""
    return {
        "instance_id": "INST_001",
        "integration_id": "TEST_INTEGRATION_001",
        "version": "1.0.0",
        "status": "active",
        "created_at": "2023-01-01T10:00:00Z",
        "last_run": "2023-01-01T11:30:00Z",
        "run_count": 25,
        "success_count": 23,
        "error_count": 2,
        "avg_processing_time": 2.5,
    }


# Error handling fixtures
@pytest.fixture
def error_scenarios() -> list[dict[str, Any]]:
    """Error scenarios for testing."""
    return [
        {
            "name": "connection_timeout",
            "error_type": "ConnectionTimeoutError",
            "status_code": 408,
            "message": "Connection to OIC timed out",
            "retry_strategy": "exponential_backoff",
        },
        {
            "name": "authentication_failure",
            "error_type": "AuthenticationError",
            "status_code": 401,
            "message": "Invalid credentials",
            "retry_strategy": "none",
        },
        {
            "name": "quota_exceeded",
            "error_type": "QuotaExceededError",
            "status_code": 429,
            "message": "API quota exceeded",
            "retry_strategy": "rate_limit_backoff",
        },
        {
            "name": "integration_fault",
            "error_type": "IntegrationFaultError",
            "status_code": 500,
            "message": "Integration processing failed",
            "retry_strategy": "circuit_breaker",
        },
    ]


# Security fixtures
@pytest.fixture
def security_config() -> dict[str, Any]:
    """Security configuration for testing."""
    return {
        "authentication": {
            "type": "oauth2",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "scope": "https://test.oraclecloud.com/oic",
            "token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
        },
        "encryption": {
            "enabled": True,
            "algorithm": "AES-256",
            "key_management": "oic_managed",
        },
        "certificates": {
            "ssl_verification": True,
            "custom_ca": None,
            "client_cert": None,
        },
    }


# Performance test fixtures
@pytest.fixture
def performance_test_config() -> dict[str, Any]:
    """Performance test configuration."""
    return {
        "load_test": {
            "concurrent_users": 10,
            "duration": 300,  # 5 minutes
            "ramp_up_time": 60,
            "target_throughput": 50,  # requests per second
        },
        "stress_test": {
            "max_concurrent_users": 100,
            "step_size": 10,
            "step_duration": 60,
            "break_point_threshold": 95,  # % error rate
        },
        "thresholds": {
            "response_time_p95": 5.0,  # seconds
            "error_rate": 1.0,  # percentage
            "throughput": 45,  # requests per second
        },
    }


# Pytest markers for test categorization
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "oic: Oracle OIC tests")
    config.addinivalue_line("markers", "rest: REST API tests")
    config.addinivalue_line("markers", "deployment: Deployment tests")
    config.addinivalue_line("markers", "monitoring: Monitoring tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "slow: Slow tests")


# Mock services
@pytest.fixture
def mock_oic_service() -> Any:
    """Mock OIC service for testing."""

    class MockOICService:
        def __init__(self) -> None:
            self.integrations: dict[str, dict[str, Any]] = {}
            self.connections: dict[str, dict[str, Any]] = {}
            self.packages: dict[str, dict[str, Any]] = {}
            self.instances: dict[str, dict[str, Any]] = {}

        async def create_integration(
            self,
            integration_def: dict[str, Any],
        ) -> dict[str, Any]:
            integration_id = integration_def["id"]
            integration = {
                **integration_def,
                "created_at": "2023-01-01T12:00:00Z",
                "status": "draft",
                "version": integration_def.get("version", "1.0.0"),
            }
            self.integrations[integration_id] = integration
            return integration

        async def deploy_integration(self, integration_id: str) -> dict[str, Any]:
            if integration_id not in self.integrations:
                msg = f"Integration {integration_id} not found"
                raise ValueError(msg)

            self.integrations[integration_id]["status"] = "active"

            instance = {
                "instance_id": f"INST_{len(self.instances) + 1:03d}",
                "integration_id": integration_id,
                "status": "running",
                "deployed_at": "2023-01-01T12:05:00Z",
            }

            self.instances[instance["instance_id"]] = instance
            return instance

        async def create_connection(
            self,
            connection_def: dict[str, Any],
        ) -> dict[str, Any]:
            connection_id = connection_def["id"]
            connection = {
                **connection_def,
                "created_at": "2023-01-01T12:00:00Z",
                "status": "configured",
            }
            self.connections[connection_id] = connection
            return connection

        async def test_connection(self, connection_id: str) -> dict[str, Any]:
            if connection_id not in self.connections:
                msg = f"Connection {connection_id} not found"
                raise ValueError(msg)

            return {
                "connection_id": connection_id,
                "test_result": "success",
                "tested_at": "2023-01-01T12:00:00Z",
                "response_time": 1.5,
            }

        async def get_monitoring_data(
            self,
            integration_id: str,
            start_time: str,
            end_time: str,
        ) -> dict[str, Any]:
            return {
                "integration_id": integration_id,
                "period": {"start": start_time, "end": end_time},
                "metrics": {
                    "total_executions": 100,
                    "successful_executions": 95,
                    "failed_executions": 5,
                    "avg_response_time": 2.3,
                    "throughput": 25.5,
                },
                "errors": [
                    {
                        "error_code": "OIC-001",
                        "count": 3,
                        "message": "Connection timeout",
                    },
                    {
                        "error_code": "OIC-002",
                        "count": 2,
                        "message": "Data validation failed",
                    },
                ],
            }

    return MockOICService()


@pytest.fixture
def mock_oic_client() -> Any:
    """Mock OIC client for testing."""

    class MockOICClient:
        def __init__(self, config: dict[str, Any]) -> None:
            self.config = config
            self.connected = False
            self.session_token: str | None = None

        async def connect(self) -> bool:
            self.connected = True
            self.session_token = "mock_session_token_123"
            return True

        async def disconnect(self) -> bool:
            self.connected = False
            self.session_token = None
            return True

        async def get(
            self,
            endpoint: str,
            params: dict[str, Any] | None = None,
        ) -> dict[str, Any]:
            return {
                "status": "success",
                "endpoint": endpoint,
                "params": params,
                "response_time": 0.5,
            }

        async def post(
            self,
            endpoint: str,
            data: dict[str, Any],
            headers: dict[str, Any] | None = None,
        ) -> dict[str, Any]:
            return {
                "status": "success",
                "endpoint": endpoint,
                "data": data,
                "headers": headers,
                "response_time": 1.0,
            }

        async def put(
            self,
            endpoint: str,
            data: dict[str, Any],
            headers: dict[str, Any] | None = None,
        ) -> dict[str, Any]:
            return {
                "status": "success",
                "endpoint": endpoint,
                "data": data,
                "headers": headers,
                "response_time": 0.8,
            }

        async def delete(self, endpoint: str) -> dict[str, Any]:
            return {
                "status": "success",
                "endpoint": endpoint,
                "response_time": 0.3,
            }

    return MockOICClient
