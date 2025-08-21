"""FLEXT Meltano Plugin Implementation - Clean Architecture Plugin Implementation.

This module implements the clean plugin architecture for FLEXT Meltano, providing
proper separation between abstract interfaces and concrete implementations.
Follows the principles established in flext-core interfaces and flext-plugin domain entities.

Key Components:
    - FlextMeltanoDataPlugin: Main implementation of FlextDataPlugin interface
    - FlextMeltanoPluginContext: Context provider for plugin runtime
    - FlextMeltanoPluginRegistry: Registry implementation for plugin management

Architecture:
    - Uses composition with flext-plugin domain entities
    - Implements flext-core interfaces without mixing concrete logic
    - Maintains backward compatibility with existing flext-meltano APIs
    - Provides clean separation between abstractions and implementations

Example:
    >>> from flext_meltano.plugin_implementation import FlextMeltanoTapPlugin
    >>>
    >>> # Create tap plugin directly using flext-core patterns
    >>> plugin = FlextMeltanoTapPlugin(
    ...     name="tap-csv",
    ...     version="1.0.0",
    ...     config={"description": "CSV tap for Meltano"},
    ... )
    >>>
    >>> # Use plugin functionality
    >>> result = plugin.validate_config({"path": "/data/file.csv"})

"""

from __future__ import annotations

from collections.abc import Mapping

from flext_core import FlextPlugin, FlextPluginContext, FlextResult, get_logger
from structlog.stdlib import BoundLogger

from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.execution import create_executor

# =============================================================================
# MELTANO PLUGIN IMPLEMENTATIONS - FLEXT-CORE INTERFACE COMPLIANCE
# =============================================================================


class FlextMeltanoPlugin(FlextPlugin):
    """Concrete Meltano plugin implementation using flext-core FlextPlugin interface.

    COMPLIANCE: Pure implementation of FlextPlugin from flext-core, no mixing with flext-plugin.
    NO MIXING: Uses only flext-core interfaces without domain entity dependencies.
    """

    def __init__(self, name: str, version: str, plugin_type: str = "generic") -> None:
        """Initialize Meltano plugin with basic information."""
        self._name = name
        self._version = version
        self._plugin_type = plugin_type
        self._logger = get_logger(f"FlextMeltanoPlugin.{name}")

    @property
    def name(self) -> str:
        """Plugin name from abstract interface."""
        return self._name

    @property
    def version(self) -> str:
        """Plugin version from abstract interface."""
        return self._version

    @property
    def plugin_type(self) -> str:
        """Plugin type for Meltano integration."""
        return self._plugin_type

    def initialize(self, context: FlextPluginContext) -> FlextResult[None]:
        """Initialize plugin with context from abstract interface."""
        try:
            # Use context for Meltano initialization if needed
            _ = context  # Acknowledge parameter for interface compliance
            self._logger.info("Meltano plugin initialized", plugin_name=self.name)
            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Meltano plugin initialization failed: {e}")

    def shutdown(self) -> FlextResult[None]:
        """Shutdown plugin and release resources from abstract interface."""
        try:
            self._logger.info("Meltano plugin shutdown", plugin_name=self.name)
            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Meltano plugin shutdown failed: {e}")

    def get_info(self) -> dict[str, object]:
        """Get plugin information from abstract interface."""
        return {
            "name": self.name,
            "version": self.version,
            "plugin_type": self.plugin_type,
            "status": "active",
        }

    def execute(self) -> FlextResult[object]:
        """Execute the plugin."""
        try:
            self._logger.info("Executing Meltano plugin", plugin_name=self.name)
            # Plugin-specific execution logic would go here
            return FlextResult[object].ok({"executed": True, "plugin": self.name})
        except Exception as e:
            return FlextResult[object].fail(f"Plugin execution failed: {e}")

    def cleanup(self) -> FlextResult[None]:
        """Cleanup plugin resources."""
        try:
            self._logger.info("Cleaning up Meltano plugin", plugin_name=self.name)
            # Delegate to shutdown for consistency
            return self.shutdown()
        except Exception as e:
            return FlextResult[None].fail(f"Plugin cleanup failed: {e}")


class FlextMeltanoPluginExecution:
    """Simple data class for plugin execution information - replaces FlextPluginExecution."""

    def __init__(self, plugin_name: str, input_data: dict[str, object]) -> None:
        """Initialize plugin execution."""
        self.plugin_name = plugin_name
        self.input_data = input_data


# FlextMeltanoPluginRegistry is defined later in the file with full implementation


# =============================================================================
# MELTANO DATA OPERATIONS - Using FlextMeltanoPlugin base class
# =============================================================================


class FlextMeltanoTapPlugin(FlextMeltanoPlugin):
    """Concrete Meltano tap plugin implementation extending FlextMeltanoPlugin.

    COMPLIANCE: Pure extension of FlextMeltanoPlugin from above, no mixing with flext-plugin.
    NO MIXING: Uses only flext-core patterns and Meltano execution layer.
    """

    def __init__(
        self,
        name: str,
        version: str = "2.0.0",
        config: dict[str, object] | None = None,
    ) -> None:
        """Initialize Meltano tap plugin."""
        super().__init__(name, version, "tap")
        self._config = config or {}
        self._executor: object | None = None  # FlextMeltanoExecutor

    def validate_config(self, config: dict[str, object]) -> FlextResult[None]:
        """Validate tap-specific configuration."""
        try:
            required_fields = []

            # Define common required fields by tap type
            if "postgres" in self.name:
                required_fields = ["host", "port", "user", "password", "dbname"]
            elif "csv" in self.name:
                required_fields = ["files"]
            elif "oracle" in self.name:
                required_fields = ["host", "port", "user", "password", "service_name"]

            # Validate required fields
            missing_fields = [field for field in required_fields if field not in config]

            if missing_fields:
                return FlextResult[None].fail(
                    f"Missing required fields for {self.name}: {missing_fields}",
                )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Config validation failed: {e}")

    def discover_catalog(self) -> FlextResult[dict[str, object]]:
        """Discover schema catalog for tap."""
        try:
            if not self._executor:
                return FlextResult[dict[str, object]].fail("Executor not initialized")

            # Execute discovery via Meltano executor
            # This would be implemented with actual Meltano execution
            return FlextResult[dict[str, object]].ok({"streams": []})  # Placeholder

        except Exception as e:
            return FlextResult[dict[str, object]].fail(f"Catalog discovery error: {e}")


class FlextMeltanoTargetPlugin(FlextMeltanoPlugin):
    """Concrete Meltano target plugin implementation extending FlextMeltanoPlugin.

    COMPLIANCE: Pure extension of FlextMeltanoPlugin, no domain entity mixing.
    NO MIXING: Uses only flext-core interfaces and Meltano-specific functionality.
    """

    def __init__(
        self,
        name: str,
        version: str = "2.0.0",
        config: dict[str, object] | None = None,
    ) -> None:
        """Initialize Meltano target plugin."""
        super().__init__(name, version, "target")
        self._config = config or {}
        self._executor: object | None = None  # FlextMeltanoExecutor

    def validate_config(self, config: dict[str, object]) -> FlextResult[None]:
        """Validate target-specific configuration."""
        try:
            required_fields = []

            # Define common required fields by target type
            if "postgres" in self.name:
                required_fields = ["host", "port", "user", "password", "dbname"]
            elif "csv" in self.name or "jsonl" in self.name:
                required_fields = ["destination_path"]

            # Validate required fields
            missing_fields = [field for field in required_fields if field not in config]

            if missing_fields:
                return FlextResult[None].fail(
                    f"Missing required fields for {self.name}: {missing_fields}",
                )

            return FlextResult[None].ok(None)
        except Exception as e:
            return FlextResult[None].fail(f"Config validation failed: {e}")


# =============================================================================
# FACTORY FUNCTIONS FOR CLEAN INSTANTIATION
# =============================================================================


def create_meltano_tap_plugin(
    name: str,
    version: str = "2.0.0",
    config: dict[str, object] | None = None,
) -> FlextResult[FlextMeltanoTapPlugin]:
    """Create a Meltano tap plugin using pure flext-core patterns.

    Args:
      name: Plugin name
      version: Plugin version
      config: Plugin configuration

    Returns:
      FlextResult containing the created tap plugin or error

    """
    try:
        plugin = FlextMeltanoTapPlugin(name=name, version=version, config=config)
        return FlextResult[FlextMeltanoTapPlugin].ok(plugin)
    except Exception as e:
        return FlextResult[FlextMeltanoTapPlugin].fail(
            f"Failed to create tap plugin: {e}"
        )


def create_meltano_target_plugin(
    name: str,
    version: str = "2.0.0",
    config: dict[str, object] | None = None,
) -> FlextResult[FlextMeltanoTargetPlugin]:
    """Create a Meltano target plugin using pure flext-core patterns.

    Args:
      name: Plugin name
      version: Plugin version
      config: Plugin configuration

    Returns:
      FlextResult containing the created target plugin or error

    """
    try:
        plugin = FlextMeltanoTargetPlugin(name=name, version=version, config=config)
        return FlextResult[FlextMeltanoTargetPlugin].ok(plugin)
    except Exception as e:
        return FlextResult[FlextMeltanoTargetPlugin].fail(
            f"Failed to create target plugin: {e}"
        )


class FlextMeltanoPluginContext:
    """Meltano-specific plugin context implementation.

    Provides plugins with access to Meltano-specific services, configuration,
    and logging. Implements the FlextPluginContext protocol.
    """

    def __init__(
        self,
        *,
        logger: BoundLogger,
        config: Mapping[str, object],
        meltano_config: FlextMeltanoConfig,
        services: dict[str, object] | None = None,
    ) -> None:
        """Initialize Meltano plugin context.

        Args:
            logger: Structured logger for plugin
            config: Plugin configuration
            meltano_config: Meltano-specific configuration
            services: Available services for plugin

        """
        self._logger = logger
        self._config = config
        self._meltano_config = meltano_config
        self._services = services or {}

    @property
    def logger(self) -> BoundLogger:
        """Get logger for plugin."""
        return self._logger

    @property
    def config(self) -> Mapping[str, object]:
        """Get plugin configuration."""
        return self._config

    @property
    def meltano_config(self) -> FlextMeltanoConfig:
        """Get Meltano-specific configuration."""
        return self._meltano_config

    def get_service(self, service_name: str) -> FlextResult[object]:
        """Get service by name from container.

        Args:
            service_name: Name of service to retrieve

        Returns:
            FlextResult with service instance or not found error

        """
        if service_name in self._services:
            return FlextResult[object].ok(self._services[service_name])

        # Try to resolve common Meltano services
        if service_name == "executor":
            result = create_executor(self._meltano_config)
            if result.success:
                self._services[service_name] = result.data
                return FlextResult[object].ok(result.data)

        return FlextResult[object].fail(f"Service '{service_name}' not found")


# FlextMeltanoPluginRegistry is now available from flext_meltano.models
# Use the centralized FlextModel-based implementation for better validation
