"""UNIFIED FLX MELTANO INTEGRATION - ZERO TOLERANCE CONSOLIDATION.

ARCHITECTURAL REVOLUTION: Single source of truth for ALL Meltano integration.
Eliminates scattered meltano implementations with unified, modern architecture.

CONSOLIDATES:
- infrastructure/meltano/ (ENTIRE DIRECTORY) - Infrastructure-level meltano support
- meltano/ (ENHANCED) - Domain-level meltano integration with enterprise patterns

ZERO TOLERANCE PRINCIPLES:
✅ Single import path for all Meltano operations
✅ Unified anti-corruption layer consolidating both implementations
✅ Modern Python 3.13 type system with ServiceResult patterns
✅ Strategic dependency injection integration
✅ Enterprise error handling and validation
✅ Domain-driven design patterns throughout

FEATURES: 1. Unified Anti-Corruption Layer (consolidates infrastructure + domain ACLs)
2. Enterprise project management with event publishing
3. Modern plugin management with type safety
4. State management with proper isolation
5. Configuration models with Pydantic validation
6. Pipeline orchestration with complexity-based execution
7. Job management with enterprise patterns
"""

__version__ = "0.1.0"

# UNIFIED IMPORTS - Single source of truth for all Meltano operations
from flx_meltano.event_bridge import MeltanoEventBridge
from flx_meltano.job_manager import FlxMeltanoJobManager
from flx_meltano.models import (
    MeltanoEnvironment,
    MeltanoJob,
    MeltanoPlugin,
    MeltanoPlugins,
    MeltanoProjectConfig,
    MeltanoSchedule,
)
from flx_meltano.orchestrator import FlxMeltanoOrchestrator
from flx_meltano.project_manager import FlxMeltanoProjectManager, MeltanoProjectManager
from flx_meltano.state_manager import FlxMeltanoStateManager
from flx_meltano.unified_anti_corruption_layer import (
    MeltanoPluginDescriptor,
    MeltanoRunResult,
    UnifiedMeltanoAntiCorruptionLayer,
)

# Note: FlxMeltanoSDK is defined in sdk.py as individual exception classes

# BACKWARD COMPATIBILITY ALIASES - For existing code migration
MeltanoAntiCorruptionLayer = UnifiedMeltanoAntiCorruptionLayer

# Export unified interface
__all__ = [
    "FlxMeltanoJobManager",
    "FlxMeltanoOrchestrator",
    # CORE MANAGERS
    "FlxMeltanoProjectManager",
    "FlxMeltanoStateManager",
    "MeltanoAntiCorruptionLayer",  # Backward compatibility
    "MeltanoEnvironment",
    # INTEGRATION COMPONENTS
    "MeltanoEventBridge",
    "MeltanoJob",
    # CONFIGURATION MODELS
    "MeltanoPlugin",
    "MeltanoPluginDescriptor",
    "MeltanoPlugins",
    "MeltanoProjectConfig",
    "MeltanoProjectManager",
    "MeltanoRunResult",
    "MeltanoSchedule",
    # UNIFIED ANTI-CORRUPTION LAYER
    "UnifiedMeltanoAntiCorruptionLayer",
]
