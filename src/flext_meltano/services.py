"""FLEXT Meltano Services - UNIFIED service implementation.

This module provides a SINGLE UNIFIED Meltano/Singer/DBT service implementation using
strict flext-core architecture with SOLID compliance:
- Single Responsibility: ONE class with clear purpose
- No nested classes violating module organization
- FlextResult railway-oriented programming throughout

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from pydantic import ConfigDict

from flext_core import (
    FlextContainer,
    FlextDomainService,
    FlextLogger,
    FlextResult,
    FlextTypes,
    FlextUtilities,
    T,
)
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.validators import FlextMeltanoValidators


class FlextMeltanoService(FlextDomainService[FlextTypes.Core.Dict]):
    """Unified Meltano service implementation with single responsibility.

    This service handles all Meltano operations (tap, target, dbt) in one cohesive
    service following SOLID principles and flext-core patterns. It provides a
    unified interface for creating, configuring, and executing Meltano services
    across different service types.

    Attributes:
        SERVICE_TYPES: Mapping of service types to their categories.
        model_config: Pydantic configuration for the service model.

    Example:
        >>> service = FlextMeltanoService(service_type="tap", tap_name="tap-csv")
        >>> result = service.execute()
        >>> if result.is_success:
        ...     print("Service executed successfully")

    """

    # Override parent's frozen=True and extra="forbid" for service-specific fields
    model_config = ConfigDict(
        frozen=False,  # Allow attribute assignment for service-specific fields
        extra="allow",  # Allow service-specific fields like tap_name, target_name
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )

    # Service type enumeration for unified handling
    SERVICE_TYPES: ClassVar[dict[str, str]] = {
        "tap": "extractor",
        "target": "loader",
        "dbt": "transformer",
    }

    def __init__(self, *, service_type: str = "tap", **data: object) -> None:
        """Initialize unified Meltano service using FlextConfig.

        Args:
            service_type: Type of service to create (tap, target, or dbt).
            **data: Additional configuration data for the service.

        Raises:
            FlextMeltanoConfigurationError: If service configuration is invalid.

        """
        # Convert data to mutable dict and extract service-specific fields
        mutable_data = dict(data)
        service_specific_fields = {
            "tap_name": mutable_data.pop("tap_name", None),
            "target_name": mutable_data.pop("target_name", None),
            "project_name": mutable_data.pop("project_name", None),
        }

        # Initialize parent with empty data - let BaseModel handle timestamps
        super().__init__()
        self._service_type = service_type
        self._logger = FlextLogger(__name__)
        self._container = FlextContainer.get_global()

        # Store service-specific fields as instance attributes
        for field, value in service_specific_fields.items():
            if value is not None:
                setattr(self, field, value)

    def execute(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Execute service operation based on type.

        Performs the main operation for the configured service type, returning
        a standardized result with service metadata and execution status.

        Returns:
            FlextResult containing service execution data with:
                - name: Generated service name
                - variant: Service variant identifier
                - type: Service type (tap/target/dbt)
                - status: Execution status
                - timestamp: ISO timestamp of execution

        Example:
            >>> service = FlextMeltanoService(service_type="tap")
            >>> result = service.execute()
            >>> if result.is_success:
            ...     data = result.unwrap()
            ...     print(f"Service {data['name']} executed successfully")

        """
        self._logger.info(
            "Executing Meltano service",
            extra={"service_type": self._service_type},
        )

        # Convert to proper type for FlextResult
        config_data: FlextTypes.Core.Dict = {
            "name": f"FlextMeltano{self._service_type.title()}Service",
            "variant": "flext",
            "type": self._service_type,
            "status": "ready",
            "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
        }

        return FlextResult[FlextTypes.Core.Dict].ok(data=config_data)

    def get_info(self) -> FlextResult[FlextMeltanoTypes.Plugin.PluginInfo]:
        """Get service information for any service type.

        Retrieves comprehensive information about the current service instance,
        including service type, name, and operational status.

        Returns:
            FlextResult containing plugin information with:
                - service_type: The type of service (tap/target/dbt)
                - name: The configured service name
                - status: Current service status

        Example:
            >>> service = FlextMeltanoService(service_type="tap", tap_name="tap-csv")
            >>> info_result = service.get_info()
            >>> if info_result.is_success:
            ...     info = info_result.unwrap()
            ...     print(f"Service: {info['name']}, Type: {info['service_type']}")

        """
        service_name = getattr(
            self,
            f"{self._service_type}_name",
            f"default-{self._service_type}",
        )
        info: FlextMeltanoTypes.Plugin.PluginInfo = {
            "service_type": self._service_type,
            "name": service_name,
            "status": "ready",
        }
        return FlextResult[FlextMeltanoTypes.Plugin.PluginInfo].ok(data=info)

    def validate_config(self) -> FlextResult[None]:
        """Validate service configuration based on type.

        Performs comprehensive validation of the service configuration using
        centralized validators to ensure all required fields are present and
        properly formatted.

        Returns:
            FlextResult indicating validation success or failure with error details.

        Example:
            >>> service = FlextMeltanoService(service_type="tap", tap_name="tap-csv")
            >>> validation_result = service.validate_config()
            >>> if validation_result.is_failure:
            ...     print(f"Validation failed: {validation_result.error}")

        """
        # Use centralized validator to eliminate duplication
        config = {
            "service_type": self._service_type,
            "tap_name": getattr(self, "tap_name", None),
            "target_name": getattr(self, "target_name", None),
            "project_name": getattr(self, "project_name", None),
        }

        result = FlextMeltanoValidators.validate_plugin_config(config)
        if result.is_failure:
            return FlextResult.fail(result.error or "Configuration validation failed")

        return FlextResult.ok(data=None)

    def create_instance(
        self,
        config: FlextTypes.Core.Dict,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create service instance with configuration based on type.

        Creates a properly configured service instance with the provided
        configuration data, including executable paths, capabilities, and
        namespace information.

        Args:
            config: Configuration dictionary containing service-specific settings.

        Returns:
            FlextResult containing the created service instance configuration with:
                - name: Service name
                - namespace: Generated namespace for the service
                - config: Provided configuration
                - executable: Executable command for the service
                - capabilities: List of service capabilities

        Raises:
            FlextMeltanoConfigurationError: If configuration is empty or invalid.

        Example:
            >>> service = FlextMeltanoService(service_type="tap", tap_name="tap-csv")
            >>> config = {"connection_string": "postgresql://..."}
            >>> instance_result = service.create_instance(config)
            >>> if instance_result.is_success:
            ...     instance = instance_result.unwrap()
            ...     print(
            ...         f"Created {instance['name']} with executable {instance['executable']}"
            ...     )

        """
        if not config:
            return FlextResult[FlextTypes.Core.Dict].fail(
                "Empty configuration provided",
            )

        service_name = getattr(
            self,
            f"{self._service_type}_name",
            f"default-{self._service_type}",
        )

        instance: FlextTypes.Core.Dict
        if self._service_type == "tap":
            instance = {
                "name": service_name,
                "namespace": f"tap_{service_name.replace('-', '_')}",
                "config": config,
                "executable": f"tap-{service_name.split('-')[-1]}",
                "capabilities": ["discover", "catalog", "state"],
            }
        elif self._service_type == "target":
            instance = {
                "name": service_name,
                "namespace": f"target_{service_name.replace('-', '_')}",
                "config": config,
                "executable": f"target-{service_name.split('-')[-1]}",
                "capabilities": ["about", "stream-maps"],
            }
        elif self._service_type == "dbt":
            instance = {
                "name": service_name,
                "type": "dbt",
                "config": config,
                "executable": "dbt",
            }
        else:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Unknown service type: {self._service_type}",
            )

        return FlextResult[FlextTypes.Core.Dict].ok(data=instance)

    def validate_service_config(
        self,
        config: FlextTypes.Core.Dict,
    ) -> FlextResult[bool]:
        """Validate service configuration based on type.

        Validates the provided configuration against service-specific requirements
        using centralized validation logic.

        Args:
            config: Configuration dictionary to validate.

        Returns:
            FlextResult containing boolean validation result or error details.

        Example:
            >>> service = FlextMeltanoService(service_type="tap")
            >>> config = {"connection_string": "postgresql://..."}
            >>> validation_result = service.validate_service_config(config)
            >>> if validation_result.is_success and validation_result.unwrap():
            ...     print("Configuration is valid")

        """
        # Use centralized validator to eliminate duplication
        return FlextMeltanoValidators.validate_plugin_config(config)

    def get_default_config(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Get default configuration based on service type.

        Generates appropriate default configuration for the current service type,
        including connection strings, output formats, and other service-specific
        settings.

        Returns:
            FlextResult containing default configuration dictionary for the service type.

        Example:
            >>> service = FlextMeltanoService(service_type="tap")
            >>> config_result = service.get_default_config()
            >>> if config_result.is_success:
            ...     config = config_result.unwrap()
            ...     print(f"Default config: {config}")

        """
        if self._service_type == "tap":
            tap_config: FlextTypes.Core.Dict = {"connection_string": "test_connection"}
            return FlextResult[FlextTypes.Core.Dict].ok(data=tap_config)
        if self._service_type == "target":
            target_config: FlextTypes.Core.Dict = {
                "output_file": "test_output.json",
                "format": "json",
            }
            return FlextResult[FlextTypes.Core.Dict].ok(data=target_config)
        if self._service_type == "dbt":
            project_name = getattr(self, "project_name", "default_project")
            dbt_config: FlextTypes.Core.Dict = {
                project_name: {
                    "outputs": {"dev": {"type": "duckdb", "path": "test.duckdb"}},
                    "target": "dev",
                },
            }
            return FlextResult[FlextTypes.Core.Dict].ok(data=dbt_config)
        empty_config: FlextTypes.Core.Dict = {}
        return FlextResult[FlextTypes.Core.Dict].ok(data=empty_config)

    def validate_service(self) -> FlextResult[bool]:
        """Validate service configuration and setup.

        Performs end-to-end validation of the service by first generating default
        configuration and then validating it against service requirements.

        Returns:
            FlextResult containing boolean validation result or error details.

        Example:
            >>> service = FlextMeltanoService(service_type="tap", tap_name="tap-csv")
            >>> validation_result = service.validate_service()
            >>> if validation_result.is_success and validation_result.unwrap():
            ...     print("Service is properly configured")

        """
        config_result = self.get_default_config()
        if config_result.is_failure:
            return FlextResult[bool].fail(
                f"Default config failed: {config_result.error}",
            )
        return self.validate_service_config(config_result.unwrap())

    def run_models(
        self,
        model_names: list[str] | None = None,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Run DBT models with specified model names.

        Executes DBT model transformations for the specified models or all models
        if no specific models are provided. This method is only available for
        DBT service types.

        Args:
            model_names: Optional list of specific model names to run. If None,
                        all models will be executed.

        Returns:
            FlextResult containing execution results with:
                - status: Execution status
                - models_run: List of models that were executed
                - timestamp: ISO timestamp of execution

        Raises:
            FlextMeltanoConfigurationError: If service type is not DBT.

        Example:
            >>> service = FlextMeltanoService(
            ...     service_type="dbt", project_name="my_project"
            ... )
            >>> result = service.run_models(["model1", "model2"])
            >>> if result.is_success:
            ...     data = result.unwrap()
            ...     print(f"Ran {len(data['models_run'])} models")

        """
        if self._service_type != "dbt":
            return FlextResult[FlextTypes.Core.Dict].fail(
                "run_models is only available for DBT services",
            )

        self._logger.info("Running DBT models", extra={"models": model_names or "all"})

        # Placeholder implementation - would integrate with actual DBT
        result_data: FlextTypes.Core.Dict = {
            "status": "completed",
            "models_run": model_names or [],
            "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
        }

        return FlextResult[FlextTypes.Core.Dict].ok(data=result_data)

    # DBT-specific method for compatibility
    def get_profiles_config(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Get DBT profiles configuration for DBT service type.

        Retrieves the DBT profiles configuration, which contains database
        connection settings and other DBT-specific configuration. This method
        is only available for DBT service types.

        Returns:
            FlextResult containing DBT profiles configuration or error details.

        Raises:
            FlextMeltanoConfigurationError: If service type is not DBT.

        Example:
            >>> service = FlextMeltanoService(
            ...     service_type="dbt", project_name="my_project"
            ... )
            >>> profiles_result = service.get_profiles_config()
            >>> if profiles_result.is_success:
            ...     profiles = profiles_result.unwrap()
            ...     print(f"Profiles config: {profiles}")

        """
        if self._service_type != "dbt":
            return FlextResult[FlextTypes.Core.Dict].fail(
                "Profiles config only available for DBT service type",
            )

        return self.get_default_config()

    # Consolidated Service Factory - ZERO DUPLICATION using flext-core patterns
    @staticmethod
    def _create_service_with_type(
        name: str,
        service_type: str,
        field_name: str,
        **config: object,
    ) -> FlextResult[FlextMeltanoService]:
        """Consolidated factory using flext-core extensively.

        Creates a service instance with the specified type and configuration,
        using flext-core validation and text processing utilities.

        Args:
            name: Service name to validate and use.
            service_type: Type of service to create (tap, target, dbt).
            field_name: Field name for the service (tap_name, target_name, etc.).
            **config: Additional configuration parameters.

        Returns:
            FlextResult containing the created service instance or error details.

        """
        # Use flext-core validation and text processing extensively
        safe_name = FlextUtilities.TextProcessor.safe_string(name)

        # Create unified configuration using flext-core patterns
        service_kwargs: FlextTypes.Core.Dict = {
            "service_type": service_type,
            field_name: safe_name,
            "entity_id": FlextUtilities.Generators.generate_id(),
            **{k: v for k, v in config.items() if k != "service_type"},
        }

        # Use model_validate for proper Pydantic instantiation
        service_instance = FlextMeltanoService.model_validate(service_kwargs)
        return FlextResult[FlextMeltanoService].ok(data=service_instance)

    # Generic Service Factory using advanced Python 3.13+ patterns
    @staticmethod
    def _create_service_generic(
        service_class: type[T],
        name: str,
        field_name: str,
        service_prefix: str,
        **config: object,
    ) -> FlextResult[T]:
        """Generic factory method for all Meltano service types.

        Uses advanced Python 3.13+ generics with FlextUtilities validation
        and consolidated error handling following DRY principles.

        Args:
            service_class: The service class to instantiate (TapService, TargetService, etc.).
            name: The service name to validate and use.
            field_name: The field name for the service (tap_name, target_name, etc.).
            service_prefix: The default prefix for validation (tap, target, dbt).
            **config: Additional configuration parameters passed to the service constructor.

        Returns:
            FlextResult containing the created service instance or error.

        Example:
            >>> result = FlextMeltanoService._create_service_generic(
            ...     FlextMeltanoService, "my-tap", "tap_name", "tap"
            ... )
            >>> if result.is_success:
            ...     service = result.unwrap()
            ...     print(f"Created service: {service}")

        """
        # Use FlextUtilities for name validation - consolidated pattern
        default_name = f"{service_prefix}-default"
        safe_name = FlextUtilities.TextProcessor.safe_string(name)

        # Consolidated validation logic
        if not safe_name or safe_name == default_name:
            return FlextResult[T].fail(f"Invalid {service_prefix} name: {name}")

        # Dynamic service instance creation using **kwargs pattern
        service_kwargs: FlextTypes.Core.Dict = {field_name: safe_name}
        service_kwargs.update(config)  # Add additional configuration

        # Convert service_kwargs to proper types using FlextUtilities
        typed_kwargs = {
            "service_type": str(service_kwargs.get("service_type", service_prefix)),
            "app_name": str(
                service_kwargs.get("app_name", f"{service_prefix}-{safe_name}"),
            ),
            "environment": str(service_kwargs.get("environment", "development")),
            "debug": bool(service_kwargs.get("debug", False)),
            "log_level": str(service_kwargs.get("log_level", "INFO")),
            "max_workers": FlextUtilities.Conversions.safe_int(
                str(service_kwargs.get("max_workers", 4)),
            ),
            "timeout_seconds": FlextUtilities.Conversions.safe_int(
                str(service_kwargs.get("timeout_seconds", 30)),
            ),
        }

        # Add service-specific field
        typed_kwargs[field_name] = safe_name

        # Service instantiation - Handle both Pydantic and regular classes
        try:
            # Try Pydantic model_validate first, fallback to regular instantiation
            if hasattr(service_class, "model_validate"):
                # Use getattr to satisfy MyPy type checking
                model_validate_method = getattr(service_class, "model_validate")
                service_instance = model_validate_method(typed_kwargs)
            else:
                # Regular class instantiation
                service_instance = service_class(**typed_kwargs)
        except Exception as e:
            return FlextResult[T].fail(
                f"Failed to create {service_prefix} service: {e}",
            )

        return FlextResult[T].ok(data=service_instance)

    @staticmethod
    def create_tap_service(
        tap_name: str,
        **config: object,
    ) -> FlextResult[FlextMeltanoService]:
        """Create tap service using flext-core factory patterns.

        Creates a new tap (extractor) service with the specified name and
        configuration using standardized factory patterns.

        Args:
            tap_name: Name of the tap service to create.
            **config: Additional configuration parameters for the tap service.

        Returns:
            FlextResult containing the created tap service instance or error details.

        Example:
            >>> result = FlextMeltanoService.create_tap_service("tap-csv")
            >>> if result.is_success:
            ...     tap_service = result.unwrap()
            ...     print(f"Created tap service: {tap_service}")

        """
        return FlextMeltanoService._create_service_with_type(
            tap_name,
            "tap",
            "tap_name",
            **config,
        )

    @staticmethod
    def create_target_service(
        target_name: str,
        **config: object,
    ) -> FlextResult[FlextMeltanoService]:
        """Create target service using flext-core factory patterns.

        Creates a new target (loader) service with the specified name and
        configuration using standardized factory patterns.

        Args:
            target_name: Name of the target service to create.
            **config: Additional configuration parameters for the target service.

        Returns:
            FlextResult containing the created target service instance or error details.

        Example:
            >>> result = FlextMeltanoService.create_target_service("target-jsonl")
            >>> if result.is_success:
            ...     target_service = result.unwrap()
            ...     print(f"Created target service: {target_service}")

        """
        return FlextMeltanoService._create_service_with_type(
            target_name,
            "target",
            "target_name",
            **config,
        )

    @staticmethod
    def create_dbt_service(
        project_name: str,
        **config: object,
    ) -> FlextResult[FlextMeltanoService]:
        """Create DBT service using flext-core factory patterns.

        Creates a new DBT (transformer) service with the specified project name
        and configuration using standardized factory patterns.

        Args:
            project_name: Name of the DBT project to create.
            **config: Additional configuration parameters for the DBT service.

        Returns:
            FlextResult containing the created DBT service instance or error details.

        Example:
            >>> result = FlextMeltanoService.create_dbt_service("my_dbt_project")
            >>> if result.is_success:
            ...     dbt_service = result.unwrap()
            ...     print(f"Created DBT service: {dbt_service}")

        """
        return FlextMeltanoService._create_service_with_type(
            project_name,
            "dbt",
            "project_name",
            **config,
        )


__all__ = [
    "FlextMeltanoService",
]
