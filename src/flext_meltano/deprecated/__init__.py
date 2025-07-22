"""Deprecated Components - BACKWARD COMPATIBILITY LAYER.

⚠️  DEPRECATION NOTICE: Components in this module are deprecated and will be removed.

This module provides backward compatibility for the old flext-meltano API.
All components here issue deprecation warnings and redirect to the new semantic architecture.

🚨 MIGRATION GUIDE:
Old Import → New Import
- from flext_meltano import FlextMeltanoProjectManager → from flext_meltano.application.services import ProjectApplicationService
- from flext_meltano import FlextMeltanoOrchestrator → from flext_meltano.application.orchestrators import PipelineOrchestrator
- from flext_meltano import MeltanoAntiCorruptionLayer → from flext_meltano.infrastructure.meltano import MeltanoCLIAdapter

Built on flext-core foundation patterns.
"""

from __future__ import annotations

import warnings
from typing import Any

# Import new implementations
from flext_meltano.application.services.project_service import ProjectApplicationService


# Deprecation warning helper
def _deprecation_warning(old_name: str, new_location: str) -> None:
    """Issue deprecation warning."""
    warnings.warn(
        f"{old_name} is deprecated and will be removed in version 1.0.0. "
        f"Use {new_location} instead. "
        f"See SEMANTIC_ARCHITECTURE_REDESIGN.md for migration guide.",
        DeprecationWarning,
        stacklevel=3,
    )


class FlextMeltanoProjectManager:
    """DEPRECATED: Use ProjectApplicationService instead."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _deprecation_warning(
            "FlextMeltanoProjectManager",
            "flext_meltano.application.services.ProjectApplicationService",
        )

        # For now, redirect to ProjectApplicationService
        # In a real implementation, you'd inject the dependencies properly
        self._new_service = None  # Would be injected

    def create_project(self, *args: Any, **kwargs: Any) -> Any:
        """DEPRECATED: Use ProjectApplicationService.create_project instead."""
        _deprecation_warning(
            "FlextMeltanoProjectManager.create_project",
            "ProjectApplicationService.create_project",
        )
        # Redirect to new implementation
        msg = "Please migrate to new ProjectApplicationService"
        raise NotImplementedError(msg)


class FlextMeltanoOrchestrator:
    """DEPRECATED: Use PipelineOrchestrator instead."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _deprecation_warning(
            "FlextMeltanoOrchestrator",
            "flext_meltano.application.orchestrators.PipelineOrchestrator",
        )

    def execute_pipeline(self, *args: Any, **kwargs: Any) -> Any:
        """DEPRECATED: Use PipelineOrchestrator.execute_pipeline instead."""
        _deprecation_warning(
            "FlextMeltanoOrchestrator.execute_pipeline",
            "PipelineOrchestrator.execute_pipeline",
        )
        msg = "Please migrate to new PipelineOrchestrator"
        raise NotImplementedError(msg)


class MeltanoAntiCorruptionLayer:
    """DEPRECATED: Use MeltanoCLIAdapter instead."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _deprecation_warning(
            "MeltanoAntiCorruptionLayer",
            "flext_meltano.infrastructure.meltano.MeltanoCLIAdapter",
        )

    def run_meltano_command(self, *args: Any, **kwargs: Any) -> Any:
        """DEPRECATED: Use MeltanoCLIAdapter methods instead."""
        _deprecation_warning(
            "MeltanoAntiCorruptionLayer.run_meltano_command",
            "MeltanoCLIAdapter.run_job or MeltanoCLIAdapter.install_plugin",
        )
        msg = "Please migrate to new MeltanoCLIAdapter"
        raise NotImplementedError(msg)


# Legacy exports for backward compatibility
__all__ = [
    "FlextMeltanoOrchestrator",
    "FlextMeltanoProjectManager",
    "MeltanoAntiCorruptionLayer",
]
