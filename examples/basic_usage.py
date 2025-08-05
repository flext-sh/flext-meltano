"""FLEXT Meltano Basic Usage Examples - Foundation Patterns.

**Purpose**: Demonstrate fundamental FLEXT Meltano bridge library usage patterns
**Scope**: Configuration management, service creation, basic operations, result handling
**Target Audience**: New developers learning FLEXT Meltano integration patterns
**Dependencies**: flext-core (FlextResult patterns), minimal infrastructure requirements

## Overview

This example demonstrates the essential patterns for integrating FLEXT Meltano's
Go ↔ Python bridge library into applications, focusing on:

1. **Configuration Management**: Environment-aware settings with validation
2. **Service Creation**: Factory patterns with dependency injection
3. **Result Handling**: FlextResult railway-oriented programming patterns
4. **Error Management**: Enterprise-grade error handling and recovery
5. **Bridge Integration**: JSON-serializable operations for Go service consumption

## Usage

```bash
python basic_usage.py
```

## Expected Output

The example will demonstrate:
- Configuration initialization with various settings
- Service creation using factory functions
- Basic operations with proper error handling
- Result validation and data extraction patterns

All operations use mocked components to avoid external dependencies,
making this example suitable for learning and development environments.

## Architecture Alignment

Examples follow FLEXT Meltano's foundation layer patterns:
- **Value Objects**: Configuration as immutable value objects
- **Factory Pattern**: Consistent service creation with DI container
- **Railway Programming**: FlextResult for error handling
- **Bridge Compatibility**: All results are JSON-serializable for Go services
"""

import traceback
import warnings

from flext_meltano import (
    FlextMeltanoConfig,
    FlextMeltanoDiscoverer,
    FlextMeltanoExecutor,
    FlextMeltanoInstaller,
    FlextMeltanoValidationService,
    PropertiesList,
    Property,
    create_discoverer,
    create_executor,
    create_installer_service,
    create_meltano_dbt_service,
    create_validation_service,
    flext_meltano_discover_plugins,
    singer_typing,
)


def example_basic_configuration() -> None:
    """Demonstrate basic configuration setup."""
    # Create basic configuration
    FlextMeltanoConfig(
        project_root="./my_meltano_project",
        environment="dev",
    )


def example_service_creation() -> None:
    """Demonstrate service creation using factory functions."""
    config = FlextMeltanoConfig()

    # Create services using factory functions
    executor_result = create_executor(config)
    if executor_result.success:
        pass

    discoverer_result = create_discoverer(config)
    if discoverer_result.success:
        pass

    installer_result = create_installer_service(config)
    if installer_result.success:
        pass

    validation_result = create_validation_service(config)
    if validation_result.success:
        pass


def example_health_checks() -> None:
    """Example: Service health checks."""
    config = FlextMeltanoConfig()

    # Check health of all services
    services = [
        ("Executor", FlextMeltanoExecutor(config)),
        ("Discoverer", FlextMeltanoDiscoverer(config)),
        ("Installer", FlextMeltanoInstaller(config)),
        ("Validator", FlextMeltanoValidationService(config)),
    ]

    for _name, service in services:
        health_result = service.get_health_status()
        if health_result.success:
            pass


def example_plugin_discovery() -> None:
    """Example: Plugin discovery."""
    config = FlextMeltanoConfig()
    discoverer = FlextMeltanoDiscoverer(config)

    # Constants for plugin discovery
    MAX_PLUGINS_TO_SHOW = 5

    # Discover all plugins
    result = discoverer.discover_plugins()
    if result.success:
        plugins = result.data

        for _plugin in plugins[:MAX_PLUGINS_TO_SHOW]:  # Show first 5
            pass

        if len(plugins) > MAX_PLUGINS_TO_SHOW:
            pass

    # Discover extractors only
    extractors_result = discoverer.discover_plugins("extractors")
    if extractors_result.success:
        extractors = extractors_result.data
        for _extractor in extractors[:3]:  # Show first 3
            pass


def example_project_validation() -> None:
    """Example: Project validation."""
    config = FlextMeltanoConfig()
    validator = FlextMeltanoValidationService(config)

    # Validate project
    result = validator.validate_project()
    if result.success:
        validation_result = result.data

        if validation_result.issues:
            for _issue in validation_result.issues:
                pass

        if validation_result.warnings:
            for _warning in validation_result.warnings:
                pass


def example_legacy_compatibility() -> None:
    """Example: Legacy compatibility functions."""
    # Use legacy functions imported at module level

    # Use legacy plugin discovery (with deprecation warning)
    try:
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            flext_meltano_discover_plugins()
            if w:
                pass
    except (RuntimeError, ValueError, TypeError):
        pass


def example_singer_sdk_integration() -> None:
    """Example: Singer SDK integration."""
    # Use Singer SDK components imported at module level

    # Create a basic schema using Singer SDK types
    if singer_typing and Property and PropertiesList:
        PropertiesList(
            Property("id", singer_typing.StringType),
            Property("name", singer_typing.StringType),
            Property("created_at", singer_typing.DateTimeType),
            Property("active", singer_typing.BooleanType),
        )


def example_dbt_integration() -> None:
    """Example: DBT integration."""
    # Use DBT components imported at module level

    # Create DBT service configuration
    config = FlextMeltanoConfig(project_root=".")

    # Create DBT service
    dbt_result = create_meltano_dbt_service(config)
    if dbt_result.success:
        pass


def main() -> None:
    """Run all examples."""
    try:
        example_basic_configuration()
        example_service_creation()
        example_health_checks()
        example_plugin_discovery()
        example_project_validation()
        example_legacy_compatibility()
        example_singer_sdk_integration()
        example_dbt_integration()

    except (RuntimeError, ValueError, TypeError):
        traceback.print_exc()


if __name__ == "__main__":
    main()
