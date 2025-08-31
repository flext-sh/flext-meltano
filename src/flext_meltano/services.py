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

        def execute(self) -> FlextResult[FlextMeltanoTypes.JsonObject]:
            """Execute tap service operation (required by FlextDomainService)."""
            from flext_core import FlextLogger

            logger = FlextLogger(__name__)
            logger.info("Executing tap service", tap_name=self.tap_name)

            return FlextResult.ok({
                "service": "TapService",
                "tap_name": self.tap_name,
                "status": "ready",
            })

        def validate_config(self, config: FlextMeltanoTypes.Singer.TapConfig) -> FlextResult[FlextMeltanoTypes.Singer.TapConfig]:
            """Validate tap configuration using local types."""
            # Use local validation patterns
            if not config:
                return FlextResult.fail("Empty configuration")

            return FlextResult.ok(config)

        def get_info(self) -> FlextMeltanoTypes.Plugin.PluginInfo:
            """Get service information."""
            return {
                "service_type": "tap",
                "name": self.tap_name,
                "status": "ready"
            }

    class TargetService(FlextDomainService[FlextMeltanoTypes.Plugin.Config]):
        """Target service implementation using strict flext-core patterns."""

        target_name: FlextMeltanoTypes.Plugin.Name

        def __init__(self, /, **data: object) -> None:
            """Initialize with Pydantic **data pattern (frozen model)."""
            super().__init__(**data)

        def execute(self) -> FlextResult[FlextMeltanoTypes.JsonObject]:
            """Execute target service operation (required by FlextDomainService)."""
            from flext_core import FlextLogger

            logger = FlextLogger(__name__)
            logger.info("Executing target service", target_name=self.target_name)

            return FlextResult.ok({
                "service": "TargetService",
                "target_name": self.target_name,
                "status": "ready",
            })

        def get_info(self) -> FlextMeltanoTypes.Plugin.PluginInfo:
            """Get service information."""
            return {
                "service_type": "target",
                "name": self.target_name,
                "status": "ready"
            }

    class DbtService(FlextDomainService[FlextMeltanoTypes.DBT.ProjectConfig]):
        """DBT service implementation using strict flext-core patterns."""

        project_name: FlextMeltanoTypes.DBT.Model

        def __init__(self, /, **data: object) -> None:
            """Initialize with Pydantic **data pattern (frozen model)."""
            super().__init__(**data)

        def execute(self) -> FlextResult[FlextMeltanoTypes.JsonObject]:
            """Execute DBT service operation (required by FlextDomainService)."""
            from flext_core import FlextLogger

            logger = FlextLogger(__name__)
            logger.info("Executing DBT service", project_name=self.project_name)

            return FlextResult.ok({
                "service": "DbtService",
                "project_name": self.project_name,
                "status": "ready",
            })

        def get_info(self) -> FlextMeltanoTypes.DBT.ExecutionResult:
            """Get service information."""
            return {
                "service_type": "dbt",
                "name": self.project_name,
                "status": "ready"
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
