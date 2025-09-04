"""FLEXT Meltano Services - Unified service implementations following flext-core patterns.

This module provides Meltano/Singer/DBT service implementations using strict flext-core
architecture with nested service classes, Pydantic BaseConfig inheritance,
and FlextResult railway-oriented programming.

Architecture:
    - Unified FlextMeltanoService class following FlextServices pattern
    - Nested service classes inherit from FlextDomainService[ConfigDict]
    - No legacy protocols or backwards compatibility
    - Strict Pydantic validation with Python 3.13+ features
    - FlextResult[T] for all operations

Classes:
    FlextMeltanoService: Unified service class with nested implementations
        .TapService: Singer tap service implementation
        .TargetService: Singer target service implementation
        .DbtService: DBT service implementation

Usage:
    >>> service = FlextMeltanoService.TapService(tap_name="test-tap")
    >>> result = service.execute()
    >>> if result.success:
    ...     print(result.value)
"""

from __future__ import annotations

from typing import TypeVar

from flext_core import (
    FlextDomainService,
    FlextLogger,
    FlextResult,
    FlextUtilities,
    get_flext_container,
)

from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.typings import FlextMeltanoTypes

# Generic type variable for service factory methods
T_Service = TypeVar("T_Service", bound=FlextDomainService)

# Constants to avoid boolean positional arguments

# =============================================================================
# MAIN SERVICES CLASS - Following FlextServices pattern
# =============================================================================


class FlextMeltanoService:
    """Unified service class following flext-core FlextServices pattern.

    Provides Meltano/Singer/DBT service implementations using strict flext-core
    architecture with nested service classes, Pydantic BaseConfig inheritance,
    and FlextResult railway-oriented programming.

    Architecture:
        - Nested service classes inherit from FlextDomainService[ConfigDict]
        - No legacy protocols or backwards compatibility
        - Strict Pydantic validation with Python 3.13+ features
        - FlextResult[T] for all operations
    """

    def __init__(self) -> None:
        """Initialize FlextMeltanoService with FlextContainer dependency injection."""
        self._container = get_flext_container()

        # Register service types in container for dependency injection
        self._container.register("tap_service_class", self.TapService)
        self._container.register("target_service_class", self.TargetService)
        self._container.register("dbt_service_class", self.DbtService)

    class TapService(FlextDomainService[FlextMeltanoTypes.Plugin.Config]):
        """Tap service implementation using strict flext-core patterns.

        Pydantic model with frozen configuration, following FlextDomainService
        inheritance with proper field declarations and validation.
        """

        # Pydantic fields using local types directly
        tap_name: FlextMeltanoTypes.Plugin.Name

        def __init__(self, /, **data: object) -> None:
            """Initialize with Pydantic **data pattern (frozen model)."""
            # Pass data directly to Pydantic - it handles type conversion
            super().__init__(**data)  # type: ignore[arg-type]  # Pydantic handles object->field type conversion

        @property
        def adapter(self) -> object:
            """Get unified Meltano adapter for all operations."""
            return FlextMeltanoAdapter()

        def execute(self) -> FlextResult[FlextMeltanoTypes.Plugin.Config]:
            """Execute tap service operation (required by FlextDomainService)."""
            logger = FlextLogger(__name__)
            logger.info("Executing tap service", tap_name=self.tap_name)

            return FlextResult.ok({
                "service": "FlextMeltanoTapService",
                "tap_name": self.tap_name,
                "status": "ready",
            })

        def validate_config(self) -> FlextResult[None]:
            """Validate tap configuration using local types."""
            # Use local validation patterns
            if not self.tap_name:
                return FlextResult.fail("Empty tap_name configuration")

            return FlextResult.ok(None)

        def get_info(self) -> FlextResult[FlextMeltanoTypes.Plugin.PluginInfo]:
            """Get service information."""
            return FlextResult.ok({
                "service_type": "tap",
                "name": self.tap_name,
                "status": "ready",
            })

        def create_tap_instance(self, config: dict[str, object]) -> FlextResult[object]:
            """Create tap instance with configuration."""
            if not config:
                return FlextResult.fail("Empty configuration provided")

            try:
                # This is a placeholder implementation
                # In real usage, this would create actual Singer Tap instances
                return FlextResult.ok({"tap": self.tap_name, "config": config})
            except Exception as e:
                return FlextResult.fail(f"Failed to create tap instance: {e}")

        def validate_tap_config(self, config: dict[str, object]) -> FlextResult[bool]:
            """Validate tap configuration."""
            if not config:
                return FlextResult.fail("Empty configuration provided")

            return FlextResult.ok(data=True)

        def get_default_config(self) -> FlextResult[dict[str, object]]:
            """Get default configuration for tap."""
            return FlextResult.ok({"connection_string": "test_connection"})

        def validate_service(self) -> FlextResult[bool]:
            """Validate tap service configuration and setup (renamed to avoid Pydantic conflict)."""
            try:
                # Basic validation - check if tap has valid configuration
                config_result = self.get_default_config()
                if config_result.failure:
                    return FlextResult.fail(
                        f"Default config failed: {config_result.error}"
                    )
                return self.validate_tap_config(config_result.value)
            except Exception as e:
                return FlextResult.fail(f"Tap service validation failed: {e}")

    class TargetService(FlextDomainService[FlextMeltanoTypes.Plugin.Config]):
        """Target service implementation using strict flext-core patterns."""

        target_name: FlextMeltanoTypes.Plugin.Name

        def __init__(self, /, **data: object) -> None:
            """Initialize with Pydantic **data pattern (frozen model)."""
            # Pass data directly to Pydantic - it handles type conversion
            super().__init__(**data)  # type: ignore[arg-type]  # Pydantic handles object->field type conversion

        @property
        def adapter(self) -> object:
            """Get unified Meltano adapter for all operations."""
            return FlextMeltanoAdapter()

        def execute(self) -> FlextResult[FlextMeltanoTypes.Plugin.Config]:
            """Execute target service operation (required by FlextDomainService)."""
            logger = FlextLogger(__name__)
            logger.info("Executing target service", target_name=self.target_name)

            return FlextResult.ok({
                "service": "FlextMeltanoTargetService",
                "target_name": self.target_name,
                "status": "ready",
            })

        def get_info(self) -> FlextResult[FlextMeltanoTypes.Plugin.PluginInfo]:
            """Get service information."""
            return FlextResult.ok({
                "service_type": "target",
                "name": self.target_name,
                "status": "ready",
            })

        def create_target_instance(
            self, config: dict[str, object]
        ) -> FlextResult[object]:
            """Create target instance with configuration."""
            if not config:
                return FlextResult.fail("Empty configuration provided")

            try:
                # This is a placeholder implementation
                # In real usage, this would create actual Singer Target instances
                return FlextResult.ok({"target": self.target_name, "config": config})
            except Exception as e:
                return FlextResult.fail(f"Failed to create target instance: {e}")

        def validate_target_config(
            self, config: dict[str, object]
        ) -> FlextResult[bool]:
            """Validate target configuration."""
            if not config:
                return FlextResult.fail("Empty configuration provided")

            # Basic validation - check for required fields
            if "output_file" not in config:
                return FlextResult.fail("Missing required field: output_file")

            return FlextResult.ok(data=True)

        def get_default_config(self) -> FlextResult[dict[str, object]]:
            """Get default configuration for target."""
            return FlextResult.ok({"output_file": "test_output.json", "format": "json"})

        def validate_service(self) -> FlextResult[bool]:
            """Validate target service configuration and setup (renamed to avoid Pydantic conflict)."""
            try:
                # Basic validation - check if target has valid configuration
                config_result = self.get_default_config()
                if config_result.failure:
                    return FlextResult.fail(
                        f"Default config failed: {config_result.error}"
                    )
                return self.validate_target_config(config_result.value)
            except Exception as e:
                return FlextResult.fail(f"Target service validation failed: {e}")

    class DbtService(FlextDomainService[FlextMeltanoTypes.DBT.ProjectConfig]):
        """DBT service implementation using strict flext-core patterns."""

        project_name: FlextMeltanoTypes.DBT.Model

        def __init__(self, /, **data: object) -> None:
            """Initialize with Pydantic **data pattern (frozen model)."""
            # Pass data directly to Pydantic - it handles type conversion
            super().__init__(**data)  # type: ignore[arg-type]  # Pydantic handles object->field type conversion

        @property
        def adapter(self) -> object:
            """Get unified Meltano adapter for all operations."""
            return FlextMeltanoAdapter()

        def execute(self) -> FlextResult[FlextMeltanoTypes.DBT.ProjectConfig]:
            """Execute DBT service operation (required by FlextDomainService)."""
            logger = FlextLogger(__name__)
            logger.info("Executing DBT service", project_name=self.project_name)

            return FlextResult.ok({
                "service": "FlextMeltanoDbtService",
                "project_name": self.project_name,
                "status": "ready",
            })

        def get_info(self) -> FlextResult[FlextMeltanoTypes.DBT.ExecutionResult]:
            """Get service information."""
            return FlextResult.ok({
                "service_type": "dbt",
                "name": self.project_name,
                "status": "ready",
            })

        def get_profiles_config(self) -> FlextResult[dict[str, object]]:
            """Get DBT profiles configuration."""
            return FlextResult.ok({
                self.project_name: {
                    "outputs": {"dev": {"type": "duckdb", "path": "test.duckdb"}},
                    "target": "dev",
                }
            })

    # Generic Service Factory using advanced Python 3.13+ patterns

    @staticmethod
    def _create_service_generic(
        service_type: type[T_Service],
        name: str,
        field_name: str,
        service_prefix: str,
    ) -> FlextResult[T_Service]:
        """Generic factory method for all Meltano service types.

        Uses advanced Python 3.13+ generics with FlextUtilities validation
        and consolidated error handling following DRY principles.

        Args:
            service_type: The service class to instantiate (TapService, TargetService, etc.)
            name: The service name to validate and use
            field_name: The field name for the service (tap_name, target_name, etc.)
            service_prefix: The default prefix for validation (tap, target, dbt)

        Returns:
            FlextResult containing the created service instance or error

        """
        try:
            # Use FlextUtilities for name validation - consolidated pattern
            default_name = f"{service_prefix}-default"
            safe_name = FlextUtilities.TextProcessor.safe_string(name, default_name)

            # Consolidated validation logic
            if not safe_name or safe_name == default_name:
                return FlextResult[T_Service].fail(
                    f"Invalid {service_prefix} name: {name}"
                )

            # Dynamic service instance creation using **kwargs pattern
            service_kwargs = {field_name: safe_name}
            service_instance = service_type(**service_kwargs)

            return FlextResult[T_Service].ok(service_instance)

        except Exception as e:
            return FlextResult[T_Service].fail(
                f"Failed to create {service_prefix} service: {e}"
            )

    @staticmethod
    def create_tap_service(
        tap_name: str,
    ) -> FlextResult[FlextMeltanoService.TapService]:
        """Create tap service using generic factory pattern."""
        return FlextMeltanoService._create_service_generic(
            FlextMeltanoService.TapService, tap_name, "tap_name", "tap"
        )

    @staticmethod
    def create_target_service(
        target_name: str,
    ) -> FlextResult[FlextMeltanoService.TargetService]:
        """Create target service using generic factory pattern."""
        return FlextMeltanoService._create_service_generic(
            FlextMeltanoService.TargetService, target_name, "target_name", "target"
        )

    @staticmethod
    def create_dbt_service(
        project_name: str,
    ) -> FlextResult[FlextMeltanoService.DbtService]:
        """Create DBT service using generic factory pattern."""
        return FlextMeltanoService._create_service_generic(
            FlextMeltanoService.DbtService, project_name, "project_name", "dbt"
        )


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "FlextMeltanoService",
]
