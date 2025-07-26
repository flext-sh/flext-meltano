"""FLEXT Meltano - Enterprise Meltano Integration.

Clean Meltano integration using flext-core patterns.
"""

from __future__ import annotations

# API components
from flext_meltano.api import (
    FlextMeltanoAPI,
    FlextMeltanoPipelineResult,
    discover_catalog,
    run_pipeline,
    test_connection,
)

# Common utilities
from flext_meltano.common import (
    ensure_directory,
    validate_directory_path,
    validate_file_path,
    validate_meltano_project,
    validate_plugin_config,
)

# Constants
from flext_meltano.constants import (
    FlextMeltanoConstants,
    MeltanoEnvironment,
    MeltanoLogLevel,
    MeltanoResultStatus,
)

# Core components
from flext_meltano.core import (
    FlextMeltanoDbtService,
    FlextMeltanoExtension,
    FlextMeltanoOrchestrationService,
    FlextMeltanoPipelineConfig,
    FlextMeltanoSingerService,
)

# Models
from flext_meltano.models import (
    FlextMeltanoEnvironment,
    FlextMeltanoJob,
    FlextMeltanoPlugin,
    FlextMeltanoPlugins,
    FlextMeltanoProjectConfig,
    FlextMeltanoSchedule,
)

# Bridge
from flext_meltano.simple_bridge import FlextMeltanoBridge

# Singer integration
from flext_meltano.singer import (
    SINGER_AVAILABLE,
    FlextSingerService,
    get_singer_service,
)

# Version
__version__ = "2.0.0"

# Public API
__all__ = [
    "SINGER_AVAILABLE",
    # API
    "FlextMeltanoAPI",
    # Bridge
    "FlextMeltanoBridge",
    # Constants
    "FlextMeltanoConstants",
    "FlextMeltanoDbtService",
    "FlextMeltanoEnvironment",
    "FlextMeltanoExtension",
    "FlextMeltanoJob",
    "FlextMeltanoOrchestrationService",
    "FlextMeltanoPipelineConfig",
    "FlextMeltanoPipelineResult",
    # Models
    "FlextMeltanoPlugin",
    "FlextMeltanoPlugins",
    "FlextMeltanoProjectConfig",
    "FlextMeltanoSchedule",
    # Core services
    "FlextMeltanoSingerService",
    # Singer
    "FlextSingerService",
    "MeltanoEnvironment",
    "MeltanoLogLevel",
    "MeltanoResultStatus",
    # Version
    "__version__",
    "discover_catalog",
    "ensure_directory",
    "get_singer_service",
    "run_pipeline",
    "test_connection",
    "validate_directory_path",
    # Utilities
    "validate_file_path",
    "validate_meltano_project",
    "validate_plugin_config",
]
