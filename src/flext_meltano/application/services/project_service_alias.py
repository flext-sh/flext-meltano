"""Project Service Alias - NEW SEMANTIC ARCHITECTURE.

Alias MeltanoProjectService to ProjectApplicationService for backward compatibility.
"""

from __future__ import annotations

from flext_meltano.application.services.project_service import ProjectApplicationService

# Alias for backward compatibility
MeltanoProjectService = ProjectApplicationService
