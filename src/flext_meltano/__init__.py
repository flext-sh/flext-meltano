"""FLEXT Meltano - Enterprise wrapper for Meltano/Singer SDK/DBT.

Provides 3 core functions:
1. **Wrapper**: Adapts Meltano/Singer SDK/DBT APIs to flext-core patterns
2. **Runtime**: Go bridge execution for Meltano/DBT commands
3. **Base Components**: Base classes for flext-(dbt|tap|target) projects

**Real Native Integration**: Uses installed Meltano 3.9.1, DBT Core 1.10.5, Singer SDK 0.48.0
**No subprocess calls** - Pure Python API integration
**FlextResult patterns** - Railway-oriented programming with .value and .unwrap_or()
"""

from __future__ import annotations

# === SINGER SDK RE-EXPORTS (FUNÇÃO 1) ===
# Direct integration with real installed Singer SDK 0.48.0
from singer_sdk import Stream, Tap, Target, typing as singer_typing
from singer_sdk.authenticators import OAuthAuthenticator
from singer_sdk.sinks import BatchSink, Sink, SQLSink
from singer_sdk.testing import get_tap_test_class
from singer_sdk.typing import PropertiesList, Property

# === FUNÇÃO 1: BASE WRAPPERS FOR EXTERNAL LIBRARIES ===
# Base wrapper modules adapting APIs to flext-core patterns
from .meltano_adapters import MeltanoBridge, FlextMeltanoAdapter
from .dbt_adapters import MeltanoDbtWrapper, FlextDbtAdapter
from .singer_adapters import MeltanoSingerWrapper, FlextSingerAdapter

# === FUNÇÃO 2: EXECUTORS FOR GO BRIDGE INTEGRATION ===
from .executors_meltano import FlextMeltanoExecutor, FlextExecutionResult
from .executors_bridge import (
    FlextMeltanoBridge,
    create_flext_meltano_bridge,
)
from .executors_cli import FlextMeltanoCli, flext_meltano_run_cli

# === FUNÇÃO 3: SERVICE IMPLEMENTATIONS FOR FLEXT-* PROJECTS ===
from .service_implementations import (
    # Base service implementations (concrete classes using flext-core)
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
    FlextMeltanoDbtService,
    # Service protocols (typing.Protocol instead of @abstractmethod)
    TapServiceProtocol,
    TargetServiceProtocol,
    DbtServiceProtocol,
)
from .plugin_protocols import (
    FlextTapPlugin,
    FlextTargetPlugin,
    FlextDbtPlugin,
)

# === UTILITIES AND CORE ===
from .utilities import FlextMeltanoUtilities
from .validators import (
    validate_config_value_simple as validate_config_value,
    validate_directory_path,
    validate_file_path,
)
from .config import FlextMeltanoConfig, FLEXT_MELTANO_VERSION
from .exceptions import FlextMeltanoError

# === TYPES AND FILE MANAGEMENT ===
from .flext_types import FlextMeltanoTypes, ConfigDict
from .file_managers import FlextMeltanoFileManagers

# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    # === SINGER SDK DIRECT INTEGRATION ===
    "Stream",
    "Tap",
    "Target",
    "singer_typing",
    "OAuthAuthenticator",
    "BatchSink",
    "Sink",
    "SQLSink",
    "get_tap_test_class",
    "PropertiesList",
    "Property",
    # === FUNÇÃO 1: WRAPPERS PARA BIBLIOTECAS ===
    "MeltanoBridge",
    "FlextMeltanoAdapter",  # Meltano Core 3.9.1
    "MeltanoDbtWrapper",
    "FlextDbtAdapter",  # DBT Core 1.10.5
    "MeltanoSingerWrapper",
    "FlextSingerAdapter",  # Singer SDK 0.48.0
    # === FUNÇÃO 2: RUNTIME GO BRIDGE ===
    "FlextMeltanoExecutor",
    "FlextExecutionResult",  # Runtime base
    "FlextMeltanoBridge",  # Go bridge JSON API
    "create_flext_meltano_bridge",  # Bridge factory function
    "flext_meltano_run_cli",  # CLI factory function
    # === FUNÇÃO 3: BASE PARA PROJETOS FLEXT-* ===
    "FlextMeltanoTapService",  # Base para flext-tap-*
    "FlextMeltanoTargetService",  # Base para flext-target-*
    "FlextMeltanoDbtService",  # Base para flext-dbt-*
    "TapServiceProtocol",  # Service protocols
    "TargetServiceProtocol",
    "DbtServiceProtocol",
    "FlextTapPlugin",
    "FlextTargetPlugin",
    "FlextDbtPlugin",
    # === UTILITIES ===
    "FlextMeltanoUtilities",  # Utilidades gerais
    # === CORE ===
    "FlextMeltanoConfig",
    "FlextMeltanoError",
    "FLEXT_MELTANO_VERSION",
    "FlextMeltanoCli",
    # === TYPES AND FILE MANAGEMENT ===
    "FlextMeltanoTypes",  # Type definitions
    "ConfigDict",  # Configuration dictionary type
    "FlextMeltanoFileManagers",  # File management utilities
    # === VALIDATION FUNCTIONS ===
    "validate_config_value",
    "validate_directory_path",
    "validate_file_path",
]

# Version info
__version__ = "2.0.0-enterprise"
