"""Application Services - NEW SEMANTIC ARCHITECTURE.

Built on flext-core foundation patterns.
"""

from __future__ import annotations

from flext_meltano.application.services.job_service import MeltanoJobService
from flext_meltano.application.services.plugin_service import MeltanoPluginService
from flext_meltano.application.services.project_service import ProjectApplicationService
from flext_meltano.application.services.project_service_alias import (
    MeltanoProjectService,
)
from flext_meltano.application.services.state_service import MeltanoStateService

__all__ = [
    "MeltanoJobService",
    "MeltanoPluginService",
    "MeltanoProjectService",
    "MeltanoStateService",
    "ProjectApplicationService",
]
