"""UNIFIED FLEXT MELTANO INTEGRATION - ZERO TOLERANCE CONSOLIDATION.

Copyright (c) 2025 FLEXT Team. All rights reserved.

ARCHITECTURAL REVOLUTION: Single source of truth for ALL Meltano integration.
Eliminates scattered meltano implementations with unified, modern architecture.

CONSOLIDATES:
            - infrastructure/meltano/ (ENTIRE DIRECTORY) - Infrastructure-level
            meltano support
- meltano/ (ENHANCED) - Domain-level meltano integration with enterprise patterns

ZERO TOLERANCE PRINCIPLES:
✅ Single import path for all Meltano operations
✅ Unified anti-corruption layer consolidating both implementations
✅ Modern Python 3.13 type system with ServiceResult patterns
✅ Strategic dependency injection integration
✅ Enterprise error handling and validation
✅ Domain-driven design patterns throughout

FEATURES:
            1. Unified Anti-Corruption Layer (consolidates infrastructure + domain ACLs)
2. Enterprise project management with event publishing
3. Modern plugin management with type safety
4. State management with proper isolation
5. Configuration models with Pydantic validation
6. Pipeline orchestration with complexity-based execution
7. Job management with enterprise patterns
"""

from __future__ import annotations

from flext_core.domain.types import ServiceResult

# FLEXT-Meltano: Core imports and version management
from flext_meltano.event_bridge import MeltanoEventBridge

# Integration modules
from flext_meltano.integrations import GopyIntegration, MeltanoBridge
from flext_meltano.job_manager import FlextMeltanoJobManager
from flext_meltano.models import (
    MeltanoEnvironment,
    MeltanoJob,
    MeltanoPlugin,
    MeltanoPlugins,
    MeltanoProjectConfig,
    MeltanoSchedule,
)
from flext_meltano.orchestrator import FlextMeltanoOrchestrator
from flext_meltano.project_manager import MeltanoProjectManager
from flext_meltano.state_manager import FlextMeltanoStateManager
from flext_meltano.unified_anti_corruption_layer import (
    MeltanoPluginDescriptor,
    MeltanoRunResult,
    UnifiedMeltanoAntiCorruptionLayer,
)

try:
    from flext_core.domain.constants import FlextFramework

    __version__ = FlextFramework.VERSION
except ImportError:
    __version__ = "0.7.0"

# Backward compatibility
FlextMeltanoProjectManager = MeltanoProjectManager
MeltanoAntiCorruptionLayer = UnifiedMeltanoAntiCorruptionLayer

# Export unified interface
__all__ = [
    "FlextMeltanoJobManager",
    "FlextMeltanoOrchestrator",
    # CORE MANAGERS
    "FlextMeltanoProjectManager",
    "FlextMeltanoStateManager",
    "GopyIntegration",
    "MeltanoAntiCorruptionLayer",  # Backward compatibility
    # INTEGRATION MODULES
    "MeltanoBridge",
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
