"""FLEXT Meltano - Enterprise Meltano integration with simplified imports.

🎯 SIMPLE IMPORTS - Use these for ALL new code:

# Core entities (direct access)
from flext_meltano import MeltanoProject, MeltanoState, MeltanoJob, MeltanoPlugin

# Services (simplified names)
from flext_meltano import ProjectService, StateService, JobService, PluginService

# Configuration and types
from flext_meltano import EnvironmentType, JobStatus, PluginType, ServiceResult

🚨 DEPRECATED LONG PATHS (still work, but discouraged):
❌ from flext_meltano.application.services.project_service import ProjectApplicationService
✅ from flext_meltano import ProjectService

❌ from flext_meltano.domain.entities.project import MeltanoProject
✅ from flext_meltano import MeltanoProject

❌ from flext_meltano.application.services.state_service import MeltanoStateService
✅ from flext_meltano import StateService

🔄 MIGRATION STRATEGY:
All complex paths show warnings pointing to simple root-level imports.
Use short, direct imports for maximum productivity and clarity.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any

# Import deprecation warning from flext-core
from flext_core import FlextDeprecationWarning
from flext_core.domain.shared_types import ServiceResult

# Import all real implementations - NO FALLBACKS
from flext_meltano.application.services.job_service import (
    MeltanoJobService,
)
from flext_meltano.application.services.plugin_service import (
    MeltanoPluginService,
)
from flext_meltano.application.services.project_service import (
    ProjectApplicationService,
)
from flext_meltano.application.services.state_service import (
    MeltanoStateService,
)
from flext_meltano.domain.entities import (
    EnvironmentType,
    JobStatus,
    PluginType,
)
from flext_meltano.domain.entities.job import MeltanoJob
from flext_meltano.domain.entities.plugin import MeltanoPlugin
from flext_meltano.domain.entities.project import MeltanoProject
from flext_meltano.domain.entities.state import MeltanoState
from flext_meltano.unified_anti_corruption_layer import (
    UnifiedMeltanoAntiCorruptionLayer,
)

__version__ = "0.7.0"

# ============================================================================
# 🎯 SIMPLIFIED PUBLIC API - Direct imports without complex paths
# ============================================================================

# Create simple aliases for direct access
ProjectService = ProjectApplicationService
StateService = MeltanoStateService
JobService = MeltanoJobService
PluginService = MeltanoPluginService


def _warn_deprecated_import(
    old_path: str,
    new_import: str,
    removal_version: str = "v0.8.0",
) -> None:
    """Issue comprehensive deprecation warning with clear migration path."""
    warnings.warn(
        f"\n\n🚨 DEPRECATED COMPLEX PATH:\n"
        f"Using '{old_path}' is deprecated.\n\n"
        f"🎯 SIMPLE IMPORT SOLUTION:\n"
        f"Use: from flext_meltano import {new_import}\n\n"
        f"💡 PRODUCTIVITY TIP:\n"
        f"All FLEXT Meltano imports are now available at root level!\n"
        f"No more complex nested paths - just import what you need directly.\n\n"
        f"🔄 MIGRATION:\n"
        f"Support for complex paths will be removed in {removal_version}.\n"
        f"Use simple root-level imports for better developer experience.\n\n"
        f"Examples:\n"
        f"✅ from flext_meltano import ProjectService, StateService, JobService\n"
        f"✅ from flext_meltano import MeltanoProject, MeltanoJob, MeltanoPlugin\n"
        f"✅ from flext_meltano import JobStatus, PluginType, EnvironmentType",
        category=FlextDeprecationWarning,
        stacklevel=3,
    )


# ============================================================================
# ⚠️ DEPRECATED COMPATIBILITY - Will show helpful warnings
# ============================================================================


def __getattr__(name: str) -> Any:
    """Handle legacy imports with detailed deprecation guidance."""
    # Legacy import mappings
    legacy_mappings = {
        # Core service classes
        "ProjectApplicationService": {
            "new_import": "ProjectService",
            "component": ProjectService,
            "reason": "Simplified to ProjectService at root level",
        },
        "MeltanoStateService": {
            "new_import": "StateService",
            "component": StateService,
            "reason": "Simplified to StateService at root level",
        },
        "MeltanoJobService": {
            "new_import": "JobService",
            "component": JobService,
            "reason": "Simplified to JobService at root level",
        },
        "MeltanoPluginService": {
            "new_import": "PluginService",
            "component": PluginService,
            "reason": "Simplified to PluginService at root level",
        },
        # Legacy manager classes
        "MeltanoProjectManager": {
            "new_import": "ProjectService",
            "component": ProjectService,
            "reason": "Renamed to ProjectService following Clean Architecture",
        },
        "FlextMeltanoProjectManager": {
            "new_import": "ProjectService",
            "component": ProjectService,
            "reason": "Renamed to ProjectService following Clean Architecture",
        },
    }

    if name in legacy_mappings:
        mapping = legacy_mappings[name]

        # Show clear guidance for migration
        _warn_deprecated_import(f"flext_meltano.{name}", str(mapping["new_import"]))

        return mapping["component"]

    msg = f"module 'flext_meltano' has no attribute '{name}'"
    raise AttributeError(msg)


# ============================================================================
# 📦 PUBLIC API EXPORTS
# ============================================================================

__all__ = [
    # Enums and Value Objects (configuration types)
    "EnvironmentType",  # from flext_meltano import EnvironmentType
    "FlextMeltanoProjectManager",  # ⚠️ Deprecated → Use ProjectService
    "JobService",  # from flext_meltano import JobService
    "JobStatus",  # from flext_meltano import JobStatus
    "MeltanoJob",  # from flext_meltano import MeltanoJob
    "MeltanoJobService",  # ⚠️ Deprecated → Use JobService
    "MeltanoPlugin",  # from flext_meltano import MeltanoPlugin
    "MeltanoPluginService",  # ⚠️ Deprecated → Use PluginService
    # ✅ RECOMMENDED - SIMPLE DIRECT IMPORTS
    # Core Domain Entities (data models)
    "MeltanoProject",  # from flext_meltano import MeltanoProject
    # Legacy manager classes
    "MeltanoProjectManager",  # ⚠️ Deprecated → Use ProjectService
    "MeltanoState",  # from flext_meltano import MeltanoState
    "MeltanoStateService",  # ⚠️ Deprecated → Use StateService
    "PluginService",  # from flext_meltano import PluginService
    "PluginType",  # from flext_meltano import PluginType
    # ⚠️ DEPRECATED - LEGACY COMPATIBILITY (will show warnings)
    # Legacy service names (redirect to simplified versions)
    "ProjectApplicationService",  # ⚠️ Deprecated → Use ProjectService
    # Application Services (business logic)
    "ProjectService",  # from flext_meltano import ProjectService
    # Shared Utilities (from flext-core)
    "ServiceResult",  # from flext_meltano import ServiceResult
    "StateService",  # from flext_meltano import StateService
    # Anti-corruption layer
    "UnifiedMeltanoAntiCorruptionLayer",  # from flext_meltano import UnifiedMeltanoAntiCorruptionLayer
    # Metadata
    "__version__",  # Package version
]
