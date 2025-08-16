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
from typing import Any

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
def MeltanoConfig(*args: Any, **kwargs: Any) -> FlextMeltanoConfig:
    """Legacy alias for FlextMeltanoConfig."""
    _deprecation_warning("MeltanoConfig", "FlextMeltanoConfig")
    return FlextMeltanoConfig(*args, **kwargs)


def MeltanoBridge(*args: Any, **kwargs: Any) -> FlextMeltanoBridge:
    """Legacy alias for FlextMeltanoBridge."""
    _deprecation_warning("MeltanoBridge", "FlextMeltanoBridge")
    return FlextMeltanoBridge(*args, **kwargs)


def MeltanoCli(*args: Any, **kwargs: Any) -> FlextMeltanoCli:
    """Legacy alias for FlextMeltanoCli."""
    _deprecation_warning("MeltanoCli", "FlextMeltanoCli")
    return FlextMeltanoCli(*args, **kwargs)


def MeltanoOrchestrationService(*args: Any, **kwargs: Any) -> FlextMeltanoOrchestrationService:
    """Legacy alias for FlextMeltanoOrchestrationService."""
    _deprecation_warning("MeltanoOrchestrationService", "FlextMeltanoOrchestrationService")
    return FlextMeltanoOrchestrationService(*args, **kwargs)


def MeltanoDbtService(*args: Any, **kwargs: Any) -> FlextMeltanoDbtService:
    """Legacy alias for FlextMeltanoDbtService."""
    _deprecation_warning("MeltanoDbtService", "FlextMeltanoDbtService")
    return FlextMeltanoDbtService(*args, **kwargs)


def MeltanoSingerService(*args: Any, **kwargs: Any) -> FlextMeltanoSingerService:
    """Legacy alias for FlextMeltanoSingerService."""
    _deprecation_warning("MeltanoSingerService", "FlextMeltanoSingerService")
    return FlextMeltanoSingerService(*args, **kwargs)


# Legacy aliases for base classes
def MeltanoTap(*args: Any, **kwargs: Any) -> FlextMeltanoTap:
    """Legacy alias for FlextMeltanoTap."""
    _deprecation_warning("MeltanoTap", "FlextMeltanoTap")
    return FlextMeltanoTap(*args, **kwargs)


def MeltanoTarget(*args: Any, **kwargs: Any) -> FlextMeltanoTarget:
    """Legacy alias for FlextMeltanoTarget."""
    _deprecation_warning("MeltanoTarget", "FlextMeltanoTarget")
    return FlextMeltanoTarget(*args, **kwargs)


def MeltanoDbt(*args: Any, **kwargs: Any) -> FlextMeltanoDbt:
    """Legacy alias for FlextMeltanoDbt."""
    _deprecation_warning("MeltanoDbt", "FlextMeltanoDbt")
    return FlextMeltanoDbt(*args, **kwargs)


# Legacy aliases for utility classes
def MeltanoDiscovery(*args: Any, **kwargs: Any) -> FlextMeltanoDiscovery:
    """Legacy alias for FlextMeltanoDiscovery."""
    _deprecation_warning("MeltanoDiscovery", "FlextMeltanoDiscovery")
    return FlextMeltanoDiscovery(*args, **kwargs)


def MeltanoInstaller(*args: Any, **kwargs: Any) -> FlextMeltanoInstaller:
    """Legacy alias for FlextMeltanoInstaller."""
    _deprecation_warning("MeltanoInstaller", "FlextMeltanoInstaller")
    return FlextMeltanoInstaller(*args, **kwargs)


# Legacy exception aliases (more concise names that were probably used)
def MeltanoError(*args: Any, **kwargs: Any) -> FlextMeltanoError:
    """Legacy alias for FlextMeltanoError."""
    _deprecation_warning("MeltanoError", "FlextMeltanoError")
    return FlextMeltanoError(*args, **kwargs)


def MeltanoValidationError(*args: Any, **kwargs: Any) -> FlextMeltanoValidationError:
    """Legacy alias for FlextMeltanoValidationError."""
    _deprecation_warning("MeltanoValidationError", "FlextMeltanoValidationError")
    return FlextMeltanoValidationError(*args, **kwargs)


def MeltanoConfigurationError(*args: Any, **kwargs: Any) -> FlextMeltanoConfigurationError:
    """Legacy alias for FlextMeltanoConfigurationError."""
    _deprecation_warning("MeltanoConfigurationError", "FlextMeltanoConfigurationError")
    return FlextMeltanoConfigurationError(*args, **kwargs)


def MeltanoConnectionError(*args: Any, **kwargs: Any) -> FlextMeltanoConnectionError:
    """Legacy alias for FlextMeltanoConnectionError."""
    _deprecation_warning("MeltanoConnectionError", "FlextMeltanoConnectionError")
    return FlextMeltanoConnectionError(*args, **kwargs)


def MeltanoPluginError(*args: Any, **kwargs: Any) -> FlextMeltanoPluginError:
    """Legacy alias for FlextMeltanoPluginError."""
    _deprecation_warning("MeltanoPluginError", "FlextMeltanoPluginError")
    return FlextMeltanoPluginError(*args, **kwargs)


def MeltanoExecutionError(*args: Any, **kwargs: Any) -> FlextMeltanoExecutionError:
    """Legacy alias for FlextMeltanoExecutionError."""
    _deprecation_warning("MeltanoExecutionError", "FlextMeltanoExecutionError")
    return FlextMeltanoExecutionError(*args, **kwargs)


def MeltanoSingerError(*args: Any, **kwargs: Any) -> FlextMeltanoSingerError:
    """Legacy alias for FlextMeltanoSingerError."""
    _deprecation_warning("MeltanoSingerError", "FlextMeltanoSingerError")
    return FlextMeltanoSingerError(*args, **kwargs)


def MeltanoDBTError(*args: Any, **kwargs: Any) -> FlextMeltanoDBTError:
    """Legacy alias for FlextMeltanoDBTError."""
    _deprecation_warning("MeltanoDBTError", "FlextMeltanoDBTError")
    return FlextMeltanoDBTError(*args, **kwargs)


# Legacy function aliases
def get_meltano_bridge(*args: Any, **kwargs: Any) -> Any:
    """Legacy alias for FlextMeltanoBridge constructor."""
    _deprecation_warning("get_meltano_bridge", "FlextMeltanoBridge")
    return FlextMeltanoBridge(*args, **kwargs)


def create_meltano_tap(*args: Any, **kwargs: Any) -> Any:
    """Legacy alias for create_tap."""
    _deprecation_warning("create_meltano_tap", "create_tap")
    return create_tap(*args, **kwargs)


def create_meltano_target(*args: Any, **kwargs: Any) -> Any:
    """Legacy alias for create_target."""
    _deprecation_warning("create_meltano_target", "create_target")
    return create_target(*args, **kwargs)


def create_meltano_dbt(*args: Any, **kwargs: Any) -> Any:
    """Legacy alias for create_dbt_service."""
    _deprecation_warning("create_meltano_dbt", "create_dbt_service")
    return create_dbt_service(*args, **kwargs)


def execute_command(*args: Any, **kwargs: Any) -> Any:
    """Legacy alias for execute_meltano_command."""
    _deprecation_warning("execute_command", "execute_meltano_command")
    return execute_meltano_command(*args, **kwargs)


def run_meltano_pipeline(*args: Any, **kwargs: Any) -> Any:
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
