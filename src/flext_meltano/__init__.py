"""FLEXT Meltano - Enterprise ELT orchestration platform.

Core Meltano/Singer/DBT integration library for the FLEXT ecosystem.
Provides execution, discovery, installation, and validation services.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from flext_meltano import singer

if TYPE_CHECKING:
    from pathlib import Path

    from flext_core import FlextResult

# === CORE BASE CLASSES ===
# DBT integration - required dependency
import dbt.contracts.results
from dbt.adapters.base import BaseRelation
from dbt.adapters.base.connections import (
    BaseConnectionManager,
    ConnectionState,
)
from dbt.adapters.contracts.connection import (
    AdapterRequiredConfig,
    AdapterResponse,
    Connection,
    Credentials,
)
from dbt.adapters.sql import SQLAdapter

# DBT exceptions - using available modules
from dbt_common.exceptions import (
    DbtDatabaseError,
    DbtRuntimeError,
)

# Meltano Core integration - required dependency
from meltano.core.project import Project as MeltanoCoreProject

# === OPTIONAL IMPORTS ===
# Singer SDK integration - required dependency
from singer_sdk import Stream, Tap, Target, typing as singer_typing
from singer_sdk.authenticators import OAuthAuthenticator
from singer_sdk.sinks import BatchSink, Sink, SQLSink
from singer_sdk.testing import get_tap_test_class
from singer_sdk.typing import PropertiesList, Property

from flext_meltano.base import (
    FlextMeltanoBaseService,
    FlextMeltanoConfig,
    FlextMeltanoDbtService,
    FlextMeltanoEvent,
    FlextMeltanoExtensionService,
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
    create_meltano_dbt_service,
    create_meltano_extension_service,
    create_meltano_tap_service,
    create_meltano_target_service,
)

# === CLI INTERFACE ===
from flext_meltano.cli import (
    FlextMeltanoCli,
    flext_meltano_run_cli,
)

# === COMMON UTILITIES ===
from flext_meltano.common import (
    validate_config_value,
    validate_directory_path,
    validate_file_path,
)

# === DISCOVERY & CATALOG MANAGEMENT ===
from flext_meltano.discovery import (
    FlextMeltanoDiscoverer,
    FlextMeltanoPlugin,
    create_discoverer,
    flext_meltano_discover_catalog,
    flext_meltano_discover_plugins,
)

# === EXECUTION HELPERS ===
from flext_meltano.execution import (
    FlextMeltanoExecutionCommand,
    FlextMeltanoExecutionContext,
    FlextMeltanoExecutor,
    FlextMeltanoResult,
    create_executor,
    flext_meltano_execute_job,
    flext_meltano_run_command,
)

# === INSTALLATION & PLUGIN MANAGEMENT ===
from flext_meltano.installation import (
    FlextMeltanoInstallationContext,
    FlextMeltanoInstaller,
    FlextMeltanoPluginInfo,
    create_installer_service,
    flext_meltano_install_plugin,
)

# === VALIDATION & TESTING ===
from flext_meltano.validation import (
    FlextMeltanoValidationResult,
    FlextMeltanoValidationService,
    create_validation_service,
    flext_meltano_test_tap_connection,
    flext_meltano_validate_project,
    flext_meltano_validate_tap_config,
)

# DBT run result - using available module
DbtRunResult = dbt.contracts.results.RunResult


# === LEGACY COMPATIBILITY ===
def _deprecated_api_warning(old_name: str, new_name: str) -> None:
    """Issue deprecation warning for old API usage."""
    warnings.warn(
        f"{old_name} is deprecated and will be removed in v3.0. Use {new_name} instead.",
        DeprecationWarning,
        stacklevel=3,
    )


# Type aliases for backward compatibility
TMeltanoTapConfig = FlextMeltanoConfig
TMeltanoTargetConfig = FlextMeltanoConfig
TMeltanoDbtConfig = FlextMeltanoConfig
FlextMeltanoTapBase = FlextMeltanoTapService
FlextMeltanoTargetBase = FlextMeltanoTargetService
FlextMeltanoDbtBase = FlextMeltanoDbtService

# Legacy aliases
FlextMeltanoTap = FlextMeltanoTapService
FlextMeltanoTarget = FlextMeltanoTargetService
FlextMeltanoDbt = FlextMeltanoDbtService
create_tap = create_meltano_tap_service
create_target = create_meltano_target_service
create_dbt_service = create_meltano_dbt_service


# Legacy factory functions
def flext_meltano_create_dbt_project(
    project_dir: Path,
) -> FlextResult[FlextMeltanoDbtService]:
    """Create DBT project using new base implementation."""
    _deprecated_api_warning("flext_meltano_create_dbt_project", "create_dbt_service")
    config = FlextMeltanoConfig(project_root=str(project_dir))
    return create_dbt_service(config)


def flext_meltano_create_dbt_runner(
    project_dir: Path,
) -> FlextResult[FlextMeltanoDbtService]:
    """Create DBT runner using new base implementation."""
    _deprecated_api_warning("flext_meltano_create_dbt_runner", "create_dbt_service")
    config = FlextMeltanoConfig(project_root=str(project_dir))
    return create_dbt_service(config)


# Version information
__version__ = "2.0.0-enterprise"

# === PUBLIC API ===
__all__ = [
    "AdapterRequiredConfig",
    "AdapterResponse",
    "BaseConnectionManager",
    # DBT Integration
    "BaseRelation",
    "BatchSink",
    "Connection",
    "ConnectionState",
    "Credentials",
    "DbtDatabaseError",
    "DbtRunResult",
    "DbtRuntimeError",
    # Core Services
    "FlextMeltanoBaseService",
    # CLI Interface
    "FlextMeltanoCli",
    "FlextMeltanoConfig",
    "FlextMeltanoDbt",
    "FlextMeltanoDbtBase",
    "FlextMeltanoDbtService",
    # Discovery
    "FlextMeltanoDiscoverer",
    "FlextMeltanoEvent",
    "FlextMeltanoExecutionCommand",
    "FlextMeltanoExecutionContext",
    # Execution
    "FlextMeltanoExecutor",
    "FlextMeltanoExtensionService",
    "FlextMeltanoInstallationContext",
    # Installation
    "FlextMeltanoInstaller",
    "FlextMeltanoPlugin",
    "FlextMeltanoPluginInfo",
    "FlextMeltanoResult",
    "FlextMeltanoTap",
    "FlextMeltanoTapBase",
    "FlextMeltanoTapService",
    "FlextMeltanoTarget",
    "FlextMeltanoTargetBase",
    "FlextMeltanoTargetService",
    "FlextMeltanoValidationResult",
    # Validation
    "FlextMeltanoValidationService",
    # Meltano Core
    "MeltanoCoreProject",
    "OAuthAuthenticator",
    "PropertiesList",
    "Property",
    "SQLAdapter",
    "SQLSink",
    "Sink",
    # Singer SDK re-exports
    "Stream",
    "TMeltanoDbtConfig",
    # Legacy Compatibility
    "TMeltanoTapConfig",
    "TMeltanoTargetConfig",
    "Tap",
    "Target",
    # Version
    "__version__",
    "create_dbt_service",
    "create_discoverer",
    "create_executor",
    "create_installer_service",
    "create_meltano_dbt_service",
    "create_meltano_extension_service",
    # Factory Functions
    "create_meltano_tap_service",
    "create_meltano_target_service",
    "create_tap",
    "create_target",
    "create_validation_service",
    "flext_meltano_create_dbt_project",
    "flext_meltano_create_dbt_runner",
    "flext_meltano_discover_catalog",
    "flext_meltano_discover_plugins",
    "flext_meltano_execute_job",
    "flext_meltano_install_plugin",
    "flext_meltano_run_cli",
    "flext_meltano_run_command",
    "flext_meltano_test_tap_connection",
    "flext_meltano_validate_project",
    "flext_meltano_validate_tap_config",
    "get_tap_test_class",
    "singer",
    "singer_typing",
    "validate_config_value",
    "validate_directory_path",
    "validate_file_path",
]

# Ensure singer module is available
