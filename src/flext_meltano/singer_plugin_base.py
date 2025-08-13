"""FLEXT Singer Plugin Base - Shared base for tap and target plugins.

This module provides the foundational implementation for all Singer tap and
target plugins in the FLEXT ecosystem. It implements the clean plugin
architecture interfaces from flext-core while providing Singer-specific
functionality.

Architecture:
    - Implements flext_core.FlextDataPlugin
    - Uses composition with FlextPluginEntity for domain logic
    - Provides Singer SDK integration points
    - Maintains clean separation of concerns

Classes:
    - FlextSingerPluginBase: Abstract base for Singer plugins
    - FlextTapPlugin: Base implementation for tap plugins
    - FlextTargetPlugin: Base implementation for target plugins
    - FlextSingerPluginContext: Singer-specific plugin context

Example:
    >>> from flext_meltano.singer_plugin_base import FlextTapPlugin
    >>> class MyTapPlugin(FlextTapPlugin):
    ...     def extract_data(self) -> FlextResult[object]:
    ...         # Custom extraction logic
    ...         return FlextResult.ok(data)

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from flext_core import FlextPlugin, FlextPluginContext, FlextResult, get_logger

if TYPE_CHECKING:
    from collections.abc import Mapping

    from flext_plugin.domain.entities import FlextPluginEntity
    from structlog.stdlib import BoundLogger


class FlextSingerPluginBase(FlextPlugin, ABC):
    """Abstract base class for all Singer plugins.

    Provides common functionality for tap and target plugins while
    implementing the FlextDataPlugin interface from flext-core.

    Attributes:
        _name: Plugin name
        _version: Plugin version
        _plugin_type: Singer plugin type (tap/target)
        _entity: Domain entity for business logic
        _config: Plugin configuration
        _catalog: Singer catalog
        _logger: Structured logger
        _initialized: Initialization state

    """

    def __init__(
        self,
        name: str,
        version: str,
        plugin_type: str,
        config: dict[str, object] | None = None,
        entity: FlextPluginEntity | None = None,
    ) -> None:
        """Initialize Singer plugin base.

        Args:
            name: Plugin name
            version: Plugin version
            plugin_type: Plugin type (tap/target)
            config: Plugin configuration
            entity: Optional domain entity

        """
        self._name = name
        self._version = version
        self._plugin_type = plugin_type
        self._entity = entity
        self._config = config or {}
        self._catalog: dict[str, object] = {}
        self._logger = get_logger(f"singer.{plugin_type}.{name}")
        self._initialized = False
        self._connection_valid = False

    @property
    def name(self) -> str:
        """Get plugin name."""
        return self._name

    @property
    def version(self) -> str:
        """Get plugin version."""
        return self._version

    @property
    def plugin_type(self) -> str:
        """Get plugin type (tap/target)."""
        return self._plugin_type

    @property
    def catalog(self) -> dict[str, object]:
        """Get Singer catalog."""
        return self._catalog

    def initialize(self, context: FlextPluginContext) -> FlextResult[None]:
        """Initialize plugin with context.

        Args:
            context: Plugin runtime context

        Returns:
            FlextResult indicating success or failure

        """
        try:
            self._logger.info(
                f"Initializing {self._plugin_type} plugin {self.name} v{self.version}",
            )

            # Merge context config with instance config
            context_config = context.get_config() or {}
            self._config.update(context_config)

            # Validate configuration
            validation_result = self.validate_config(self._config)
            if not validation_result.success:
                return validation_result

            # Activate entity if present
            if self._entity:
                entity_validation = self._entity.validate_business_rules()
                if not entity_validation.success:
                    return entity_validation

                if self._entity.activate():
                    self._logger.info(f"Plugin entity {self.name} activated")

            # Perform Singer-specific initialization
            init_result = self._singer_initialize()
            if not init_result.success:
                return init_result

            self._initialized = True
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception("Failed to initialize {self._plugin_type} {self.name}")
            return FlextResult.fail(f"Initialization failed: {e!s}")

    def shutdown(self) -> FlextResult[None]:
        """Shutdown plugin and release resources.

        Returns:
            FlextResult indicating success or failure

        """
        try:
            self._logger.info(f"Shutting down {self._plugin_type} {self.name}")

            # Perform Singer-specific cleanup
            cleanup_result = self._singer_cleanup()
            if not cleanup_result.success:
                self._logger.warning(f"Cleanup warning: {cleanup_result.error}")

            # Deactivate entity if present
            if self._entity and self._entity.deactivate():
                self._logger.info(f"Plugin entity {self.name} deactivated")

            self._initialized = False
            self._connection_valid = False
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception("Failed to shutdown plugin")
            return FlextResult.fail(f"Shutdown failed: {e!s}")

    def validate_config(self, config: Mapping[str, object]) -> FlextResult[None]:
        """Validate plugin configuration.

        Args:
            config: Configuration to validate

        Returns:
            FlextResult indicating validation success or errors

        """
        try:
            # Check for required Singer fields
            required_fields = self._get_required_config_fields()
            missing_fields = [f for f in required_fields if f not in config]

            if missing_fields:
                return FlextResult.fail(
                    f"Missing required configuration fields: {missing_fields}",
                )

            # Perform plugin-specific validation
            specific_validation = self._validate_specific_config(config)
            if not specific_validation.success:
                return specific_validation

            self._config.update(config)
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception("Configuration validation failed")
            return FlextResult.fail(f"Validation error: {e!s}")

    def test_connection(self) -> FlextResult[None]:
        """Test connection to data source/destination.

        Returns:
            FlextResult indicating connection success or failure

        """
        try:
            self._logger.info(f"Testing connection for {self._plugin_type} {self.name}")

            if not self._config:
                return FlextResult.fail("No configuration available for connection test")

            # Perform plugin-specific connection test
            test_result = self._test_specific_connection()
            if not test_result.success:
                self._connection_valid = False
                return test_result

            self._connection_valid = True
            self._logger.info(f"Connection test successful for {self.name}")
            return FlextResult.ok(None)

        except Exception as e:
            self._logger.exception("Connection test failed")
            self._connection_valid = False
            return FlextResult.fail(f"Connection test error: {e!s}")

    @abstractmethod
    def _singer_initialize(self) -> FlextResult[None]:
        """Perform Singer-specific initialization.

        Returns:
            FlextResult indicating success or failure

        """
        ...

    @abstractmethod
    def _singer_cleanup(self) -> FlextResult[None]:
        """Perform Singer-specific cleanup.

        Returns:
            FlextResult indicating success or failure

        """
        ...

    @abstractmethod
    def _get_required_config_fields(self) -> list[str]:
        """Get list of required configuration fields.

        Returns:
            List of required field names

        """
        ...

    @abstractmethod
    def _validate_specific_config(self, config: Mapping[str, object]) -> FlextResult[None]:
        """Perform plugin-specific configuration validation.

        Args:
            config: Configuration to validate

        Returns:
            FlextResult indicating validation success or errors

        """
        ...

    @abstractmethod
    def _test_specific_connection(self) -> FlextResult[None]:
        """Perform plugin-specific connection test.

        Returns:
            FlextResult indicating connection success or failure

        """
        ...


class FlextTapPlugin(FlextSingerPluginBase):
    """Base implementation for Singer tap plugins.

    Provides extraction-specific functionality for tap plugins.
    """

    def __init__(
        self,
        name: str,
        version: str,
        config: dict[str, object] | None = None,
        entity: FlextPluginEntity | None = None,
    ) -> None:
        """Initialize tap plugin.

        Args:
            name: Plugin name
            version: Plugin version
            config: Plugin configuration
            entity: Optional domain entity

        """
        super().__init__(name, version, "tap", config, entity)
        self._discovered_streams: list[str] = []
        self._selected_streams: list[str] = []

    @property
    def discovered_streams(self) -> list[str]:
        """Get list of discovered streams."""
        return self._discovered_streams

    @property
    def selected_streams(self) -> list[str]:
        """Get list of selected streams."""
        return self._selected_streams

    def discover_catalog(self) -> FlextResult[dict[str, object]]:
        """Discover available streams and schemas.

        Returns:
            FlextResult containing catalog or error

        """
        try:
            if not self._initialized:
                return FlextResult.fail("Plugin not initialized")

            if not self._connection_valid:
                test_result = self.test_connection()
                if not test_result.success:
                    return FlextResult.fail(f"Connection required: {test_result.error}")

            self._logger.info(f"Discovering catalog for tap {self.name}")

            # Perform tap-specific discovery
            discovery_result = self._discover_tap_catalog()
            if not discovery_result.success:
                return discovery_result

            self._catalog = discovery_result.data or {}
            streams_obj = self._catalog.get("streams", {})
            if isinstance(streams_obj, dict):
                self._discovered_streams = list(streams_obj.keys())
            else:
                self._discovered_streams = []

            return FlextResult.ok(self._catalog)

        except Exception as e:
            self._logger.exception("Catalog discovery failed")
            return FlextResult.fail(f"Discovery error: {e!s}")

    def select_streams(self, stream_names: list[str]) -> FlextResult[None]:
        """Select streams for extraction.

        Args:
            stream_names: List of stream names to select

        Returns:
            FlextResult indicating success or failure

        """
        if not self._discovered_streams:
            return FlextResult.fail("No streams discovered. Run discover_catalog first.")

        invalid_streams = [s for s in stream_names if s not in self._discovered_streams]
        if invalid_streams:
            return FlextResult.fail(f"Invalid streams: {invalid_streams}")

        self._selected_streams = stream_names
        self._logger.info(f"Selected {len(stream_names)} streams for extraction")
        return FlextResult.ok(None)

    def extract_data(self) -> FlextResult[object]:
        """Extract data from selected streams.

        Returns:
            FlextResult containing extracted data or error

        """
        try:
            if not self._initialized:
                return FlextResult.fail("Plugin not initialized")

            if not self._selected_streams:
                return FlextResult.fail("No streams selected for extraction")

            self._logger.info(f"Extracting data from {len(self._selected_streams)} streams")

            # Record execution in entity if present
            if self._entity:
                self._entity.record_execution(0.0, success=True)

            # Perform tap-specific extraction
            extraction_result = self._extract_tap_data()

            if not extraction_result.success and self._entity:
                self._entity.record_error(extraction_result.error or "Extraction failed")

            return extraction_result

        except Exception as e:
            self._logger.exception("Data extraction failed")
            if self._entity:
                self._entity.record_error(str(e))
            return FlextResult.fail(f"Extraction error: {e!s}")

    @abstractmethod
    def _discover_tap_catalog(self) -> FlextResult[dict[str, object]]:
        """Perform tap-specific catalog discovery.

        Returns:
            FlextResult containing catalog or error

        """
        ...

    @abstractmethod
    def _extract_tap_data(self) -> FlextResult[object]:
        """Perform tap-specific data extraction.

        Returns:
            FlextResult containing extracted data or error

        """
        ...

    def _singer_initialize(self) -> FlextResult[None]:
        """Perform Singer tap initialization."""
        # Default implementation - can be overridden
        return FlextResult.ok(None)

    def _singer_cleanup(self) -> FlextResult[None]:
        """Perform Singer tap cleanup."""
        # Default implementation - can be overridden
        self._discovered_streams.clear()
        self._selected_streams.clear()
        self._catalog.clear()
        return FlextResult.ok(None)


class FlextTargetPlugin(FlextSingerPluginBase):
    """Base implementation for Singer target plugins.

    Provides loading-specific functionality for target plugins.
    """

    def __init__(
        self,
        name: str,
        version: str,
        config: dict[str, object] | None = None,
        entity: FlextPluginEntity | None = None,
    ) -> None:
        """Initialize target plugin.

        Args:
            name: Plugin name
            version: Plugin version
            config: Plugin configuration
            entity: Optional domain entity

        """
        super().__init__(name, version, "target", config, entity)
        self._loaded_count = 0
        self._error_count = 0

    @property
    def loaded_count(self) -> int:
        """Get count of successfully loaded records."""
        return self._loaded_count

    @property
    def error_count(self) -> int:
        """Get count of failed records."""
        return self._error_count

    def load_data(self, data: object) -> FlextResult[dict[str, object]]:
        """Load data to destination.

        Args:
            data: Data to load (Singer messages)

        Returns:
            FlextResult containing load statistics or error

        """
        try:
            if not self._initialized:
                return FlextResult.fail("Plugin not initialized")

            if not self._connection_valid:
                test_result = self.test_connection()
                if not test_result.success:
                    return FlextResult.fail(f"Connection required: {test_result.error}")

            self._logger.info(f"Loading data with target {self.name}")

            # Record execution in entity if present
            if self._entity:
                self._entity.record_execution(0.0, success=True)

            # Perform target-specific loading
            load_result = self._load_target_data(data)

            if not load_result.success:
                if self._entity:
                    self._entity.record_error(load_result.error or "Load failed")
                return load_result

            # Update statistics
            stats = load_result.data
            if isinstance(stats, dict):
                loaded = stats.get("loaded", 0)
                errors = stats.get("errors", 0)
                if isinstance(loaded, int):
                    self._loaded_count += loaded
                if isinstance(errors, int):
                    self._error_count += errors

            return load_result

        except Exception as e:
            self._logger.exception("Data loading failed")
            if self._entity:
                self._entity.record_error(str(e))
            return FlextResult.fail(f"Load error: {e!s}")

    def get_load_statistics(self) -> dict[str, object]:
        """Get loading statistics.

        Returns:
            Dictionary with load statistics

        """
        return {
            "loaded_count": self._loaded_count,
            "error_count": self._error_count,
            "success_rate": (
                self._loaded_count / (self._loaded_count + self._error_count)
                if (self._loaded_count + self._error_count) > 0
                else 0.0
            ),
        }

    @abstractmethod
    def _load_target_data(self, data: object) -> FlextResult[dict[str, object]]:
        """Perform target-specific data loading.

        Args:
            data: Data to load

        Returns:
            FlextResult containing load statistics or error

        """
        ...

    def _singer_initialize(self) -> FlextResult[None]:
        """Perform Singer target initialization."""
        # Default implementation - can be overridden
        self._loaded_count = 0
        self._error_count = 0
        return FlextResult.ok(None)

    def _singer_cleanup(self) -> FlextResult[None]:
        """Perform Singer target cleanup."""
        # Default implementation - can be overridden
        return FlextResult.ok(None)


class FlextSingerPluginContext(FlextPluginContext):
    """Singer-specific plugin context implementation.

    Provides Singer plugins with access to Meltano services and configuration.
    """

    def __init__(
        self,
        logger: BoundLogger,
        config: dict[str, object] | None = None,
        meltano_project: object | None = None,
        singer_io: object | None = None,
    ) -> None:
        """Initialize Singer plugin context.

        Args:
            logger: Structured logger
            config: Plugin configuration
            meltano_project: Meltano project instance
            singer_io: Singer I/O handler

        """
        self._logger = logger
        self._config = config or {}
        self._meltano_project = meltano_project
        self._singer_io = singer_io
        self._services: dict[str, object] = {
            "meltano_project": meltano_project,
            "singer_io": singer_io,
        }

    @property
    def logger(self) -> BoundLogger:
        """Get logger for plugin."""
        return self._logger

    @property
    def config(self) -> dict[str, object]:
        """Get plugin configuration."""
        return dict(self._config)

    def get_service(self, service_name: str) -> FlextResult[object]:
        """Get service by name.

        Args:
            service_name: Name of service to retrieve

        Returns:
            FlextResult with service instance or not found error

        """
        if service_name not in self._services:
            return FlextResult.fail(f"Service not found: {service_name}")

        service = self._services[service_name]
        if service is None:
            return FlextResult.fail(f"Service {service_name} not initialized")

        return FlextResult.ok(service)
