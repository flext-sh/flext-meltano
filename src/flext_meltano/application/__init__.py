"""Application layer for FLEXT-MELTANO v0.7.0.

REFACTORED:
            Using flext-core application patterns - NO duplication.
"""

from __future__ import annotations

from flext_meltano.application.services import (
    FlextMeltanoJobService,
    FlextMeltanoPluginService,
    FlextMeltanoProjectService,
    FlextMeltanoStateService,
)

# Aliases for backward compatibility
MeltanoJobService = FlextMeltanoJobService
MeltanoPluginService = FlextMeltanoPluginService
MeltanoProjectService = FlextMeltanoProjectService
MeltanoStateService = FlextMeltanoStateService
ProjectApplicationService = FlextMeltanoProjectService
FlextMeltanoProjectApplicationService = FlextMeltanoProjectService  # Legacy compatibility

__all__ = [
    "FlextMeltanoJobService",
    "FlextMeltanoPluginService",
    "FlextMeltanoProjectApplicationService",  # Legacy compatibility
    "FlextMeltanoProjectService",
    "FlextMeltanoStateService",
    "MeltanoJobService",
    "MeltanoPluginService",
    "MeltanoProjectService",
    "MeltanoStateService",
    "ProjectApplicationService",
]
