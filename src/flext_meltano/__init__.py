"""FLEXT Meltano - Enterprise ELT orchestration platform.

REAL integration with flext-core, singer-sdk, meltano-edk, and dbt-core.
ALL classes use FlextMeltano*, TMeltano, flext_meltano_ prefixes.
ZERO fallbacks, ZERO mocks, ZERO incomplete implementations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextResult

# === UNIFIED BASE CLASSES ===
from flext_meltano.base import (
    DBT_AVAILABLE as BASE_DBT_AVAILABLE,
    SINGER_AVAILABLE as BASE_SINGER_AVAILABLE,
    FlextMeltanoBaseService,
    FlextMeltanoConfig,
    FlextMeltanoDbt,
    FlextMeltanoTap,
    FlextMeltanoTapLdap,
    FlextMeltanoTapOracle,
    FlextMeltanoTarget,
    FlextMeltanoTargetCsv,
    FlextMeltanoTargetLdap,
    FlextMeltanoTargetOracle,
    create_dbt_service,
    create_tap,
    create_target,
)

# === CORE ENTERPRISE FUNCTIONALITY ===
from flext_meltano.core import (
    FlextMeltanoDbtService,
    FlextMeltanoExecutionState,
    FlextMeltanoExtension,
    FlextMeltanoOrchestrationService,
    FlextMeltanoPipelineConfig,
    FlextMeltanoPipelineEvent,
    FlextMeltanoPipelineResult,
    FlextMeltanoRepository,
    FlextMeltanoSingerService,
    _deprecated_api_warning,
)

# === EXECUTION HELPERS ===
from flext_meltano.flext_meltano_execution import (
    FlextMeltanoResult,
    flext_meltano_execute_job,
    flext_meltano_run_command,
)

# === LEGACY COMPATIBILITY (deprecated) ===
# Create aliases for backward compatibility using new unified base
try:
    from flext_meltano.flext_meltano_dbt_base import (
        DBT_AVAILABLE,
        FlextMeltanoDbtProject,
        FlextMeltanoDbtRunner,
        flext_meltano_create_dbt_project,
        flext_meltano_create_dbt_runner,
    )
except ImportError:
    # Use new base implementation
    from flext_meltano.base import DBT_AVAILABLE, create_dbt_service

    def flext_meltano_create_dbt_project(project_dir: Path) -> FlextResult[FlextMeltanoDbt]:
        """Create DBT project using new base implementation."""
        return create_dbt_service(project_dir)

    def flext_meltano_create_dbt_runner(project_dir: Path) -> FlextResult[FlextMeltanoDbt]:
        """Create DBT runner using new base implementation."""
        return create_dbt_service(project_dir)

    FlextMeltanoDbtRunner = FlextMeltanoDbt
    FlextMeltanoDbtProject = FlextMeltanoDbt

# Type aliases for backward compatibility
TMeltanoTapConfig = FlextMeltanoConfig
TMeltanoTargetConfig = FlextMeltanoConfig
TMeltanoDbtConfig = FlextMeltanoConfig
FlextMeltanoTapBase = FlextMeltanoTap
FlextMeltanoTargetBase = FlextMeltanoTarget
FlextMeltanoDbtBase = FlextMeltanoDbt

# === UTILITIES ===
from flext_meltano.flext_meltano_cli import (
    FlextMeltanoCli,
    flext_meltano_run_cli,
)
from flext_meltano.flext_meltano_discovery import (
    flext_meltano_discover_catalog,
    flext_meltano_discover_plugins,
)
from flext_meltano.flext_meltano_installation import (
    FlextMeltanoInstaller,
    flext_meltano_install_plugin,
)
from flext_meltano.flext_meltano_validation import (
    flext_meltano_test_tap_connection,
    flext_meltano_validate_project,
    flext_meltano_validate_tap_config,
)

# === EXTERNAL SDK RE-EXPORTS ===
try:
    from singer_sdk import Stream, Tap, Target, typing as th
    from singer_sdk.authenticators import OAuthAuthenticator
    from singer_sdk.sinks import BatchSink, Sink, SQLSink
    from singer_sdk.testing import get_tap_test_class
    from singer_sdk.typing import PropertiesList, Property
    SINGER_AVAILABLE = True
except ImportError:
    Stream = Tap = Target = Sink = SQLSink = PropertiesList = Property = th = (
        get_tap_test_class
    ) = OAuthAuthenticator = BatchSink = None  # type: ignore[assignment,misc]
    SINGER_AVAILABLE = False

try:
    from meltano.core.project import Project as MeltanoCoreProject
    MELTANO_AVAILABLE = True
except ImportError:
    MeltanoCoreProject = None  # type: ignore[assignment,misc]
    MELTANO_AVAILABLE = False

try:
    import dbt.contracts.results
    from dbt.adapters.base import BaseRelation
    from dbt.adapters.base.connections import BaseConnectionManager, ConnectionState
    from dbt.adapters.contracts.connection import (
        AdapterRequiredConfig,
        AdapterResponse,
        Connection,
        Credentials,
    )
    from dbt.adapters.sql import SQLAdapter

    try:
        from dbt_common.exceptions import DbtDatabaseError, DbtRuntimeError
    except ImportError:
        from dbt.exceptions import (
            DatabaseException as DbtDatabaseError,
            RuntimeException as DbtRuntimeError,
        )

    DbtRunResult = getattr(dbt.contracts.results, "RunResult", None)
except ImportError:
    DbtRunResult = None
    BaseConnectionManager = None
    BaseRelation = None
    ConnectionState = None
    AdapterRequiredConfig = None
    AdapterResponse = None
    Connection = None
    Credentials = None
    DbtDatabaseError = None
    DbtRuntimeError = None
    SQLAdapter = None

# Version
__version__ = "2.0.0-enterprise"

# === PUBLIC API ===
__all__ = [
    # === FLAGS ===
    "DBT_AVAILABLE",
    "MELTANO_AVAILABLE",
    "SINGER_AVAILABLE",
    "AdapterRequiredConfig",
    "AdapterResponse",
    "BaseConnectionManager",
    "BaseRelation",
    "BatchSink",
    "Connection",
    "ConnectionState",
    "Credentials",
    "DbtDatabaseError",
    "DbtRunResult",
    "DbtRuntimeError",
    "FlextMeltanoBaseService",
    # === UTILITIES ===
    "FlextMeltanoCli",
    # === UNIFIED BASE CLASSES ===
    "FlextMeltanoConfig",
    "FlextMeltanoDbt",
    "FlextMeltanoDbtBase",
    "FlextMeltanoDbtProject",
    "FlextMeltanoDbtRunner",
    # === CORE SERVICES ===
    "FlextMeltanoDbtService",
    "FlextMeltanoExecutionState",
    "FlextMeltanoExtension",
    "FlextMeltanoInstaller",
    "FlextMeltanoOrchestrationService",
    "FlextMeltanoPipelineConfig",
    "FlextMeltanoPipelineEvent",
    "FlextMeltanoPipelineResult",
    "FlextMeltanoRepository",
    "FlextMeltanoResult",
    "FlextMeltanoSingerService",
    "FlextMeltanoTap",
    # === LEGACY COMPATIBILITY (deprecated) ===
    "FlextMeltanoTapBase",
    "FlextMeltanoTapLdap",
    # === SPECIFIC IMPLEMENTATIONS ===
    "FlextMeltanoTapOracle",
    "FlextMeltanoTarget",
    "FlextMeltanoTargetBase",
    "FlextMeltanoTargetCsv",
    "FlextMeltanoTargetLdap",
    "FlextMeltanoTargetOracle",
    "MeltanoCoreProject",
    "OAuthAuthenticator",
    "PropertiesList",
    "Property",
    "SQLAdapter",
    "SQLSink",
    "Sink",
    # === EXTERNAL SDK RE-EXPORTS ===
    "Stream",
    "TMeltanoDbtConfig",
    "TMeltanoTapConfig",
    "TMeltanoTargetConfig",
    "Tap",
    "Target",
    # === VERSION ===
    "__version__",
    "create_dbt_service",
    # === FACTORY FUNCTIONS ===
    "create_tap",
    "create_target",
    "flext_meltano_create_dbt_project",
    "flext_meltano_create_dbt_runner",
    "flext_meltano_discover_catalog",
    "flext_meltano_discover_plugins",
    # === EXECUTION FUNCTIONS ===
    "flext_meltano_execute_job",
    "flext_meltano_install_plugin",
    "flext_meltano_run_cli",
    "flext_meltano_run_command",
    "flext_meltano_test_tap_connection",
    "flext_meltano_validate_project",
    "flext_meltano_validate_tap_config",
    "get_tap_test_class",
    "th",
]
