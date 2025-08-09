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
    ...     config={"description": "CSV tap for Meltano"}
    ... )
    >>>
    >>> # Use plugin functionality
    >>> result = plugin.validate_config({"path": "/data/file.csv"})

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult
from flext_core.protocols import (
    FlextPlugin,
    FlextPluginContext,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from structlog.stdlib import BoundLogger

    from flext_meltano.config import FlextMeltanoConfig

from flext_core import get_logger

# Import create_executor function to fix F821 error
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
            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Meltano plugin initialization failed: {e}")

    def shutdown(self) -> FlextResult[None]:
        """Shutdown plugin and release resources from abstract interface."""
        try:
            self._logger.info("Meltano plugin shutdown", plugin_name=self.name)
            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Meltano plugin shutdown failed: {e}")

    def get_info(self) -> dict[str, object]:
        """Get plugin information from abstract interface."""
        return {
            "name": self.name,
            "version": self.version,
            "plugin_type": self.plugin_type,
            "status": "active",
        }


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

    def __init__(self, name: str, version: str = "2.0.0", config: dict[str, object] | None = None) -> None:
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
                return FlextResult.fail(f"Missing required fields for {self.name}: {missing_fields}")

            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Config validation failed: {e}")

    def discover_catalog(self) -> FlextResult[dict[str, object]]:
        """Discover schema catalog for tap."""
        try:
            if not self._executor:
                return FlextResult.fail("Executor not initialized")

            # Execute discovery via Meltano executor
            # This would be implemented with actual Meltano execution
            return FlextResult.ok({"streams": []})  # Placeholder

        except Exception as e:
            return FlextResult.fail(f"Catalog discovery error: {e}")


class FlextMeltanoTargetPlugin(FlextMeltanoPlugin):
    """Concrete Meltano target plugin implementation extending FlextMeltanoPlugin.

    COMPLIANCE: Pure extension of FlextMeltanoPlugin, no domain entity mixing.
    NO MIXING: Uses only flext-core interfaces and Meltano-specific functionality.
    """

    def __init__(self, name: str, version: str = "2.0.0", config: dict[str, object] | None = None) -> None:
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
                return FlextResult.fail(f"Missing required fields for {self.name}: {missing_fields}")

            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Config validation failed: {e}")


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
        return FlextResult.ok(plugin)
    except Exception as e:
        return FlextResult.fail(f"Failed to create tap plugin: {e}")


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
        return FlextResult.ok(plugin)
    except Exception as e:
        return FlextResult.fail(f"Failed to create target plugin: {e}")


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
        services: dict[str, Any] | None = None,
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
            return FlextResult.ok(self._services[service_name])

        # Try to resolve common Meltano services
        if service_name == "executor":
            result = create_executor(self._meltano_config)
            if result.success:
                self._services[service_name] = result.data
                return FlextResult.ok(result.data)

        return FlextResult.fail(f"Service '{service_name}' not found")


class FlextMeltanoPluginRegistry:
    """Meltano-specific plugin registry implementation.

    Simple plugin registry using only flext-core patterns, no domain entity mixing.
    COMPLIANCE: Uses only FlextMeltanoPlugin concrete implementations.
    """

    def __init__(self, name: str = "default") -> None:
        """Initialize registry with simple data storage.

        Args:
            name: Registry name for identification

        """
        self.name = name
        self._meltano_plugins: dict[str, FlextMeltanoPlugin] = {}

    def register(self, plugin: FlextMeltanoPlugin) -> FlextResult[None]:
        """Register a Meltano plugin.

        Args:
            plugin: Plugin instance to register

        Returns:
            FlextResult indicating registration success or failure

        """
        try:
            # Store Meltano plugin using simple registry pattern
            self._meltano_plugins[plugin.name] = plugin
            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Plugin registration failed: {e}")

    def unregister(self, plugin_name: str) -> FlextResult[None]:
        """Unregister a plugin by name.

        Args:
            plugin_name: Name of plugin to unregister

        Returns:
            FlextResult indicating success or not found error

        """
        try:
            if plugin_name in self._meltano_plugins:
                self._meltano_plugins.pop(plugin_name)
                return FlextResult.ok(None)
            return FlextResult.fail(f"Plugin '{plugin_name}' not found")

        except Exception as e:
            return FlextResult.fail(f"Plugin unregistration failed: {e}")

    def get_plugin(self, plugin_name: str) -> FlextResult[FlextMeltanoPlugin]:
        """Get plugin by name.

        Args:
            plugin_name: Name of plugin to retrieve

        Returns:
            FlextResult containing plugin or not found error

        """
        if plugin_name in self._meltano_plugins:
            return FlextResult.ok(self._meltano_plugins[plugin_name])

        return FlextResult.fail(f"Plugin '{plugin_name}' not found")

    def list_plugins(self) -> list[str]:
        """List all registered plugin names.

        Returns:
            List of registered plugin names

        """
        return list(self._meltano_plugins.keys())

# Factory functions for clean instantiation using pure flext-core patterns


def create_meltano_plugin_registry(
    name: str = "default",
) -> FlextResult[FlextMeltanoPluginRegistry]:
    """Create a Meltano plugin registry using pure flext-core patterns.

    Args:
        name: Registry name

    Returns:
        FlextResult containing the created registry or error

    """
    try:
        # Create registry implementation with simple data storage
        registry = FlextMeltanoPluginRegistry(name=name)
        return FlextResult.ok(registry)

    except Exception as e:
        return FlextResult.fail(f"Failed to create registry: {e}")
