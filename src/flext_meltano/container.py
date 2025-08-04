"""FLEXT Meltano Container - Centralized Dependency Injection Management.

**Architecture Layer**: Infrastructure Layer
**Status**: ✅ STABLE - Dependency injection container with enterprise patterns
**Dependencies**: flext-core (FlextContainer, ServiceKey), service factories

## Module Purpose

This module provides **centralized dependency injection container** for FLEXT
Meltano's bridge architecture, extending flext-core's dependency injection
patterns with Meltano-specific service registration and lifecycle management
for consistent service instantiation across the bridge ecosystem.

## Design Principles

1. **Container Extension**: Extends FlextContainer with Meltano-specific patterns
2. **Service Lifecycle**: Managed service creation and registration
3. **Factory Pattern**: Factory-based service instantiation for flexibility
4. **Type Safety**: Strict type checking and safe service resolution
5. **Bridge Integration**: Container services designed for Go service consumption

## Core Components

### FlextMeltanoContainer
- **Service Registration**: Automated registration of core Meltano services
- **Factory Management**: Factory-based service creation with type safety
- **Configuration Management**: Centralized configuration injection
- **Service Resolution**: Type-safe service resolution with error handling

### Service Categories
- **Core Services**: Configuration and base service management
- **Singer Services**: Tap, target, and DBT service factories
- **Operational Services**: Discovery, execution, installation, validation services
- **Custom Services**: User-defined service registration support

## Usage Patterns

### Container Initialization
```python
from flext_meltano.container import get_meltano_container, configure_meltano_container

# Get global container (auto-initialized)
container = get_meltano_container()

# Configure with custom settings
custom_config = FlextMeltanoConfig(project_root="/custom/path")
result = configure_meltano_container(custom_config)
if result.success:
    print("Container configured successfully")
```

### Service Creation
```python
from flext_meltano.container import get_meltano_container

container = get_meltano_container()

# Create tap service
tap_result = container.create_tap_service()
if tap_result.success:
    tap_service = tap_result.data
    # Use tap service for data extraction

# Create target service with custom config
custom_config = FlextMeltanoConfig(project_root="/data/warehouse")
target_result = container.create_target_service(custom_config)
if target_result.success:
    target_service = target_result.data
    # Use target service for data loading

# Create executor
executor_result = container.create_executor()
if executor_result.success:
    executor = executor_result.data
    # Use executor for pipeline operations
```

### Service Registration
```python
from flext_meltano.container import get_meltano_container

container = get_meltano_container()

# Register custom service
custom_service = MyCustomMeltanoService()
result = container.register_service("custom_service", custom_service)
if result.success:
    print("Custom service registered")

# Retrieve registered service
service_result = container.get_service("custom_service")
if service_result.success:
    service = service_result.data
    # Use retrieved service
```

## Service Factory Patterns

### Singer Service Factories
```python
# Container automatically registers these factories:
# - tap_service_factory: create_meltano_tap_service
# - target_service_factory: create_meltano_target_service
# - dbt_service_factory: create_meltano_dbt_service

# Factory usage through container
container = get_meltano_container()
tap_result = container.create_tap_service(config)
# Internally calls: create_meltano_tap_service(config)
```

### Operational Service Factories
```python
# Container automatically registers these factories:
# - discoverer_factory: create_discoverer
# - executor_factory: create_executor
# - installer_factory: create_installer_service
# - validation_factory: create_validation_service

# Factory usage through container
container = get_meltano_container()
executor_result = container.create_executor(config)
# Internally calls: create_executor(config)
```

## Bridge Integration Patterns

### Go Service Integration
```go
// Go service using container via bridge
func (c *FlextMeltanoClient) GetMeltanoServices() (*MeltanoServices, error) {
    cmd := exec.Command("python", "-c", `
from flext_meltano.container import get_meltano_container
import json

container = get_meltano_container()

# Create all core services
services = {}
tap_result = container.create_tap_service()
if tap_result.success:
    services["tap_available"] = True

target_result = container.create_target_service()
if target_result.success:
    services["target_available"] = True

executor_result = container.create_executor()
if executor_result.success:
    services["executor_available"] = True

print(json.dumps(services))
    `)

    output, err := cmd.Output()
    if err != nil {
        return nil, fmt.Errorf("failed to get Meltano services: %w", err)
    }

    var services MeltanoServices
    err = json.Unmarshal(output, &services)
    return &services, err
}
```

### Container Configuration Bridge
```python
# Bridge operations for container configuration
def bridge_configure_meltano_container(config_json: str) -> Dict[str, Any]:
    '''Configure Meltano container with JSON config for Go services.'''
    try:
        config_data = json.loads(config_json)
        config = FlextMeltanoConfig(**config_data)

        result = configure_meltano_container(config)

        return {
            "success": result.success,
            "container_configured": result.success,
            "error": result.error_message if result.is_failure else None
        }
    except Exception as e:
        return {
            "success": False,
            "container_configured": False,
            "error": str(e)
        }

def bridge_create_meltano_services() -> Dict[str, Any]:
    '''Create all Meltano services for Go service consumption.'''
    container = get_meltano_container()
    services_created = {}

    # Create each service type
    for service_name, factory_method in [
        ("tap", container.create_tap_service),
        ("target", container.create_target_service),
        ("executor", container.create_executor)
    ]:
        result = factory_method()
        services_created[f"{service_name}_service"] = {
            "available": result.success,
            "error": result.error_message if result.is_failure else None
        }

    return {
        "success": True,
        "services": services_created
    }
```

## Integration Points

### Bridge Module Integration (After Implementation)
- FlextMeltanoBridge uses container for service resolution
- Dependency injection for bridge operations
- Service lifecycle management for Go integration
- Configuration injection for bridge operations

### Meltano Operations Integration
- All Meltano operations use container services
- Consistent service instantiation across modules
- Configuration management for project-specific operations
- Service factory pattern for flexible instantiation

### Testing Integration
- Container services for test setup and teardown
- Mock service registration for unit testing
- Service isolation for integration testing
- Configuration override for test environments

## Quality Standards

### Dependency Injection Excellence
- **Type Safety**: Strict type checking and safe service resolution
- **Service Lifecycle**: Proper initialization and cleanup patterns
- **Factory Pattern**: Flexible service instantiation with consistent interfaces
- **Error Handling**: Comprehensive error handling with context preservation

### Enterprise Integration
- **Container Extension**: Proper extension of flext-core container patterns
- **Service Registration**: Automated registration with conflict detection
- **Configuration Management**: Centralized configuration with validation
- **Bridge Compatibility**: Services designed for subprocess consumption

## Service Registration Architecture

### Automatic Registration
```python
# Core services (configuration)
register_typed(container, ServiceKey("meltano_config"), FlextMeltanoConfig())

# Singer service factories
register_typed(container, ServiceKey("tap_service_factory"), create_meltano_tap_service)
register_typed(
    container, ServiceKey("target_service_factory"), create_meltano_target_service
)
register_typed(container, ServiceKey("dbt_service_factory"), create_meltano_dbt_service)

# Operational service factories
register_typed(container, ServiceKey("discoverer_factory"), create_discoverer)
register_typed(container, ServiceKey("executor_factory"), create_executor)
register_typed(container, ServiceKey("installer_factory"), create_installer_service)
register_typed(container, ServiceKey("validation_factory"), create_validation_service)
```

### Custom Service Registration
```python
# Register custom services with container
container = get_meltano_container()
result = container.register_service("custom_analytics", MyAnalyticsService())
if result.success:
    # Service available for injection throughout application
    pass
```

This module provides essential **dependency injection container capabilities**
for FLEXT Meltano's bridge architecture, enabling consistent service management
and configuration injection across the entire ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from flext_core import (
    FlextResult,
    ServiceKey,
    get_flext_container,
    register_typed,
)

if TYPE_CHECKING:
    from collections.abc import Callable

from flext_meltano.base import (
    FlextMeltanoConfig,
    create_meltano_dbt_service,
    create_meltano_tap_service,
    create_meltano_target_service,
)
from flext_meltano.discovery import create_discoverer
from flext_meltano.execution import create_executor
from flext_meltano.installation import create_installer_service
from flext_meltano.validation import create_validation_service

if TYPE_CHECKING:
    from flext_meltano.base import (
        FlextMeltanoTapService,
        FlextMeltanoTargetService,
    )
    from flext_meltano.execution import FlextMeltanoExecutor


class FlextMeltanoContainer:
    """Meltano-specific dependency injection container.

    Extends FlextContainer with Meltano-specific service registration patterns.
    """

    def __init__(self) -> None:
        """Initialize Meltano container with core container."""
        self._core_container = get_flext_container()
        self._initialized = False

    def initialize(self) -> FlextResult[None]:
        """Initialize container with default Meltano services."""
        try:
            # Register core Meltano services
            self._register_core_services()

            # Register Singer services
            self._register_singer_services()

            # Register operational services
            self._register_operational_services()

            self._initialized = True
            return FlextResult.ok(None)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Container initialization failed: {e}")

    def _register_core_services(self) -> None:
        """Register core Meltano services."""
        # Register default configuration
        default_config = FlextMeltanoConfig()
        register_typed(
            self._core_container,
            ServiceKey("meltano_config"),
            default_config,
        )

    def _register_singer_services(self) -> None:
        """Register Singer-related services."""
        # Register factory functions for Singer services
        register_typed(
            self._core_container,
            ServiceKey("tap_service_factory"),
            create_meltano_tap_service,
        )

        register_typed(
            self._core_container,
            ServiceKey("target_service_factory"),
            create_meltano_target_service,
        )

        register_typed(
            self._core_container,
            ServiceKey("dbt_service_factory"),
            create_meltano_dbt_service,
        )

    def _register_operational_services(self) -> None:
        """Register operational services (discovery, execution, etc.)."""
        # Register factory functions for operational services
        register_typed(
            self._core_container,
            ServiceKey("discoverer_factory"),
            create_discoverer,
        )

        register_typed(
            self._core_container,
            ServiceKey("executor_factory"),
            create_executor,
        )

        register_typed(
            self._core_container,
            ServiceKey("installer_factory"),
            create_installer_service,
        )

        register_typed(
            self._core_container,
            ServiceKey("validation_factory"),
            create_validation_service,
        )

    def get_service(self, service_key: str) -> FlextResult[object]:
        """Get service from container.

        Args:
            service_key: Service identifier

        Returns:
            FlextResult containing the service or error

        """
        if not self._initialized:
            return FlextResult.fail("Container not initialized")

        return self._core_container.get(service_key)

    def register_service(
        self,
        service_key: str,
        service_instance: object,
    ) -> FlextResult[None]:
        """Register service in container.

        Args:
            service_key: Service identifier
            service_instance: Service instance to register

        Returns:
            FlextResult indicating success or failure

        """
        try:
            register_typed(
                self._core_container,
                ServiceKey(service_key),
                service_instance,
            )
            return FlextResult.ok(None)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Service registration failed: {e}")

    def create_tap_service(
        self,
        config: FlextMeltanoConfig | None = None,
    ) -> FlextResult[FlextMeltanoTapService]:
        """Create tap service instance.

        Args:
            config: Optional configuration, uses default if None

        Returns:
            FlextResult containing tap service instance

        """
        try:
            if config is None:
                config_result = self.get_service("meltano_config")
                if config_result.is_failure:
                    return FlextResult.fail(
                        config_result.error or "Failed to get config",
                    )

                # Type-safe config extraction
                config_data = config_result.data
                if not isinstance(config_data, FlextMeltanoConfig):
                    return FlextResult.fail("Invalid config type")
                config = config_data

            factory_result = self.get_service("tap_service_factory")
            if factory_result.is_failure:
                return FlextResult.fail(factory_result.error or "Failed to get factory")

            # Type-safe factory extraction
            factory_data = factory_result.data
            if not callable(factory_data):
                return FlextResult.fail("Factory is not callable")

            # Call factory with proper typing
            factory = cast(
                "Callable[[FlextMeltanoConfig], FlextResult[FlextMeltanoTapService]]",
                factory_data,
            )
            return factory(config)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Tap service creation failed: {e}")

    def create_target_service(
        self,
        config: FlextMeltanoConfig | None = None,
    ) -> FlextResult[FlextMeltanoTargetService]:
        """Create target service instance.

        Args:
            config: Optional configuration, uses default if None

        Returns:
            FlextResult containing target service instance

        """
        try:
            if config is None:
                config_result = self.get_service("meltano_config")
                if config_result.is_failure:
                    return FlextResult.fail(
                        config_result.error or "Failed to get config",
                    )

                # Type-safe config extraction
                config_data = config_result.data
                if not isinstance(config_data, FlextMeltanoConfig):
                    return FlextResult.fail("Invalid config type")
                config = config_data

            factory_result = self.get_service("target_service_factory")
            if factory_result.is_failure:
                return FlextResult.fail(factory_result.error or "Failed to get factory")

            # Type-safe factory extraction
            factory_data = factory_result.data
            if not callable(factory_data):
                return FlextResult.fail("Factory is not callable")

            # Call factory with proper typing
            factory = cast(
                "Callable[[FlextMeltanoConfig], FlextResult[FlextMeltanoTargetService]]",
                factory_data,
            )
            return factory(config)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Target service creation failed: {e}")

    def create_executor(
        self,
        config: FlextMeltanoConfig | None = None,
    ) -> FlextResult[FlextMeltanoExecutor]:
        """Create executor instance.

        Args:
            config: Optional configuration, uses default if None

        Returns:
            FlextResult containing executor instance

        """
        try:
            if config is None:
                config_result = self.get_service("meltano_config")
                if config_result.is_failure:
                    return FlextResult.fail(
                        config_result.error or "Failed to get config",
                    )

                # Type-safe config extraction
                config_data = config_result.data
                if not isinstance(config_data, FlextMeltanoConfig):
                    return FlextResult.fail("Invalid config type")
                config = config_data

            factory_result = self.get_service("executor_factory")
            if factory_result.is_failure:
                return FlextResult.fail(factory_result.error or "Failed to get factory")

            # Type-safe factory extraction
            factory_data = factory_result.data
            if not callable(factory_data):
                return FlextResult.fail("Factory is not callable")

            # Call factory with proper typing
            factory = cast(
                "Callable[[FlextMeltanoConfig], FlextResult[FlextMeltanoExecutor]]",
                factory_data,
            )
            return factory(config)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Executor creation failed: {e}")


# Global container instance
_meltano_container: FlextMeltanoContainer | None = None


def get_meltano_container() -> FlextMeltanoContainer:
    """Get global Meltano container instance.

    Returns:
        Global FlextMeltanoContainer instance

    """
    global _meltano_container  # noqa: PLW0603
    if _meltano_container is None:
        _meltano_container = FlextMeltanoContainer()
        # Initialize with default services
        init_result = _meltano_container.initialize()
        if init_result.is_failure:
            error_msg: str = f"Container initialization failed: {init_result.error}"
            raise RuntimeError(error_msg)

    return _meltano_container


def configure_meltano_container(
    custom_config: FlextMeltanoConfig | None = None,
) -> FlextResult[None]:
    """Configure Meltano container with custom settings.

    Args:
        custom_config: Custom configuration to use

    Returns:
        FlextResult indicating success or failure

    """
    try:
        container = get_meltano_container()

        if custom_config is not None:
            register_result = container.register_service(
                "meltano_config",
                custom_config,
            )
            if register_result.is_failure:
                return register_result

        return FlextResult.ok(None)

    except (ValueError, TypeError) as e:
        return FlextResult.fail(f"Container configuration failed: {e}")


# Clean public API
__all__: list[str] = [
    "FlextMeltanoContainer",
    "configure_meltano_container",
    "get_meltano_container",
]
