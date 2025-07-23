"""FlextMeltano Platform - Unified Data Integration Platform.

Centralizes all Meltano ecosystem functionality:
- Meltano orchestration
- Singer SDK taps/targets
- dbt transformations
- EDK extensions
- FlexCore Go runtime
"""

from __future__ import annotations

from typing import Any

from flext_core import FlextResult
from flext_core.constants import FlextConstants
from flext_core.container import FlextContainer

from flext_meltano.config.settings import FlextMeltanoSettings


class FlextMeltanoPlatform:
    """Unified FLEXT Meltano platform integrating entire ecosystem."""

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize unified Meltano platform.

        Args:
            config: Platform configuration dictionary

        """
        self._config = FlextMeltanoSettings(**config)
        self._container = FlextContainer()
        self._setup_services()

    def _setup_services(self) -> None:
        """Setup all platform services in container."""
        # Register core services
        self._container.register(
            "platform_config",
            self._config,
        )

        # Register Meltano services
        from flext_meltano.environment.manager import (
            FlextMeltanoEnvironmentManager,
        )
        from flext_meltano.jobs.manager import FlextMeltanoJobManager
        from flext_meltano.plugins.manager import (
            FlextMeltanoPluginManager,
        )
        from flext_meltano.project.manager import (
            FlextMeltanoProjectManager,
        )
        from flext_meltano.state.manager import FlextMeltanoStateManager

        self._container.register(
            "project_manager",
            FlextMeltanoProjectManager(self._config),
        )
        self._container.register(
            "environment_manager",
            FlextMeltanoEnvironmentManager(self._config),
        )
        self._container.register(
            "job_manager",
            FlextMeltanoJobManager(self._config),
        )
        self._container.register(
            "plugin_manager",
            FlextMeltanoPluginManager(self._config),
        )
        self._container.register(
            "state_manager",
            FlextMeltanoStateManager(self._config),
        )

        # Register Singer SDK services
        from flext_meltano.singer.manager import FlextMeltanoSingerManager

        self._container.register(
            "singer_manager",
            FlextMeltanoSingerManager(self._config),
        )

        # Register dbt services
        from flext_meltano.dbt.manager import FlextMeltanoDbtManager

        self._container.register(
            "dbt_manager",
            FlextMeltanoDbtManager(self._config),
        )

        # Register EDK services
        from flext_meltano.edk.manager import (
            FlextMeltanoExtensionManager,
        )

        self._container.register(
            "extension_manager",
            FlextMeltanoExtensionManager(self._config),
        )

    @property
    def config(self) -> FlextMeltanoSettings:
        """Get platform configuration."""
        return self._config

    @property
    def container(self) -> FlextContainer:
        """Get service container."""
        return self._container

    def get_service(self, service_name: str) -> FlextResult[Any]:
        """Get service from container.

        Args:
            service_name: Name of service to retrieve

        Returns:
            FlextResult containing service instance or error

        """
        return self._container.get(service_name)

    async def initialize(self) -> FlextResult[None]:
        """Initialize platform and all services.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Initialize all managers
            managers = [
                "project_manager",
                "environment_manager",
                "job_manager",
                "plugin_manager",
                "state_manager",
                "singer_manager",
                "dbt_manager",
                "extension_manager",
            ]

            for manager_name in managers:
                manager_result = self.get_service(manager_name)
                if manager_result.is_failure:
                    return FlextResult.fail(
                        f"Failed to get {manager_name}: "
                        f"{manager_result.error}",
                    )

                manager = manager_result.data
                if hasattr(manager, "initialize"):
                    init_result = await manager.initialize()
                    if init_result.is_failure:
                        return FlextResult.fail(
                            f"Failed to initialize {manager_name}: "
                            f"{init_result.error}",
                        )

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Platform initialization failed: {e}")

    async def shutdown(self) -> FlextResult[None]:
        """Shutdown platform and cleanup resources.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Shutdown all managers in reverse order
            managers = [
                "extension_manager",
                "dbt_manager",
                "singer_manager",
                "state_manager",
                "plugin_manager",
                "job_manager",
                "environment_manager",
                "project_manager",
            ]

            for manager_name in managers:
                manager_result = self.get_service(manager_name)
                if manager_result.is_success:
                    manager = manager_result.data
                    if hasattr(manager, "shutdown"):
                        await manager.shutdown()

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Platform shutdown failed: {e}")

    def health_check(self) -> FlextResult[dict[str, Any]]:
        """Perform platform health check.

        Returns:
            FlextResult with health status information

        """
        try:
            health_status = {
                "platform": "healthy",
                "version": "0.7.0",
                "services": {},
            }

            # Check all services
            service_names = [
                "project_manager",
                "environment_manager",
                "job_manager",
                "plugin_manager",
                "state_manager",
                "singer_manager",
                "dbt_manager",
                "extension_manager",
            ]

            for service_name in service_names:
                service_result = self.get_service(service_name)
                if service_result.is_success:
                    service = service_result.data
                    if hasattr(service, "health_check"):
                        service_health = service.health_check()
                        health_status["services"][service_name] = (
                            service_health.data
                            if service_health.is_success
                            else {"status": "unhealthy"}
                        )
                    else:
                        health_status["services"][service_name] = {
                            "status": "healthy"
                        }
                else:
                    health_status["services"][service_name] = {
                        "status": "unavailable"
                    }

            return FlextResult.ok(health_status)

        except Exception as e:
            return FlextResult.fail(f"Health check failed: {e}")
