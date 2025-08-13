"""Legacy compatibility module for flext-meltano.

This module contains all backward compatibility code to support existing
consumers while they migrate to the new flext-core patterns.

All code in this module is considered deprecated and will be removed
in a future major version.
"""

from __future__ import annotations

import asyncio
import warnings
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

# Import all needed modules at top level
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.discovery import FlextMeltanoDiscoverer
from flext_meltano.execution import FlextMeltanoExecutor
from flext_meltano.installation import FlextMeltanoInstaller
from flext_meltano.validation import FlextMeltanoValidationService

# =============================================================================
# LEGACY RESULT TYPE
# =============================================================================


class FlextMeltanoResult:
    """Legacy result type for backward compatibility.

    DEPRECATED: Use FlextResult from flext-core instead.
    This class will be removed in version 3.0.0.
    """

    def __init__(
        self,
        *,
        success: bool,
        data: dict[str, object] | None = None,
        error: str = "",
    ) -> None:
        """Initialize result."""
        warnings.warn(
            "FlextMeltanoResult is deprecated. Use FlextResult from flext-core instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        self.success = success
        self.data = data
        self.error = error

    @classmethod
    def ok(cls, data: dict[str, object] | None = None) -> FlextMeltanoResult:
        """Create success result."""
        return cls(success=True, data=data)

    @classmethod
    def fail(cls, error: str) -> FlextMeltanoResult:
        """Create failure result."""
        return cls(success=False, error=error)


# =============================================================================
# LEGACY EXECUTION FUNCTIONS
# =============================================================================


def flext_meltano_execute_job(
    tap_name: str,
    target_name: str,
    project_root: str | Path = ".",
    environment: str = "dev",
) -> FlextMeltanoResult:
    """Execute pipeline job (legacy compatibility).

    DEPRECATED: Use FlextMeltanoExecutor.execute_pipeline instead.
    This function will be removed in version 3.0.0.
    """
    warnings.warn(
        "flext_meltano_execute_job is deprecated. Use FlextMeltanoExecutor.execute_pipeline instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    config = FlextMeltanoConfig(
        project_root=str(project_root),
        environment=environment,
    )
    executor = FlextMeltanoExecutor(config)

    result = executor.execute_pipeline(tap_name, target_name)
    if result.success:
        data_dict = result.data.dict() if hasattr(result.data, "dict") else result.data  # type: ignore[union-attr]
        return FlextMeltanoResult.ok(data_dict)
    return FlextMeltanoResult.fail(result.error or "Execution failed")


def flext_meltano_run_command(
    args: list[str],
    project_root: str | Path = ".",
    environment: str = "dev",
) -> FlextMeltanoResult:
    """Run generic command (legacy compatibility).

    DEPRECATED: Use FlextMeltanoExecutor.run_command instead.
    This function will be removed in version 3.0.0.
    """
    warnings.warn(
        "flext_meltano_run_command is deprecated. Use FlextMeltanoExecutor.run_command instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    config = FlextMeltanoConfig(
        project_root=str(project_root),
        environment=environment,
    )
    executor = FlextMeltanoExecutor(config)

    result = executor.run_command(args)
    if result.success:
        data_dict = result.data.dict() if hasattr(result.data, "dict") else result.data  # type: ignore[union-attr]
        return FlextMeltanoResult.ok(data_dict)
    return FlextMeltanoResult.fail(result.error or "Execution failed")


# =============================================================================
# LEGACY DISCOVERY FUNCTIONS
# =============================================================================


def flext_meltano_discover_catalog(
    tap_name: str,
    project_root: str | Path = ".",
    config: dict[str, object] | None = None,
) -> FlextMeltanoResult:
    """Discover tap catalog (legacy compatibility).

    DEPRECATED: Use FlextMeltanoDiscoverer.discover_catalog instead.
    This function will be removed in version 3.0.0.
    """
    warnings.warn(
        "flext_meltano_discover_catalog is deprecated. Use FlextMeltanoDiscoverer.discover_catalog instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    meltano_config = FlextMeltanoConfig(project_root=str(project_root))
    discoverer = FlextMeltanoDiscoverer(meltano_config)

    # Run async function in sync context; if already in loop, return graceful failure
    try:
        asyncio.get_running_loop()
        # If there's already a running loop, we cannot use asyncio.run or run_until_complete
        # The proper solution would be to make this function async, but for backward compatibility
        # we return a graceful failure that the test can handle
        return FlextMeltanoResult.fail("Cannot run catalog discovery within existing event loop - use async version")
    except RuntimeError:
        # No running loop, safe to use asyncio.run
        result = asyncio.run(discoverer.discover_catalog(tap_name, config))
    if result.success:
        data_dict = result.data.dict() if hasattr(result.data, "dict") else result.data  # type: ignore[union-attr]
        return FlextMeltanoResult.ok(data_dict)
    return FlextMeltanoResult.fail(result.error or "Unknown error")


def flext_meltano_discover_plugins(
    project_root: str | Path = ".",
    plugin_type: str | None = None,
) -> FlextMeltanoResult:
    """Discover available plugins (legacy compatibility).

    DEPRECATED: Use FlextMeltanoDiscoverer.discover_plugins instead.
    This function will be removed in version 3.0.0.
    """
    warnings.warn(
        "flext_meltano_discover_plugins is deprecated. Use FlextMeltanoDiscoverer.discover_plugins instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    config = FlextMeltanoConfig(project_root=str(project_root))
    discoverer = FlextMeltanoDiscoverer(config)

    result = discoverer.discover_plugins(plugin_type)
    if result.success:
        if result.data:
            plugins_dict = [plugin.dict() for plugin in result.data]
            return FlextMeltanoResult.ok({"plugins": plugins_dict})
        return FlextMeltanoResult.ok({"plugins": []})
    return FlextMeltanoResult.fail(result.error or "Unknown error")


# =============================================================================
# LEGACY VALIDATION FUNCTIONS
# =============================================================================


def validate_project(
    project_root: Path | None = None,
) -> FlextMeltanoResult:
    """Validate Meltano project configuration (legacy compatibility).

    DEPRECATED: Use FlextMeltanoValidationService.validate_project instead.
    This function will be removed in version 3.0.0.
    """
    warnings.warn(
        "validate_project is deprecated. Use FlextMeltanoValidationService.validate_project instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    config = FlextMeltanoConfig(
        project_root=str(project_root) if project_root else ".",
    )
    service = FlextMeltanoValidationService(config)

    # Convert FlextResult to legacy FlextMeltanoResult
    result = service.validate_project()
    if result.success:
        validation_result = result.data
        if validation_result is None:
            return FlextMeltanoResult.fail("Validation result is None")
        legacy_data = {
            "valid": validation_result.is_valid,
            "has_meltano_yml": validation_result.details.get(
                "meltano_yml_exists", False,
            ),
            "has_project_dir": validation_result.details.get(
                "meltano_dir_exists", False,
            ),
            "errors": list(validation_result.issues),
            "warnings": validation_result.warnings,
            "suggestions": ["Review validation errors", "Check project structure"],
        }
        return FlextMeltanoResult.ok(legacy_data)
    return FlextMeltanoResult.fail(result.error or "Validation failed")


async def test_tap_connection(
    tap_name: str,
    project_root: str | Path,
    config: dict[str, object] | None,
) -> FlextMeltanoResult:
    """Test tap connection (legacy compatibility).

    DEPRECATED: Use FlextMeltanoValidationService.test_tap_connection instead.
    This function will be removed in version 3.0.0.
    """
    warnings.warn(
        "test_tap_connection is deprecated. Use FlextMeltanoValidationService.test_tap_connection instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    meltano_config = FlextMeltanoConfig(
        project_root=str(project_root),
    )
    service = FlextMeltanoValidationService(meltano_config)

    # Convert FlextResult to legacy FlextMeltanoResult
    result = await service.test_tap_connection(tap_name, config)
    if result.success:
        validation_result = result.data
        if validation_result is None:
            return FlextMeltanoResult.fail("Validation result is None")
        legacy_data = {
            "connected": validation_result.is_valid,
            "message": validation_result.warnings[0]
            if validation_result.warnings
            else "Connection test completed",
            "details": validation_result.issues,
        }
        if validation_result.is_valid:
            return FlextMeltanoResult.ok(legacy_data)
        return FlextMeltanoResult.fail(str(legacy_data["message"]))
    return FlextMeltanoResult.fail(result.error or "Connection test failed")


def validate_tap_config(
    tap_name: str,
    config: dict[str, object],
) -> FlextMeltanoResult:
    """Validate tap configuration (legacy compatibility).

    DEPRECATED: Use FlextMeltanoValidationService.validate_tap_config instead.
    This function will be removed in version 3.0.0.
    """
    warnings.warn(
        "validate_tap_config is deprecated. Use FlextMeltanoValidationService.validate_tap_config instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    meltano_config = FlextMeltanoConfig()
    service = FlextMeltanoValidationService(meltano_config)

    # Convert FlextResult to legacy FlextMeltanoResult
    result = service.validate_tap_config(tap_name, config)
    if result.success:
        validation_result = result.data
        if validation_result is None:
            return FlextMeltanoResult.fail("Validation result is None")
        legacy_data = {
            "valid": validation_result.is_valid,
            "errors": validation_result.issues,
            "warnings": validation_result.warnings,
            "required_fields": ["host", "port", "database", "username", "password"],
        }
        return FlextMeltanoResult.ok(legacy_data)
    return FlextMeltanoResult.fail(result.error or "Validation failed")


# =============================================================================
# LEGACY INSTALLATION FUNCTIONS
# =============================================================================


def install_plugin(
    plugin_type: str,
    plugin_name: str,
    project_root: str | Path = ".",
    pip_url: str | None = None,
) -> FlextMeltanoResult:
    """Install plugin using installer (legacy compatibility).

    DEPRECATED: Use FlextMeltanoInstaller.add_plugin instead.
    This function will be removed in version 3.0.0.
    """
    warnings.warn(
        "install_plugin is deprecated. Use FlextMeltanoInstaller.add_plugin instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    config = FlextMeltanoConfig(project_root=str(project_root))
    installer = FlextMeltanoInstaller(config)

    # Convert FlextResult to legacy FlextMeltanoResult
    result = installer.install_plugin(plugin_type, plugin_name, pip_url=pip_url)
    if result.success:
        data_dict: dict[str, object] = (
            result.data if isinstance(result.data, dict) else {}
        )
        return FlextMeltanoResult.ok(data_dict)
    return FlextMeltanoResult.fail(result.error or "Unknown error")


# =============================================================================
# LEGACY ALIASES
# =============================================================================

# These are maintained for backward compatibility but should not be used
# in new code. They will be removed in version 3.0.0.

# Execution aliases
execute_meltano_command = flext_meltano_run_command
run_pipeline = flext_meltano_execute_job

# Discovery aliases
discover_catalog = flext_meltano_discover_catalog
discover_plugins = flext_meltano_discover_plugins


__all__ = [
    "FlextMeltanoResult",
    "discover_catalog",
    "discover_plugins",
    "execute_meltano_command",
    "flext_meltano_discover_catalog",
    "flext_meltano_discover_plugins",
    "flext_meltano_execute_job",
    "flext_meltano_run_command",
    "install_plugin",
    "run_pipeline",
    "test_tap_connection",
    "validate_project",
    "validate_tap_config",
]
