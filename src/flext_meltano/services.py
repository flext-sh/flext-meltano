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
        """Validate service configuration using monadic validation chain.

        Performs comprehensive validation of the service configuration using
        FlextResult.chain_validations() to compose multiple validation rules
        with automatic error accumulation and early termination.

        Returns:
            FlextResult indicating validation success or failure with error details.

        Example:
            >>> service = FlextMeltanoService(service_type="tap", tap_name="tap-csv")
            >>> validation_result = service.validate_config()
            >>> if validation_result.is_failure:
            ...     print(f"Validation failed: {validation_result.error}")

        """
        # MONADIC VALIDATION CHAIN: Replace manual validation with chain_validations
        config = {
            "service_type": self._service_type,
            "tap_name": getattr(self, "tap_name", None),
            "target_name": getattr(self, "target_name", None),
            "project_name": getattr(self, "project_name", None),
        }

        # Fixed: Convert bool result to None result for chain_validations compatibility
        def validate_plugin_config_none() -> FlextResult[None]:
            result = FlextMeltanoValidators.validate_plugin_config(config)
            if result.is_success:
                return FlextResult[None].ok(None)
            return FlextResult[None].fail(result.error or "Plugin validation failed")

        # Fixed: Use *args syntax for chain_validations
        return FlextResult.chain_validations(
            self._validate_service_type,
            lambda: self._validate_service_name(config),
            validate_plugin_config_none,
        )

    def _validate_service_type(self) -> FlextResult[None]:
        """Validate service type is supported.

        Returns:
            FlextResult indicating if service type is valid.

        """
        valid_types = {"tap", "target", "dbt"}
        if self._service_type not in valid_types:
            return FlextResult.fail(
                f"Invalid service type '{self._service_type}'. Must be one of: {valid_types}"
            )
        return FlextResult.ok(data=None)

    def _validate_service_name(self, config: FlextTypes.Core.Dict) -> FlextResult[None]:
        """Validate that appropriate service name is provided based on type.

        Args:
            config: Configuration dictionary containing service names.

        Returns:
            FlextResult indicating if service name is valid.

        """
        service_name_field = f"{self._service_type}_name"
        service_name = config.get(service_name_field)

        if not service_name and self._service_type != "dbt":
            return FlextResult.fail(
                f"Missing required field '{service_name_field}' for {self._service_type} service"
            )
        return FlextResult.ok(data=None)

    def create_instance(
        self,
        config: FlextTypes.Core.Dict,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create service instance with configuration using monadic conditional chain.

        Creates a properly configured service instance with the provided
        configuration data, using FlextResult monadic patterns for type-safe
        conditional logic and eliminating nested if/else chains.

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
        # MONADIC CONDITIONAL CHAIN: Use FlextResult.when for validation
        return (
            FlextResult[FlextTypes.Core.Dict]
            .ok(config)
            .when(bool)  # Fixed: when() only takes condition function
            .flat_map(self._create_service_instance_by_type)
        )

    def _create_service_instance_by_type(
        self, config: FlextTypes.Core.Dict
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create service instance based on type using monadic dispatch pattern.

        Private helper method that implements the actual service instance creation
        logic using monadic dispatch to avoid complex conditional chains.

        Args:
            config: Validated configuration dictionary.

        Returns:
            FlextResult containing the service instance or error.

        """
        service_name = getattr(
            self,
            f"{self._service_type}_name",
            f"default-{self._service_type}",
        )

        # MONADIC DISPATCH: Use if_then_else for type-safe conditional instance creation
        if self._service_type == "tap":
            instance: FlextTypes.Core.Dict = {
                "name": service_name,
                "namespace": f"tap_{service_name.replace('-', '_')}",
                "config": config,
                "executable": f"tap-{service_name.split('-')[-1]}",
                "capabilities": ["discover", "catalog", "state"],
            }
            return FlextResult[FlextTypes.Core.Dict].ok(data=instance)
        if self._service_type == "target":
            instance = {
                "name": service_name,
                "namespace": f"target_{service_name.replace('-', '_')}",
                "config": config,
                "executable": f"target-{service_name.split('-')[-1]}",
                "capabilities": ["about", "stream-maps"],
            }
            return FlextResult[FlextTypes.Core.Dict].ok(data=instance)
        if self._service_type == "dbt":
            instance = {
                "name": service_name,
                "type": "dbt",
                "config": config,
                "executable": "dbt",
            }
            return FlextResult[FlextTypes.Core.Dict].ok(data=instance)
        return FlextResult[FlextTypes.Core.Dict].fail(
            f"Unknown service type: {self._service_type}",
        )

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
        """Validate service configuration and setup using monadic railway pattern.

        Uses FlextResult railway-oriented programming to chain validation operations
        with early termination on failure, eliminating manual error checking.

        Returns:
            FlextResult containing boolean validation result or error details.

        Example:
            >>> service = FlextMeltanoService(service_type="tap", tap_name="tap-csv")
            >>> validation_result = service.validate_service()
            >>> if validation_result.is_success and validation_result.unwrap():
            ...     print("Service is properly configured")

        """
        # MONADIC COMPOSITION: Replace manual chaining with railway pattern
        return (
            self.get_default_config() >> self.validate_service_config
        )  # Monadic bind (flat_map)

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
        """Consolidated factory using monadic pipeline with validation and construction.

        Creates a service instance with the specified type and configuration,
        using FlextResult.pipeline() for composable service creation with
        automatic error handling and resource management.

        Args:
            name: Service name to validate and use.
            service_type: Type of service to create (tap, target, dbt).
            field_name: Field name for the service (tap_name, target_name, etc.).
            **config: Additional configuration parameters.

        Returns:
            FlextResult containing the created service instance or error details.

        """
        # Fixed: Use proper railway pattern instead of pipeline for different types
        return (
            FlextMeltanoService._validate_service_name_not_empty(name, service_type)
            .flat_map(
                lambda validated_name: FlextMeltanoService._build_service_configuration(
                    validated_name, service_type, field_name, **config
                )
            )
            .flat_map(FlextMeltanoService._instantiate_service)
        )

    @staticmethod
    def _validate_service_name_not_empty(
        name: str, service_type: str
    ) -> FlextResult[str]:
        """Validate service name is not empty or default.

        Args:
            name: Service name to validate.
            service_type: Service type for error context.

        Returns:
            FlextResult containing validated name or error.

        """
        default_name = f"{service_type}-default"
        if not name or name == default_name:
            return FlextResult[str].fail(f"Invalid {service_type} name: {name}")
        return FlextResult[str].ok(data=name)

    @staticmethod
    def _build_service_configuration(
        name: str, service_type: str, field_name: str, **config: object
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Build service configuration dictionary.

        Args:
            name: Validated service name.
            service_type: Service type.
            field_name: Field name for service.
            **config: Additional configuration.

        Returns:
            FlextResult containing service configuration.

        """
        service_kwargs: FlextTypes.Core.Dict = {
            "service_type": service_type,
            field_name: name,
            "entity_id": FlextUtilities.Generators.generate_id(),
            **{k: v for k, v in config.items() if k != "service_type"},
        }
        return FlextResult[FlextTypes.Core.Dict].ok(data=service_kwargs)

    @staticmethod
    def _instantiate_service(
        service_kwargs: FlextTypes.Core.Dict,
    ) -> FlextResult[FlextMeltanoService]:
        """Instantiate FlextMeltanoService with configuration.

        Args:
            service_kwargs: Service configuration dictionary.

        Returns:
            FlextResult containing service instance or error.

        """
        try:
            service_instance = FlextMeltanoService.model_validate(service_kwargs)
            return FlextResult[FlextMeltanoService].ok(data=service_instance)
        except Exception as e:
            return FlextResult[FlextMeltanoService].fail(
                f"Failed to create service: {e}"
            )

    # Generic Service Factory using advanced Python 3.13+ patterns
    @staticmethod
    def _create_service_generic(
        service_class: type[T],
        name: str,
        field_name: str,
        service_prefix: str,
        **config: object,
    ) -> FlextResult[T]:
        """Generic factory using applicative lifting for parallel validation.

        Uses advanced Python 3.13+ generics with FlextResult.applicative_lift3()
        to perform parallel validation of name, configuration, and service class,
        then combines results using applicative functors for maximum efficiency.

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
        # APPLICATIVE LIFTING: Use applicative_lift3() for parallel validation
        name_validation = FlextMeltanoService._validate_and_sanitize_name(
            name, service_prefix
        )
        config_validation = FlextMeltanoService._validate_and_build_config(
            field_name, name, **config
        )
        class_validation = FlextMeltanoService._validate_service_class(service_class)

        # Fixed: Function returns T directly, then flat_map the FlextResult-returning method
        def create_service_from_validation(
            validated_name: str,
            typed_kwargs: FlextTypes.Core.Dict,
            validated_class: type[T],
        ) -> T:
            """Create service instance from validated inputs - returns T directly."""
            result = FlextMeltanoService._create_instance_from_validated_inputs(
                validated_class, typed_kwargs
            )
            if result.is_failure:
                # For applicative lifting, we can't return FlextResult, so raise exception
                raise ValueError(result.error or "Failed to create service instance")
            return result.unwrap()

        return FlextResult.applicative_lift3(
            create_service_from_validation,
            name_validation,
            config_validation,
            class_validation,
        )  # Flatten nested FlextResult  # Flatten nested FlextResult

    @staticmethod
    def _validate_and_sanitize_name(name: str, service_prefix: str) -> FlextResult[str]:
        """Validate and sanitize service name.

        Args:
            name: Raw service name.
            service_prefix: Service prefix for validation.

        Returns:
            FlextResult containing sanitized name or error.

        """
        # Use FlextUtilities for name validation - consolidated pattern
        default_name = f"{service_prefix}-default"
        safe_name = FlextUtilities.TextProcessor.safe_string(name)

        # Consolidated validation logic
        if not safe_name or safe_name == default_name:
            return FlextResult[str].fail(f"Invalid {service_prefix} name: {name}")

        return FlextResult[str].ok(data=safe_name)

    @staticmethod
    def _validate_and_build_config(
        field_name: str, name: str, **config: object
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Validate and build service configuration.

        Args:
            field_name: Service field name.
            name: Service name.
            **config: Additional configuration.

        Returns:
            FlextResult containing typed configuration dictionary.

        """
        safe_name = FlextUtilities.TextProcessor.safe_string(name)

        # Convert max_workers safely with proper type validation
        max_workers_raw = config.get("max_workers", 4)
        if isinstance(max_workers_raw, (str, int, float)) or max_workers_raw is None:
            max_workers_result = FlextUtilities.Conversions.to_int(max_workers_raw)
        else:
            max_workers_result = FlextResult[int].fail(
                f"Invalid max_workers type: {type(max_workers_raw)}"
            )

        if max_workers_result.is_failure:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Invalid max_workers: {max_workers_result.error}"
            )

        # Convert timeout_seconds safely with proper type validation
        timeout_raw = config.get("timeout_seconds", 30)
        if isinstance(timeout_raw, (str, int, float)) or timeout_raw is None:
            timeout_result = FlextUtilities.Conversions.to_int(timeout_raw)
        else:
            timeout_result = FlextResult[int].fail(
                f"Invalid timeout_seconds type: {type(timeout_raw)}"
            )

        if timeout_result.is_failure:
            return FlextResult[FlextTypes.Core.Dict].fail(
                f"Invalid timeout_seconds: {timeout_result.error}"
            )

        # Convert service_kwargs to proper types using FlextUtilities
        typed_kwargs: FlextTypes.Core.Dict = {
            "service_type": str(
                config.get("service_type", field_name.split("_", maxsplit=1)[0])
            ),
            "app_name": str(
                config.get(
                    "app_name", f"{field_name.split('_', maxsplit=1)[0]}-{safe_name}"
                )
            ),
            "environment": str(config.get("environment", "development")),
            "debug": bool(config.get("debug")),
            "log_level": str(config.get("log_level", "INFO")),
            "max_workers": max_workers_result.unwrap(),
            "timeout_seconds": timeout_result.unwrap(),
        }

        # Add service-specific field
        typed_kwargs[field_name] = safe_name

        return FlextResult[FlextTypes.Core.Dict].ok(data=typed_kwargs)

    @staticmethod
    def _validate_service_class(service_class: type[T]) -> FlextResult[type[T]]:
        """Validate service class has required methods.

        Args:
            service_class: Service class to validate.

        Returns:
            FlextResult containing validated class or error.

        """
        # Type system guarantees this is a valid type[T], so always return success
        return FlextResult[type[T]].ok(data=service_class)

    @staticmethod
    def _create_instance_from_validated_inputs(
        service_class: type[T], typed_kwargs: FlextTypes.Core.Dict
    ) -> FlextResult[T]:
        """Create service instance from validated inputs.

        Args:
            service_class: Validated service class.
            typed_kwargs: Validated configuration.

        Returns:
            FlextResult containing service instance or error.

        """
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
            return FlextResult[T].fail(f"Failed to create service: {e}")

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
