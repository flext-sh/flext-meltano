"""Deprecated Components - BACKWARD COMPATIBILITY LAYER.

⚠️  DEPRECATION NOTICE: Components in this module are deprecated and will be removed.

This module provides backward compatibility for the old flext-meltano API.
All components here issue deprecation warnings and redirect to the new semantic architecture.

🚨 MIGRATION GUIDE:
Old Import → New Import
- from flext_meltano import FlextMeltanoProjectManager → from flext_meltano.application.services import FlextMeltanoProjectService
- from flext_meltano import FlextMeltanoOrchestrator → from flext_meltano.application.services import FlextMeltanoJobService
- from flext_meltano import MeltanoAntiCorruptionLayer → from flext_meltano.application.services import FlextMeltanoProjectService

Built on flext-core foundation patterns.
"""

from __future__ import annotations

import warnings
from typing import Any

# Import available new implementations
from flext_meltano.application.services import (
    FlextMeltanoJobService,
    FlextMeltanoPluginService,
    FlextMeltanoProjectService,
    FlextMeltanoStateService,
)


# Deprecation warning helper
def _deprecation_warning(old_name: str, new_location: str) -> None:
    """Issue deprecation warning."""
    warnings.warn(
        f"{old_name} is deprecated. Use {new_location} instead.",
        DeprecationWarning,
        stacklevel=3
    )


# Deprecated class aliases with warnings
class FlextMeltanoProjectManager:
    """Deprecated project manager - use FlextMeltanoProjectService instead."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _deprecation_warning(
            "FlextMeltanoProjectManager",
            "flext_meltano.application.services.FlextMeltanoProjectService"
        )
        self._service = FlextMeltanoProjectService()

    def create_project(self, *args: Any, **kwargs: Any) -> None:
        """Deprecated method - raises NotImplementedError."""
        _deprecation_warning("create_project", "ProjectApplicationService.create_project")
        raise NotImplementedError("Please migrate to new ProjectApplicationService")

    def __getattr__(self, name: str) -> Any:
        return getattr(self._service, name)


class FlextMeltanoOrchestrator:
    """Deprecated orchestrator - use FlextMeltanoJobService instead."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _deprecation_warning(
            "FlextMeltanoOrchestrator",
            "flext_meltano.application.services.FlextMeltanoJobService"
        )
        self._service = FlextMeltanoJobService()

    def execute_pipeline(self, *args: Any, **kwargs: Any) -> None:
        """Deprecated method - raises NotImplementedError."""
        _deprecation_warning("execute_pipeline", "PipelineOrchestrator.execute_pipeline")
        raise NotImplementedError("Please migrate to new PipelineOrchestrator")

    def __getattr__(self, name: str) -> Any:
        return getattr(self._service, name)


class FlextMeltanoAntiCorruptionLayer:
    """Deprecated anti-corruption layer - use services directly."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        _deprecation_warning(
            "FlextMeltanoAntiCorruptionLayer",
            "flext_meltano.application.services (direct service usage)"
        )
        self.project_service = FlextMeltanoProjectService()
        self.job_service = FlextMeltanoJobService()
        self.plugin_service = FlextMeltanoPluginService()
        self.state_service = FlextMeltanoStateService()

    def run_meltano_command(self, *args: Any, **kwargs: Any) -> None:
        """Deprecated method - raises NotImplementedError."""
        _deprecation_warning("run_meltano_command", "MeltanoCLIAdapter")
        raise NotImplementedError("Please migrate to new MeltanoCLIAdapter")

    def __getattr__(self, name: str) -> Any:
        # Try to find the attribute in available services
        for service in [self.project_service, self.job_service, self.plugin_service, self.state_service]:
            if hasattr(service, name):
                return getattr(service, name)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


# Export deprecated classes
__all__ = [
    "FlextMeltanoAntiCorruptionLayer",
    "FlextMeltanoOrchestrator",
    "FlextMeltanoProjectManager",
    "_deprecation_warning",
]
