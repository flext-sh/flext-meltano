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
    """UNIFIED Meltano service implementation - SINGLE RESPONSIBILITY.

    Handles ALL Meltano operations (tap, target, dbt) in one cohesive service
    following SOLID principles and flext-core patterns.
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
        """Initialize unified Meltano service using FlextConfig."""
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
        """Execute service operation based on type - UNIFIED IMPLEMENTATION."""
        self._logger.info(
            "Executing Meltano service", extra={"service_type": self._service_type}
        )

        # Convert to proper type for FlextResult
        config_data: FlextTypes.Core.Dict = {
            "name": f"FlextMeltano{self._service_type.title()}Service",
            "variant": "flext",
            "type": self._service_type,
            "status": "ready",
            "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
        }

        return FlextResult[FlextTypes.Core.Dict].ok(config_data)

    def get_info(self) -> FlextResult[FlextMeltanoTypes.Plugin.PluginInfo]:
        """Get service information for any service type."""
        service_name = getattr(
            self, f"{self._service_type}_name", f"default-{self._service_type}"
        )
        info: FlextMeltanoTypes.Plugin.PluginInfo = {
            "service_type": self._service_type,
            "name": service_name,
            "status": "ready",
        }
        return FlextResult[FlextMeltanoTypes.Plugin.PluginInfo].ok(info)

    def validate_config(self) -> FlextResult[None]:
        """Validate service configuration based on type."""
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

        return FlextResult.ok(None)

    def create_instance(
        self, config: FlextTypes.Core.Dict
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create service instance with configuration based on type."""
        if not config:
            return FlextResult[FlextTypes.Core.Dict].fail(
                "Empty configuration provided"
            )

        service_name = getattr(
            self, f"{self._service_type}_name", f"default-{self._service_type}"
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
                f"Unknown service type: {self._service_type}"
            )

        return FlextResult[FlextTypes.Core.Dict].ok(instance)

    def validate_service_config(
        self, config: FlextTypes.Core.Dict
    ) -> FlextResult[bool]:
        """Validate service configuration based on type."""
        # Use centralized validator to eliminate duplication

        return FlextMeltanoValidators.validate_plugin_config(config)

    def get_default_config(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Get default configuration based on service type."""
        if self._service_type == "tap":
            tap_config: FlextTypes.Core.Dict = {"connection_string": "test_connection"}
            return FlextResult[FlextTypes.Core.Dict].ok(tap_config)
        if self._service_type == "target":
            target_config: FlextTypes.Core.Dict = {
                "output_file": "test_output.json",
                "format": "json",
            }
            return FlextResult[FlextTypes.Core.Dict].ok(target_config)
        if self._service_type == "dbt":
            project_name = getattr(self, "project_name", "default_project")
            dbt_config: FlextTypes.Core.Dict = {
                project_name: {
                    "outputs": {"dev": {"type": "duckdb", "path": "test.duckdb"}},
                    "target": "dev",
                }
            }
            return FlextResult[FlextTypes.Core.Dict].ok(dbt_config)
        empty_config: FlextTypes.Core.Dict = {}
        return FlextResult[FlextTypes.Core.Dict].ok(empty_config)

    def validate_service(self) -> FlextResult[bool]:
        """Validate service configuration and setup."""
        config_result = self.get_default_config()
        if config_result.is_failure:
            return FlextResult[bool].fail(
                f"Default config failed: {config_result.error}"
            )
        return self.validate_service_config(config_result.unwrap())

    def run_models(
        self, model_names: list[str] | None = None
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Run DBT models - placeholder implementation."""
        if self._service_type != "dbt":
            return FlextResult[FlextTypes.Core.Dict].fail(
                "run_models is only available for DBT services"
            )

        self._logger.info("Running DBT models", extra={"models": model_names or "all"})

        # Placeholder implementation - would integrate with actual DBT
        result_data: FlextTypes.Core.Dict = {
            "status": "completed",
            "models_run": model_names or [],
            "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
        }

        return FlextResult[FlextTypes.Core.Dict].ok(result_data)

    # DBT-specific method for compatibility
    def get_profiles_config(self) -> FlextResult[FlextTypes.Core.Dict]:
        """Get DBT profiles configuration (only for DBT service type)."""
        if self._service_type != "dbt":
            return FlextResult[FlextTypes.Core.Dict].fail(
                "Profiles config only available for DBT service type"
            )

        return self.get_default_config()

    # Consolidated Service Factory - ZERO DUPLICATION using flext-core patterns
    @staticmethod
    def _create_service_with_type(
        name: str, service_type: str, field_name: str, **config: object
    ) -> FlextResult[FlextMeltanoService]:
        """Consolidated factory using flext-core extensively - ELIMINATES 150+ lines duplication."""
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
        return FlextResult[FlextMeltanoService].ok(service_instance)

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
            service_class: The service class to instantiate (TapService, TargetService, etc.)
            name: The service name to validate and use
            field_name: The field name for the service (tap_name, target_name, etc.)
            service_prefix: The default prefix for validation (tap, target, dbt)
            **config: Additional configuration parameters passed to the service constructor

        Returns:
            FlextResult containing the created service instance or error

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
                service_kwargs.get("app_name", f"{service_prefix}-{safe_name}")
            ),
            "environment": str(service_kwargs.get("environment", "development")),
            "debug": bool(service_kwargs.get("debug", False)),
            "log_level": str(service_kwargs.get("log_level", "INFO")),
            "max_workers": FlextUtilities.Conversions.safe_int(
                str(service_kwargs.get("max_workers", 4))
            ),
            "timeout_seconds": FlextUtilities.Conversions.safe_int(
                str(service_kwargs.get("timeout_seconds", 30))
            ),
        }

        # Add service-specific field
        typed_kwargs[field_name] = safe_name

        # Service instantiation - Handle both Pydantic and regular classes
        try:
            # Try Pydantic model_validate first, fallback to regular instantiation
            if hasattr(service_class, "model_validate"):
                # Pydantic model - use getattr for type safety
                model_validate = getattr(service_class, "model_validate")
                service_instance = model_validate(typed_kwargs)
            else:
                # Regular class instantiation
                service_instance = service_class(**typed_kwargs)
        except Exception as e:
            return FlextResult[T].fail(
                f"Failed to create {service_prefix} service: {e}"
            )

        return FlextResult[T].ok(service_instance)

    @staticmethod
    def create_tap_service(
        tap_name: str, **config: object
    ) -> FlextResult[FlextMeltanoService]:
        """Create tap service using flext-core factory patterns - ZERO DUPLICATION."""
        return FlextMeltanoService._create_service_with_type(
            tap_name, "tap", "tap_name", **config
        )

    @staticmethod
    def create_target_service(
        target_name: str, **config: object
    ) -> FlextResult[FlextMeltanoService]:
        """Create target service using flext-core factory patterns - ZERO DUPLICATION."""
        return FlextMeltanoService._create_service_with_type(
            target_name, "target", "target_name", **config
        )

    @staticmethod
    def create_dbt_service(
        project_name: str, **config: object
    ) -> FlextResult[FlextMeltanoService]:
        """Create DBT service using flext-core factory patterns - ZERO DUPLICATION."""
        return FlextMeltanoService._create_service_with_type(
            project_name, "dbt", "project_name", **config
        )



__all__ = [
    "FlextMeltanoService",
]
