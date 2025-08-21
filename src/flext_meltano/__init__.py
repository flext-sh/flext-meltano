"""FLEXT Meltano - Enterprise wrapper for Meltano/Singer SDK/DBT.

Provides 3 core functions:
1. **Wrapper**: Adapts Meltano/Singer SDK/DBT APIs to flext-core patterns
2. **Runtime**: Go bridge execution for Meltano/DBT commands  
3. **Base Components**: Base classes for flext-(dbt|tap|target) projects

**Real Native Integration**: Uses installed Meltano 3.9.1, DBT Core 1.10.5, Singer SDK 0.48.0
**No subprocess calls** - Pure Python API integration
"""

from __future__ import annotations

# === FUNÇÃO 1: WRAPPERS FOR EXTERNAL LIBRARIES ===
# Direct integration with real installed libraries
from singer_sdk import Stream, Tap, Target, typing as singer_typing
from singer_sdk.authenticators import OAuthAuthenticator
from singer_sdk.sinks import BatchSink, Sink, SQLSink
from singer_sdk.testing import get_tap_test_class
from singer_sdk.typing import PropertiesList, Property

# Wrapper modules adapting APIs to flext-core patterns
from .meltano_wrapper import MeltanoBridge, FlextMeltanoAdapter
from .dbt_wrapper import MeltanoDbtWrapper, FlextDbtAdapter
from .singer_wrapper import MeltanoSingerWrapper, FlextSingerAdapter

# === FUNÇÃO 2: RUNTIME EXECUTION VIA GO BRIDGE ===
from .runtime import FlextMeltanoExecutor, FlextExecutionResult
from .go_bridge import FlextMeltanoBridge
from .cli import FlextMeltanoCli

# === FUNÇÃO 3: BASE COMPONENTS FOR FLEXT-* PROJECTS ===
from .base_services import (
    FlextMeltanoTapService,
    FlextMeltanoTargetService, 
    FlextMeltanoDbtService,
)
from .base_plugins import (
    FlextTapPlugin,
    FlextTargetPlugin,
    FlextDbtPlugin,
)

# Core utilities and configuration
from .base import FlextMeltanoConfig, FlextMeltanoTap, FlextMeltanoTarget
from .exceptions import FlextMeltanoError
from .constants import FLEXT_MELTANO_VERSION

# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    # === FUNÇÃO 1: WRAPPERS ===
    # Singer SDK re-exports (direct from installed library)
    "Stream", "Tap", "Target", "singer_typing",
    "OAuthAuthenticator", "BatchSink", "Sink", "SQLSink",
    "get_tap_test_class", "PropertiesList", "Property",
    
    # Native API Wrappers
    "MeltanoBridge", "FlextMeltanoAdapter",           # Meltano Core wrapper
    "MeltanoDbtWrapper", "FlextDbtAdapter",          # DBT Core wrapper
    "MeltanoSingerWrapper", "FlextSingerAdapter",    # Singer SDK wrapper
    
    # === FUNÇÃO 2: RUNTIME GO BRIDGE ===
    "FlextMeltanoExecutor", "FlextExecutionResult",   # Runtime execution
    "FlextMeltanoBridge",                             # Go bridge JSON API
    "FlextMeltanoCli",                                # CLI interface
    
    # === FUNÇÃO 3: BASE COMPONENTS ===
    "FlextMeltanoTapService",                         # Base for flext-tap-*
    "FlextMeltanoTargetService",                      # Base for flext-target-*
    "FlextMeltanoDbtService",                         # Base for flext-dbt-*
    "FlextTapPlugin", "FlextTargetPlugin", "FlextDbtPlugin", # Plugin interfaces
    
    # === CORE UTILITIES ===
    "FlextMeltanoConfig", "FlextMeltanoTap", "FlextMeltanoTarget",
    "FlextMeltanoError", "FLEXT_MELTANO_VERSION",
]

# Version info
__version__ = "2.0.0-enterprise"