"""FLEXT Meltano - Enterprise wrapper for Meltano/Singer SDK/DBT.

Provides 3 core functions:
1. **Wrapper**: Adapts Meltano/Singer SDK/DBT APIs to flext-core patterns
2. **Runtime**: Go bridge execution for Meltano/DBT commands  
3. **Base Components**: Base classes for flext-(dbt|tap|target) projects

**Real Native Integration**: Uses installed Meltano 3.9.1, DBT Core 1.10.5, Singer SDK 0.48.0
**No subprocess calls** - Pure Python API integration
**FlextResult patterns** - Railway-oriented programming with .unwrap_or()
"""

from __future__ import annotations

# === SINGER SDK RE-EXPORTS (FUNÇÃO 1) ===
# Direct integration with real installed Singer SDK 0.48.0
from singer_sdk import Stream, Tap, Target, typing as singer_typing
from singer_sdk.authenticators import OAuthAuthenticator  
from singer_sdk.sinks import BatchSink, Sink, SQLSink
from singer_sdk.testing import get_tap_test_class
from singer_sdk.typing import PropertiesList, Property

# === FUNÇÃO 1: WRAPPERS FOR EXTERNAL LIBRARIES ===
# Wrapper modules adapting APIs to flext-core patterns
from .wrapper_meltano import MeltanoBridge, FlextMeltanoAdapter
from .wrapper_dbt import MeltanoDbtWrapper, FlextDbtAdapter  
from .wrapper_singer import MeltanoSingerWrapper, FlextSingerAdapter

# === FUNÇÃO 2: RUNTIME EXECUTION VIA GO BRIDGE ===
from .runtime_executor import FlextMeltanoExecutor, FlextExecutionResult
from .runtime_bridge import FlextMeltanoBridge
from .runtime_meltano_real import MeltanoEltExecutor, execute_real_elt_pipeline
from .runtime_dbt_real import DbtRealExecutor, execute_real_dbt_workflow

# === FUNÇÃO 3: BASE COMPONENTS FOR FLEXT-* PROJECTS ===
from .base_flext_services import (
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
    FlextMeltanoDbtService,
)
from .base_flext_plugins import (
    FlextTapPlugin,
    FlextTargetPlugin,
    FlextDbtPlugin,
)

# === UTILITIES AND CORE ===
from .utilities import (
    FlextMeltanoUtilities,
    FlextResultHelpers,
    FlextTypeAdapters,
    FlextWrapperUtilities,
    FlextRuntimeUtilities, 
    FlextBaseUtilities
)
from .base_flext_projects import FlextMeltanoConfig, FlextMeltanoTap, FlextMeltanoTarget
from .exceptions import FlextMeltanoError
from .constants import FLEXT_MELTANO_VERSION
from .cli import FlextMeltanoCli

# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    # === SINGER SDK DIRECT INTEGRATION ===
    "Stream", "Tap", "Target", "singer_typing",
    "OAuthAuthenticator", "BatchSink", "Sink", "SQLSink", 
    "get_tap_test_class", "PropertiesList", "Property",
    
    # === FUNÇÃO 1: WRAPPERS PARA BIBLIOTECAS ===
    "MeltanoBridge", "FlextMeltanoAdapter",        # Meltano Core 3.9.1
    "MeltanoDbtWrapper", "FlextDbtAdapter",        # DBT Core 1.10.5
    "MeltanoSingerWrapper", "FlextSingerAdapter",  # Singer SDK 0.48.0
    
    # === FUNÇÃO 2: RUNTIME GO BRIDGE ===
    "FlextMeltanoExecutor", "FlextExecutionResult",     # Runtime base
    "FlextMeltanoBridge",                               # Go bridge JSON API
    "MeltanoEltExecutor", "execute_real_elt_pipeline",  # Real Meltano ELT
    "DbtRealExecutor", "execute_real_dbt_workflow",     # Real DBT execution
    
    # === FUNÇÃO 3: BASE PARA PROJETOS FLEXT-* ===
    "FlextMeltanoTapService",      # Base para flext-tap-*
    "FlextMeltanoTargetService",   # Base para flext-target-*  
    "FlextMeltanoDbtService",      # Base para flext-dbt-*
    "FlextTapPlugin", "FlextTargetPlugin", "FlextDbtPlugin",
    
    # === UTILITIES ===
    "FlextMeltanoUtilities",       # Utilidades gerais
    "FlextResultHelpers",          # Helpers para FlextResult
    "FlextTypeAdapters",           # Adaptadores de tipos
    "FlextWrapperUtilities",       # Específicas para wrappers
    "FlextRuntimeUtilities",       # Específicas para runtime  
    "FlextBaseUtilities",          # Específicas para base projects
    
    # === CORE ===
    "FlextMeltanoConfig", "FlextMeltanoTap", "FlextMeltanoTarget",
    "FlextMeltanoError", "FLEXT_MELTANO_VERSION", "FlextMeltanoCli"
]

# Version info
__version__ = "2.0.0-enterprise"