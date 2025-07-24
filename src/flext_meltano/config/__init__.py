"""FlextMeltano Configuration Module.

Configuration management following Clean Architecture patterns.
"""

from flext_meltano.config.settings import (
    FlextMeltanoBusinessConfig,
    FlextMeltanoExecutionConfig,
    FlextMeltanoMonitoringConfig,
    FlextMeltanoPluginConfig,
    FlextMeltanoProjectConfig,
    FlextMeltanoSettings,
    FlextMeltanoStateConfig,
    get_settings,
)
from flext_meltano.infrastructure.di_container import get_container

# Backward compatibility alias
get_meltano_settings = get_settings

__all__ = [
    "FlextMeltanoBusinessConfig",
    "FlextMeltanoExecutionConfig",
    "FlextMeltanoMonitoringConfig",
    "FlextMeltanoPluginConfig",
    "FlextMeltanoProjectConfig",
    "FlextMeltanoSettings",
    "FlextMeltanoStateConfig",
    "get_container",
    "get_meltano_settings",
    "get_settings",
]
