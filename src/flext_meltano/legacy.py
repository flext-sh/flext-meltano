"""Legacy compatibility facade for flext-meltano.

This module provides backward compatibility for APIs that may have been refactored
or renamed during the Pydantic modernization process. It follows the same pattern
as flext-core's legacy.py to ensure consistent facade patterns across the ecosystem.

All imports here should be considered deprecated and may issue warnings.
Modern code should import directly from the appropriate modules.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

# Import modern implementations to re-export under legacy names
from flext_meltano.base import (
    FlextMeltanoConfig,
    FlextMeltanoDbt,
    FlextMeltanoTap,
    FlextMeltanoTarget,
    create_dbt_service,
    create_tap,
    create_target,
)
from flext_meltano.cli import FlextMeltanoCli
from flext_meltano.core import (
    FlextMeltanoDbtService,
    FlextMeltanoOrchestrationService,
    FlextMeltanoSingerService,
)
from flext_meltano.discovery import (
    FlextMeltanoDiscovery,
)
from flext_meltano.exceptions import (
    FlextMeltanoConfigurationError,
    FlextMeltanoConnectionError,
    FlextMeltanoDBTError,
    FlextMeltanoError,
    FlextMeltanoExecutionError,
    FlextMeltanoPluginError,
    FlextMeltanoSingerError,
    FlextMeltanoValidationError,
)
from flext_meltano.execution import (
    execute_meltano_command,
    run_pipeline,
)
from flext_meltano.installation import (
    FlextMeltanoInstaller,
)
from flext_meltano.simple_bridge import FlextMeltanoBridge


def _deprecation_warning(old_name: str, new_name: str) -> None:
    """Issue a deprecation warning for legacy imports."""
    warnings.warn(
      f"{old_name} is deprecated, use {new_name} instead",
      DeprecationWarning,
      stacklevel=3,
    )


# Legacy aliases for main classes - commonly used names
def MeltanoConfig(*args: object, **kwargs: object) -> FlextMeltanoConfig:  # noqa: N802
    """Legacy alias for FlextMeltanoConfig."""
    _deprecation_warning("MeltanoConfig", "FlextMeltanoConfig")
    return FlextMeltanoConfig(*args, **kwargs)


def MeltanoBridge(*args: object, **kwargs: object) -> FlextMeltanoBridge:  # noqa: N802
    """Legacy alias for FlextMeltanoBridge."""
    _deprecation_warning("MeltanoBridge", "FlextMeltanoBridge")
    return FlextMeltanoBridge(*args, **kwargs)


def MeltanoCli(*args: object, **kwargs: object) -> FlextMeltanoCli:  # noqa: N802
    """Legacy alias for FlextMeltanoCli."""
    _deprecation_warning("MeltanoCli", "FlextMeltanoCli")
    return FlextMeltanoCli(*args, **kwargs)


def MeltanoOrchestrationService(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoOrchestrationService:
    """Legacy alias for FlextMeltanoOrchestrationService."""
    _deprecation_warning(
      "MeltanoOrchestrationService", "FlextMeltanoOrchestrationService",
    )
    return FlextMeltanoOrchestrationService(*args, **kwargs)


def MeltanoDbtService(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoDbtService:
    """Legacy alias for FlextMeltanoDbtService."""
    _deprecation_warning("MeltanoDbtService", "FlextMeltanoDbtService")
    return FlextMeltanoDbtService(*args, **kwargs)


def MeltanoSingerService(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoSingerService:
    """Legacy alias for FlextMeltanoSingerService."""
    _deprecation_warning("MeltanoSingerService", "FlextMeltanoSingerService")
    return FlextMeltanoSingerService(*args, **kwargs)


# Legacy aliases for base classes
def MeltanoTap(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoTap:
    """Legacy alias for FlextMeltanoTap."""
    _deprecation_warning("MeltanoTap", "FlextMeltanoTap")
    return FlextMeltanoTap(*args, **kwargs)


def MeltanoTarget(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoTarget:
    """Legacy alias for FlextMeltanoTarget."""
    _deprecation_warning("MeltanoTarget", "FlextMeltanoTarget")
    return FlextMeltanoTarget(*args, **kwargs)


def MeltanoDbt(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoDbt:
    """Legacy alias for FlextMeltanoDbt."""
    _deprecation_warning("MeltanoDbt", "FlextMeltanoDbt")
    return FlextMeltanoDbt(*args, **kwargs)


# Legacy aliases for utility classes
def MeltanoDiscovery(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoDiscovery:
    """Legacy alias for FlextMeltanoDiscovery."""
    _deprecation_warning("MeltanoDiscovery", "FlextMeltanoDiscovery")
    return FlextMeltanoDiscovery(*args, **kwargs)


def MeltanoInstaller(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoInstaller:
    """Legacy alias for FlextMeltanoInstaller."""
    _deprecation_warning("MeltanoInstaller", "FlextMeltanoInstaller")
    return FlextMeltanoInstaller(*args, **kwargs)


# Legacy exception aliases (more concise names that were probably used)
def MeltanoError(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoError:
    """Legacy alias for FlextMeltanoError."""
    _deprecation_warning("MeltanoError", "FlextMeltanoError")
    return FlextMeltanoError(*args, **kwargs)


def MeltanoValidationError(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoValidationError:
    """Legacy alias for FlextMeltanoValidationError."""
    _deprecation_warning("MeltanoValidationError", "FlextMeltanoValidationError")
    return FlextMeltanoValidationError(*args, **kwargs)


def MeltanoConfigurationError(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoConfigurationError:
    """Legacy alias for FlextMeltanoConfigurationError."""
    _deprecation_warning("MeltanoConfigurationError", "FlextMeltanoConfigurationError")
    return FlextMeltanoConfigurationError(*args, **kwargs)


def MeltanoConnectionError(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoConnectionError:
    """Legacy alias for FlextMeltanoConnectionError."""
    _deprecation_warning("MeltanoConnectionError", "FlextMeltanoConnectionError")
    return FlextMeltanoConnectionError(*args, **kwargs)


def MeltanoPluginError(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoPluginError:
    """Legacy alias for FlextMeltanoPluginError."""
    _deprecation_warning("MeltanoPluginError", "FlextMeltanoPluginError")
    return FlextMeltanoPluginError(*args, **kwargs)


def MeltanoExecutionError(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoExecutionError:
    """Legacy alias for FlextMeltanoExecutionError."""
    _deprecation_warning("MeltanoExecutionError", "FlextMeltanoExecutionError")
    return FlextMeltanoExecutionError(*args, **kwargs)


def MeltanoSingerError(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoSingerError:
    """Legacy alias for FlextMeltanoSingerError."""
    _deprecation_warning("MeltanoSingerError", "FlextMeltanoSingerError")
    return FlextMeltanoSingerError(*args, **kwargs)


def MeltanoDBTError(  # noqa: N802
    *args: object, **kwargs: object,
) -> FlextMeltanoDBTError:
    """Legacy alias for FlextMeltanoDBTError."""
    _deprecation_warning("MeltanoDBTError", "FlextMeltanoDBTError")
    return FlextMeltanoDBTError(*args, **kwargs)


# Legacy function aliases
def get_meltano_bridge(*args: object, **kwargs: object) -> object:
    """Legacy alias for FlextMeltanoBridge constructor."""
    _deprecation_warning("get_meltano_bridge", "FlextMeltanoBridge")
    return FlextMeltanoBridge(*args, **kwargs)


def create_meltano_tap(*args: object, **kwargs: object) -> object:
    """Legacy alias for create_tap."""
    _deprecation_warning("create_meltano_tap", "create_tap")
    return create_tap(*args, **kwargs)


def create_meltano_target(*args: object, **kwargs: object) -> object:
    """Legacy alias for create_target."""
    _deprecation_warning("create_meltano_target", "create_target")
    return create_target(*args, **kwargs)


def create_meltano_dbt(*args: object, **kwargs: object) -> object:
    """Legacy alias for create_dbt_service."""
    _deprecation_warning("create_meltano_dbt", "create_dbt_service")
    return create_dbt_service(*args, **kwargs)


def execute_command(*args: object, **kwargs: object) -> object:
    """Legacy alias for execute_meltano_command."""
    _deprecation_warning("execute_command", "execute_meltano_command")
    return execute_meltano_command(*args, **kwargs)


def run_meltano_pipeline(*args: object, **kwargs: object) -> object:
    """Legacy alias for run_pipeline."""
    _deprecation_warning("run_meltano_pipeline", "run_pipeline")
    return run_pipeline(*args, **kwargs)


# Export legacy aliases for backward compatibility
__all__ = [
    "MeltanoBridge",
    "MeltanoCli",
    # Legacy class aliases
    "MeltanoConfig",
    "MeltanoConfigurationError",
    "MeltanoConnectionError",
    "MeltanoDBTError",
    "MeltanoDbt",
    "MeltanoDbtService",
    "MeltanoDiscovery",
    # Legacy exception aliases
    "MeltanoError",
    "MeltanoExecutionError",
    "MeltanoInstaller",
    "MeltanoOrchestrationService",
    "MeltanoPluginError",
    "MeltanoSingerError",
    "MeltanoSingerService",
    "MeltanoTap",
    "MeltanoTarget",
    "MeltanoValidationError",
    "create_meltano_dbt",
    "create_meltano_tap",
    "create_meltano_target",
    "execute_command",
    # Legacy function aliases
    "get_meltano_bridge",
    "run_meltano_pipeline",
]
