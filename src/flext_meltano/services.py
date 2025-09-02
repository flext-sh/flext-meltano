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

from flext_core import FlextDomainService, FlextResult

from flext_meltano.typings import FlextMeltanoTypes

# Constants to avoid boolean positional arguments
_VALIDATION_SUCCESS = True

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

    class TapService(FlextDomainService[FlextMeltanoTypes.Plugin.Config]):
        """Tap service implementation using strict flext-core patterns.

        Pydantic model with frozen configuration, following FlextDomainService
        inheritance with proper field declarations and validation.
        """

        # Pydantic fields using local types directly
        tap_name: FlextMeltanoTypes.Plugin.Name

        def __init__(self, /, **data: object) -> None:
            """Initialize with Pydantic **data pattern (frozen model)."""
            super().__init__(**data)

        @property
        def wrapper_singer(self) -> object:
            """Get Singer wrapper for tap operations."""
            from flext_meltano.wrappers import FlextMeltanoWrapper

            return FlextMeltanoWrapper()

        @property
        def singer_adapter(self) -> object:
            """Get Singer adapter for tap operations."""
            from flext_meltano.singer_adapters import FlextMeltanoAdapters

            return FlextMeltanoAdapters()

        def execute(self) -> FlextResult[FlextMeltanoTypes.Plugin.Config]:
            """Execute tap service operation (required by FlextDomainService)."""
            from flext_core import FlextLogger

            logger = FlextLogger(__name__)
            logger.info("Executing tap service", tap_name=self.tap_name)

            return FlextResult.ok(
                {
                    "service": "FlextMeltanoTapService",
                    "tap_name": self.tap_name,
                    "status": "ready",
                }
            )

        def validate_config(self) -> FlextResult[None]:
            """Validate tap configuration using local types."""
            # Use local validation patterns
            if not self.tap_name:
                return FlextResult.fail("Empty tap_name configuration")

            return FlextResult.ok(None)

        def get_info(self) -> FlextMeltanoTypes.Plugin.PluginInfo:
            """Get service information."""
            return {"service_type": "tap", "name": self.tap_name, "status": "ready"}

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

            return FlextResult.ok(_VALIDATION_SUCCESS)

        def get_default_config(self) -> dict[str, object]:
            """Get default configuration for tap."""
            return {"connection_string": "test_connection"}

        def validate_service(self) -> FlextResult[bool]:
            """Validate tap service configuration and setup (renamed to avoid Pydantic conflict)."""
            try:
                # Basic validation - check if tap has valid configuration
                config = self.get_default_config()
                return self.validate_tap_config(config)
            except Exception as e:
                return FlextResult.fail(f"Tap service validation failed: {e}")

    class TargetService(FlextDomainService[FlextMeltanoTypes.Plugin.Config]):
        """Target service implementation using strict flext-core patterns."""

        target_name: FlextMeltanoTypes.Plugin.Name

        def __init__(self, /, **data: object) -> None:
            """Initialize with Pydantic **data pattern (frozen model)."""
            super().__init__(**data)

        @property
        def wrapper_singer(self) -> object:
            """Get Singer wrapper for target operations."""
            from flext_meltano.wrappers import FlextMeltanoWrapper

            return FlextMeltanoWrapper()

        @property
        def singer_adapter(self) -> object:
            """Get Singer adapter for target operations."""
            from flext_meltano.singer_adapters import FlextMeltanoAdapters

            return FlextMeltanoAdapters()

        def execute(self) -> FlextResult[FlextMeltanoTypes.Plugin.Config]:
            """Execute target service operation (required by FlextDomainService)."""
            from flext_core import FlextLogger

            logger = FlextLogger(__name__)
            logger.info("Executing target service", target_name=self.target_name)

            return FlextResult.ok(
                {
                    "service": "FlextMeltanoTargetService",
                    "target_name": self.target_name,
                    "status": "ready",
                }
            )

        def get_info(self) -> FlextMeltanoTypes.Plugin.PluginInfo:
            """Get service information."""
            return {
                "service_type": "target",
                "name": self.target_name,
                "status": "ready",
            }

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

            return FlextResult.ok(_VALIDATION_SUCCESS)

        def get_default_config(self) -> dict[str, object]:
            """Get default configuration for target."""
            return {"output_file": "test_output.json", "format": "json"}

        def validate_service(self) -> FlextResult[bool]:
            """Validate target service configuration and setup (renamed to avoid Pydantic conflict)."""
            try:
                # Basic validation - check if target has valid configuration
                config = self.get_default_config()
                return self.validate_target_config(config)
            except Exception as e:
                return FlextResult.fail(f"Target service validation failed: {e}")

    class DbtService(FlextDomainService[FlextMeltanoTypes.DBT.ProjectConfig]):
        """DBT service implementation using strict flext-core patterns."""

        project_name: FlextMeltanoTypes.DBT.Model

        def __init__(self, /, **data: object) -> None:
            """Initialize with Pydantic **data pattern (frozen model)."""
            super().__init__(**data)

        @property
        def wrapper_dbt(self) -> object:
            """Get DBT wrapper for DBT operations."""
            from flext_meltano.wrappers import FlextMeltanoWrapper

            return FlextMeltanoWrapper.DbtWrapper()

        @property
        def dbt_adapter(self) -> object:
            """Get DBT adapter for DBT operations."""
            from flext_meltano.adapters import FlextMeltanoAdapter

            return FlextMeltanoAdapter()

        def execute(self) -> FlextResult[FlextMeltanoTypes.DBT.ProjectConfig]:
            """Execute DBT service operation (required by FlextDomainService)."""
            from flext_core import FlextLogger

            logger = FlextLogger(__name__)
            logger.info("Executing DBT service", project_name=self.project_name)

            return FlextResult.ok(
                {
                    "service": "FlextMeltanoDbtService",
                    "project_name": self.project_name,
                    "status": "ready",
                }
            )

        def get_info(self) -> FlextMeltanoTypes.DBT.ExecutionResult:
            """Get service information."""
            return {"service_type": "dbt", "name": self.project_name, "status": "ready"}

        def get_profiles_config(self) -> dict[str, object]:
            """Get DBT profiles configuration."""
            return {
                self.project_name: {
                    "outputs": {"dev": {"type": "duckdb", "path": "test.duckdb"}},
                    "target": "dev",
                }
            }

    # Service factory methods using flext-core patterns
    @staticmethod
    def create_tap_service(tap_name: str) -> FlextMeltanoService.TapService:
        """Create tap service instance."""
        return FlextMeltanoService.TapService(tap_name=tap_name)

    @staticmethod
    def create_target_service(target_name: str) -> FlextMeltanoService.TargetService:
        """Create target service instance."""
        return FlextMeltanoService.TargetService(target_name=target_name)

    @staticmethod
    def create_dbt_service(project_name: str) -> FlextMeltanoService.DbtService:
        """Create DBT service instance."""
        return FlextMeltanoService.DbtService(project_name=project_name)


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "FlextMeltanoService",
]
