"""FlextMeltano FlexCore Go Runtime Integration.

Integration with FlexCore Go runtime service following Clean Architecture patterns.
"""

from __future__ import annotations

from typing import Any

from flext_core import FlextResult
from pydantic import BaseModel, Field

from flext_meltano.constants import FlextMeltanoConstants


class FlextMeltanoRuntime(BaseModel):
    """FlexCore Go runtime integration.

    Manages communication and integration with FlexCore Go runtime service
    following Clean Architecture patterns.
    """

    # Runtime connection settings
    host: str = Field(
        default=FlextMeltanoConstants.FLEXCORE_DEFAULT_HOST,
        description="FlexCore runtime host",
    )
    port: int = Field(
        default=FlextMeltanoConstants.FLEXCORE_DEFAULT_PORT,
        description="FlexCore runtime HTTP port",
        gt=0,
        le=65535,
    )
    grpc_port: int = Field(
        default=FlextMeltanoConstants.FLEXCORE_DEFAULT_GRPC_PORT,
        description="FlexCore runtime gRPC port",
        gt=0,
        le=65535,
    )

    # Runtime configuration
    timeout: int = Field(
        default=30,
        description="Connection timeout in seconds",
        gt=0,
    )
    enabled: bool = Field(
        default=True,
        description="Whether runtime integration is enabled",
    )

    # Runtime status
    is_connected: bool = Field(
        default=False,
        description="Whether connected to runtime",
    )
    runtime_version: str | None = Field(
        default=None,
        description="Runtime version if connected",
    )

    class Config:
        """Pydantic model configuration."""

        frozen = False
        validate_assignment = True
        extra = "forbid"

    def connect(self) -> FlextResult[dict[str, Any]]:
        """Connect to FlexCore Go runtime.

        Returns:
            FlextResult with connection information

        """
        try:
            if not self.enabled:
                return FlextResult.fail("Runtime integration is disabled")

            # Test HTTP connection
            http_result = self._test_http_connection()
            if not http_result.is_success:
                return FlextResult.fail(f"HTTP connection failed: {http_result.error}")

            # Test gRPC connection
            grpc_result = self._test_grpc_connection()
            if not grpc_result.is_success:
                return FlextResult.fail(f"gRPC connection failed: {grpc_result.error}")

            self.is_connected = True
            connection_info = {
                "http_status": http_result.data,
                "grpc_status": grpc_result.data,
                "runtime_host": self.host,
                "runtime_ports": {
                    "http": self.port,
                    "grpc": self.grpc_port,
                },
            }

            return FlextResult.ok(connection_info)

        except Exception as e:
            return FlextResult.fail(f"Runtime connection failed: {e}")

    def disconnect(self) -> FlextResult[None]:
        """Disconnect from FlexCore Go runtime.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            self.is_connected = False
            self.runtime_version = None
            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Runtime disconnection failed: {e}")

    def health_check(self) -> FlextResult[dict[str, Any]]:
        """Perform runtime health check.

        Returns:
            FlextResult with health status

        """
        try:
            if not self.is_connected:
                return FlextResult.fail("Not connected to runtime")

            # Check HTTP health endpoint
            health_result = self._check_health_endpoint()
            if not health_result.is_success:
                return health_result

            health_data = health_result.data or {}
            health_data["connection_status"] = "healthy"
            health_data["runtime_host"] = self.host
            health_data["runtime_ports"] = {
                "http": self.port,
                "grpc": self.grpc_port,
            }

            return FlextResult.ok(health_data)

        except Exception as e:
            return FlextResult.fail(f"Health check failed: {e}")

    def execute_pipeline(
        self,
        pipeline_config: dict[str, Any],
    ) -> FlextResult[dict[str, Any]]:
        """Execute pipeline via FlexCore Go runtime.

        Args:
            pipeline_config: Pipeline configuration

        Returns:
            FlextResult with execution results

        """
        try:
            if not self.is_connected:
                return FlextResult.fail("Not connected to runtime")

            # Validate pipeline configuration
            validation_result = self._validate_pipeline_config(pipeline_config)
            if not validation_result.is_success:
                return FlextResult.fail(
                    validation_result.error or "Pipeline validation failed",
                )

            # Execute pipeline via gRPC
            execution_result = self._execute_pipeline_grpc(pipeline_config)
            if not execution_result.is_success:
                return execution_result

            return FlextResult.ok(execution_result.data or {})

        except Exception as e:
            return FlextResult.fail(f"Pipeline execution failed: {e}")

    def get_pipeline_status(
        self,
        pipeline_id: str,
    ) -> FlextResult[dict[str, Any]]:
        """Get pipeline execution status.

        Args:
            pipeline_id: Pipeline identifier

        Returns:
            FlextResult with pipeline status

        """
        try:
            if not self.is_connected:
                return FlextResult.fail("Not connected to runtime")

            # Get status via HTTP API
            return self._get_pipeline_status_http(pipeline_id)

        except Exception as e:
            return FlextResult.fail(f"Failed to get pipeline status: {e}")

    def list_active_pipelines(self) -> FlextResult[list[dict[str, Any]]]:
        """List active pipelines in runtime.

        Returns:
            FlextResult with list of active pipelines

        """
        try:
            if not self.is_connected:
                return FlextResult.fail("Not connected to runtime")

            # List pipelines via HTTP API
            return self._list_pipelines_http()

        except Exception as e:
            return FlextResult.fail(f"Failed to list pipelines: {e}")

    def get_runtime_metrics(self) -> FlextResult[dict[str, Any]]:
        """Get runtime performance metrics.

        Returns:
            FlextResult with metrics data

        """
        try:
            if not self.is_connected:
                return FlextResult.fail("Not connected to runtime")

            # Get metrics via HTTP endpoint
            return self._get_metrics_http()

        except Exception as e:
            return FlextResult.fail(f"Failed to get runtime metrics: {e}")

    def _test_http_connection(self) -> FlextResult[dict[str, Any]]:
        """Test HTTP connection to runtime.

        Returns:
            FlextResult with connection test results

        """
        try:
            import requests

            url = f"http://{self.host}:{self.port}{FlextMeltanoConstants.FLEXCORE_HEALTH_ENDPOINT}"

            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            connection_data = {
                "http_connected": True,
                "status_code": response.status_code,
                "response_time": response.elapsed.total_seconds(),
                "health_endpoint": url,
            }

            return FlextResult.ok(connection_data)

        except requests.exceptions.RequestException as e:
            return FlextResult.fail(f"HTTP connection test failed: {e}")
        except Exception as e:
            return FlextResult.fail(f"HTTP connection error: {e}")

    def _test_grpc_connection(self) -> FlextResult[dict[str, Any]]:
        """Test gRPC connection to runtime.

        Returns:
            FlextResult with connection test results

        """
        try:
            # Mock gRPC connection test - in real implementation would use grpcio
            # For now, just validate that the port is accessible
            import socket

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((self.host, self.grpc_port))

                if result == 0:
                    connection_data = {
                        "grpc_connected": True,
                        "grpc_host": self.host,
                        "grpc_port": self.grpc_port,
                    }
                    return FlextResult.ok(connection_data)
                return FlextResult.fail(f"gRPC port {self.grpc_port} not accessible")

        except Exception as e:
            return FlextResult.fail(f"gRPC connection test failed: {e}")

    def _check_health_endpoint(self) -> FlextResult[dict[str, Any]]:
        """Check runtime health endpoint.

        Returns:
            FlextResult with health data

        """
        try:
            import requests

            url = f"http://{self.host}:{self.port}{FlextMeltanoConstants.FLEXCORE_HEALTH_ENDPOINT}"

            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            health_data = {
                "status": "healthy",
                "timestamp": response.headers.get("Date"),
                "version": response.headers.get("X-Runtime-Version"),
                "uptime": response.json().get("uptime") if response.content else None,
            }

            if health_data["version"]:
                self.runtime_version = health_data["version"]

            return FlextResult.ok(health_data)

        except requests.exceptions.RequestException as e:
            return FlextResult.fail(f"Health check failed: {e}")
        except Exception as e:
            return FlextResult.fail(f"Health endpoint error: {e}")

    def _validate_pipeline_config(
        self,
        config: dict[str, Any],
    ) -> FlextResult[None]:
        """Validate pipeline configuration.

        Args:
            config: Pipeline configuration to validate

        Returns:
            FlextResult indicating validation success or failure

        """
        try:
            required_fields = ["name", "steps"]

            for field in required_fields:
                if field not in config:
                    return FlextResult.fail(
                        f"Missing required field in pipeline config: {field}",
                    )

            if not isinstance(config["steps"], list):
                return FlextResult.fail("Pipeline steps must be a list")

            if len(config["steps"]) == 0:
                return FlextResult.fail("Pipeline must have at least one step")

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Pipeline config validation failed: {e}")

    def _execute_pipeline_grpc(
        self,
        config: dict[str, Any],
    ) -> FlextResult[dict[str, Any]]:
        """Execute pipeline via gRPC.

        Args:
            config: Pipeline configuration

        Returns:
            FlextResult with execution results

        """
        try:
            # Mock gRPC execution - in real implementation would use grpcio
            execution_data = {
                "pipeline_id": f"pipeline_{config['name']}_{hash(str(config))}",
                "status": "submitted",
                "submitted_at": "2025-01-01T00:00:00Z",
                "config": config,
            }

            return FlextResult.ok(execution_data)

        except Exception as e:
            return FlextResult.fail(f"gRPC pipeline execution failed: {e}")

    def _get_pipeline_status_http(
        self,
        pipeline_id: str,
    ) -> FlextResult[dict[str, Any]]:
        """Get pipeline status via HTTP.

        Args:
            pipeline_id: Pipeline identifier

        Returns:
            FlextResult with pipeline status

        """
        try:
            import requests

            url = (
                f"http://{self.host}:{self.port}/api/v1/pipelines/{pipeline_id}/status"
            )

            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            status_data = (
                response.json()
                if response.content
                else {
                    "pipeline_id": pipeline_id,
                    "status": "unknown",
                    "message": "Status endpoint returned empty response",
                }
            )

            return FlextResult.ok(status_data)

        except requests.exceptions.RequestException as e:
            return FlextResult.fail(f"Pipeline status request failed: {e}")
        except Exception as e:
            return FlextResult.fail(f"Pipeline status error: {e}")

    def _list_pipelines_http(self) -> FlextResult[list[dict[str, Any]]]:
        """List pipelines via HTTP.

        Returns:
            FlextResult with list of pipelines

        """
        try:
            import requests

            url = f"http://{self.host}:{self.port}/api/v1/pipelines"

            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            pipelines_data = response.json() if response.content else []

            return FlextResult.ok(pipelines_data)

        except requests.exceptions.RequestException as e:
            return FlextResult.fail(f"Pipeline list request failed: {e}")
        except Exception as e:
            return FlextResult.fail(f"Pipeline list error: {e}")

    def _get_metrics_http(self) -> FlextResult[dict[str, Any]]:
        """Get runtime metrics via HTTP.

        Returns:
            FlextResult with metrics data

        """
        try:
            import requests

            url = f"http://{self.host}:{self.port}{FlextMeltanoConstants.FLEXCORE_METRICS_ENDPOINT}"

            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            metrics_data = (
                response.json()
                if response.content
                else {"message": "Metrics endpoint returned empty response"}
            )

            return FlextResult.ok(metrics_data)

        except requests.exceptions.RequestException as e:
            return FlextResult.fail(f"Metrics request failed: {e}")
        except Exception as e:
            return FlextResult.fail(f"Metrics error: {e}")

    def to_dict(self) -> dict[str, Any]:
        """Convert runtime to dictionary representation.

        Returns:
            Dictionary representation of the runtime

        """
        return {
            "host": self.host,
            "port": self.port,
            "grpc_port": self.grpc_port,
            "timeout": self.timeout,
            "enabled": self.enabled,
            "is_connected": self.is_connected,
            "runtime_version": self.runtime_version,
        }
