"""Enterprise data pipeline orchestration bridge for FLEXT ecosystem."""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING

from flext_meltano import singer


# === CORE BASE CLASSES ===
# === OPTIONAL IMPORTS ===
# Singer SDK integration - required dependency
# === SINGER BASE CLASSES - Proper location in flext-meltano ===
# Import Singer exceptions from flext-core (removes singer_base.py duplication)
from flext_meltano.exceptions import (
    FlextMeltanoAuthenticationError,
    FlextMeltanoAuthenticationError as FlextSingerAuthenticationError,
    FlextMeltanoConfigurationError,
    FlextMeltanoConfigurationError as FlextSingerConfigurationError,
    FlextMeltanoConnectionError,
    FlextMeltanoConnectionError as FlextSingerConnectionError,
    FlextMeltanoDBTError,
    FlextMeltanoError,
    FlextMeltanoError as FlextSingerError,
    FlextMeltanoExecutionError,
    FlextMeltanoPluginError,
    FlextMeltanoProcessingError,
    FlextMeltanoProcessingError as FlextSingerProcessingError,
    FlextMeltanoSingerError,
    FlextMeltanoTimeoutError,
    FlextMeltanoValidationError,
    FlextMeltanoValidationError as FlextSingerValidationError,
)
from singer_sdk import Stream, Tap, Target, typing as singer_typing
from singer_sdk.authenticators import OAuthAuthenticator
from singer_sdk.sinks import BatchSink, Sink, SQLSink
from singer_sdk.testing import get_tap_test_class
from singer_sdk.typing import PropertiesList, Property

from flext_meltano.base import (
    FlextMeltanoDbtService,
    FlextMeltanoExtensionService,
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
    create_meltano_dbt_service,
    create_meltano_extension_service,
    create_meltano_tap_service,
    create_meltano_target_service,
)
from flext_meltano.base_service import FlextMeltanoBaseService
from flext_meltano.models import FlextMeltanoEvent
from flext_meltano.config import FlextMeltanoConfig

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

# === DEPENDENCY INJECTION ===
from flext_meltano.container import (
    configure_meltano_container,
    configure_meltano_services,
    get_meltano_container,
)

# === DBT HUB INTEGRATION ===
from flext_meltano.dbt_hub import FlextDbtHub, create_dbt_hub
from flext_meltano.dbt_executor import (
    FlextDbtInMemoryExecutor,
    create_in_memory_executor,
)
from flext_meltano.dbt_manager import (
    FlextDbtPackage,
    FlextDbtPackageManager,
    create_package_manager,
)
from flext_meltano.dbt_registry import (
    FlextDbtModel,
    FlextDbtModelRegistry,
    create_model_registry,
)

# === DISCOVERY & CATALOG MANAGEMENT ===
from flext_meltano.discovery import (
    FlextMeltanoDiscoverer,
    create_discoverer,
)

# === EXECUTION HELPERS ===
from flext_meltano.execution import (
    FlextMeltanoExecutionCommand,
    FlextMeltanoExecutionContext,
    FlextMeltanoExecutor,
    create_executor,
)

# === LEGACY COMPATIBILITY ===
# Re-export legacy-compatible API implemented in modern modules
from flext_meltano.execution import (
    FlextMeltanoResult,
    flext_meltano_execute_job,
    flext_meltano_run_command,
)
from flext_meltano.discovery import (
    flext_meltano_discover_catalog,
    flext_meltano_discover_plugins,
)
from flext_meltano.validation import (
    flext_meltano_test_tap_connection,
    flext_meltano_validate_project,
    flext_meltano_validate_tap_config,
)
from flext_meltano.installation import flext_meltano_install_plugin

# === INSTALLATION & PLUGIN MANAGEMENT ===
from flext_meltano.installation import (
    FlextMeltanoInstallationContext,
    FlextMeltanoInstaller,
    create_installer_service,
)

# === PLUGIN IMPLEMENTATION ===
from flext_meltano.plugin_implementation import (
    FlextMeltanoPlugin,
    FlextMeltanoPluginContext,
    FlextMeltanoTapPlugin,
    FlextMeltanoTargetPlugin,
    create_meltano_tap_plugin,
    create_meltano_target_plugin,
)

# Centralized plugin info schema
from flext_meltano.common_schemas import FlextMeltanoPluginInfo

# === BRIDGE INTEGRATION ===
from flext_meltano.simple_bridge import (
    FlextMeltanoBridge,
    create_flext_meltano_bridge,
)

# === SINGER UNIFIED INTERFACE - Central Simplification Hub ===
from flext_meltano.singer_unified import (
    FlextSingerUnifiedConfig,
    FlextSingerUnifiedInterface,
    FlextSingerUnifiedResult,
    FlextSingerUnifiedService,
    create_unified_singer_config,
    create_unified_singer_service,
)

# === VALIDATION & TESTING ===
from flext_meltano.validation import (
    FlextMeltanoValidationResult,
    FlextMeltanoValidationService,
    create_validation_service,
)

if TYPE_CHECKING:
    from flext_core import FlextResult
    from pathlib import Path

# DBT run result - simplified for compatibility
type DbtRunResult = object


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
__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# === PUBLIC API ===
__all__: list[str] = [
    "BatchSink",
    # DBT Hub Integration
    "FlextDbtHub",
    "FlextDbtInMemoryExecutor",
    "FlextDbtModel",
    "FlextDbtModelRegistry",
    "FlextDbtPackage",
    "FlextDbtPackageManager",
    "FlextMeltanoBaseService",
    "FlextMeltanoBridge",
    "FlextMeltanoCli",
    "FlextMeltanoConfig",
    "FlextMeltanoDbt",
    "FlextMeltanoDbtBase",
    "FlextMeltanoDbtService",
    "FlextMeltanoDiscoverer",
    "FlextMeltanoEvent",
    "FlextMeltanoExecutionCommand",
    "FlextMeltanoExecutionContext",
    "FlextMeltanoExecutor",
    "FlextMeltanoExtensionService",
    "FlextMeltanoInstallationContext",
    "FlextMeltanoInstaller",
    "FlextMeltanoPlugin",
    "FlextMeltanoPluginContext",
    "FlextMeltanoPluginInfo",
    "FlextMeltanoPluginRegistry",
    "FlextMeltanoResult",
    "FlextMeltanoTap",
    "FlextMeltanoTapBase",
    "FlextMeltanoTapPlugin",
    "FlextMeltanoTapService",
    "FlextMeltanoTarget",
    "FlextMeltanoTargetBase",
    "FlextMeltanoTargetPlugin",
    "FlextMeltanoTargetService",
    "FlextMeltanoValidationResult",
    "FlextMeltanoValidationService",
    "FlextMeltanoAuthenticationError",
    "FlextMeltanoConnectionError",
    "FlextMeltanoDBTError",
    "FlextMeltanoError",
    "FlextMeltanoExecutionError",
    "FlextMeltanoPluginError",
    "FlextMeltanoProcessingError",
    "FlextMeltanoSingerError",
    "FlextMeltanoTimeoutError",
    "FlextMeltanoValidationError",
    "FlextSingerAuthenticationError",
    "FlextSingerConfigurationError",
    "FlextSingerConnectionError",
    "FlextSingerError",
    "FlextSingerProcessingError",
    "FlextSingerUnifiedConfig",
    "FlextSingerUnifiedInterface",
    "FlextSingerUnifiedResult",
    "FlextSingerUnifiedService",
    "FlextSingerValidationError",
    "OAuthAuthenticator",
    "PropertiesList",
    "Property",
    "SQLSink",
    "Sink",
    "Stream",
    "TMeltanoDbtConfig",
    "TMeltanoTapConfig",
    "TMeltanoTargetConfig",
    "Tap",
    "Target",
    "__version__",
    "__version_info__",
    "configure_meltano_container",
    "configure_meltano_services",
    "create_dbt_hub",
    "create_dbt_service",
    "create_discoverer",
    "create_executor",
    "create_flext_meltano_bridge",
    "create_in_memory_executor",
    "create_installer_service",
    "create_meltano_dbt_service",
    "create_meltano_extension_service",
    "create_meltano_tap_plugin",
    "create_meltano_tap_service",
    "create_meltano_target_plugin",
    "create_meltano_target_service",
    "create_model_registry",
    "create_package_manager",
    "create_tap",
    "create_target",
    "create_unified_singer_config",
    "create_unified_singer_service",
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
    "get_meltano_container",
    "get_tap_test_class",
    "singer",
    "singer_typing",
    "validate_config_value",
    "validate_directory_path",
    "validate_file_path",
]

# Ensure singer module is available
