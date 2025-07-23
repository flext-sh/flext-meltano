"""FLEXT Meltano - Unified Data Integration Platform.

Modern enterprise-grade library that unifies:
- Meltano (data integration orchestration)
- Singer SDK (tap/target development)
- dbt (data transformation)
- Meltano EDK (extension development)
- FlexCore Go runtime integration

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Core FlextCore patterns
from flext_core import FlextResult
from flext_core.constants import FlextConstants
from flext_core.container import FlextContainer

from flext_meltano.config.loader import FlextMeltanoConfigLoader

# Configuration and settings
from flext_meltano.config.settings import FlextMeltanoSettings

# Unified Meltano platform classes
from flext_meltano.core.platform import FlextMeltanoPlatform
from flext_meltano.core.runtime import FlextMeltanoRuntime
from flext_meltano.dbt.models import FlextMeltanoDbtModel

# dbt integration
from flext_meltano.dbt.project import FlextMeltanoDbtProject
from flext_meltano.dbt.runner import FlextMeltanoDbtRunner

# Meltano EDK integration
from flext_meltano.edk.extension import FlextMeltanoExtension
from flext_meltano.edk.manager import FlextMeltanoExtensionManager
from flext_meltano.environment.manager import FlextMeltanoEnvironmentManager
from flext_meltano.environment.models import FlextMeltanoEnvironment

# Helpers and utilities
from flext_meltano.helpers.cli import flext_run_command
from flext_meltano.helpers.config import flext_load_config
from flext_meltano.helpers.discovery import flext_discover_plugins
from flext_meltano.helpers.execution import flext_execute_job
from flext_meltano.helpers.installation import flext_install_plugin
from flext_meltano.helpers.validation import flext_validate_project
from flext_meltano.jobs.executor import FlextMeltanoJobExecutor

# Job and execution management
from flext_meltano.jobs.manager import FlextMeltanoJobManager
from flext_meltano.jobs.models import FlextMeltanoJob

# Plugin management
from flext_meltano.plugins.manager import FlextMeltanoPluginManager
from flext_meltano.plugins.models import FlextMeltanoPlugin

# Project and environment management
from flext_meltano.project.manager import FlextMeltanoProjectManager
from flext_meltano.project.models import FlextMeltanoProject
from flext_meltano.singer.catalog import FlextMeltanoCatalog
from flext_meltano.singer.stream import FlextMeltanoStream

# Singer SDK integration
from flext_meltano.singer.tap import FlextMeltanoTap
from flext_meltano.singer.target import FlextMeltanoTarget

# State management
from flext_meltano.state.manager import FlextMeltanoStateManager
from flext_meltano.state.models import FlextMeltanoState

__version__ = "0.7.0"

# Main platform instance factory
def create_flext_meltano_platform(
    config: dict[str, object] | None = None,
) -> FlextMeltanoPlatform:
    """Create unified FLEXT Meltano platform instance.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured FlextMeltanoPlatform instance

    """
    return FlextMeltanoPlatform(config or {})

__all__ = [
    "FlextConstants",
    "FlextContainer",
    "FlextMeltanoCatalog",
    "FlextMeltanoConfigLoader",
    "FlextMeltanoDbtModel",
    # dbt integration
    "FlextMeltanoDbtProject",
    "FlextMeltanoDbtRunner",
    # Environment management
    "FlextMeltanoEnvironment",
    "FlextMeltanoEnvironmentManager",
    # EDK extensions
    "FlextMeltanoExtension",
    "FlextMeltanoExtensionManager",
    # Job management
    "FlextMeltanoJob",
    "FlextMeltanoJobExecutor",
    "FlextMeltanoJobManager",
    # Core platform
    "FlextMeltanoPlatform",
    # Plugin management
    "FlextMeltanoPlugin",
    "FlextMeltanoPluginManager",
    # Project management
    "FlextMeltanoProject",
    "FlextMeltanoProjectManager",
    "FlextMeltanoRuntime",
    # Configuration
    "FlextMeltanoSettings",
    # State management
    "FlextMeltanoState",
    "FlextMeltanoStateManager",
    "FlextMeltanoStream",
    # Singer SDK
    "FlextMeltanoTap",
    "FlextMeltanoTarget",
    # Core patterns (re-exported)
    "FlextResult",
    # Metadata
    "__version__",
    "create_flext_meltano_platform",
    "flext_discover_plugins",
    "flext_execute_job",
    "flext_install_plugin",
    "flext_load_config",
    # Helpers
    "flext_run_command",
    "flext_validate_project",
]
