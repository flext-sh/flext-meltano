"""Application Interfaces - NEW SEMANTIC ARCHITECTURE.

Interfaces that define contracts between application and infrastructure layers.
Built on flext-core foundation patterns.
"""

from __future__ import annotations

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
# Initialize types via DI container
# External service interfaces
from flext_meltano.application.interfaces.external_services import (
    EventPublisher,
    MeltanoCLIService,
    NotificationService,
)

# Repository interfaces
from flext_meltano.application.interfaces.repositories import (
    JobRepository,
    PluginRepository,
    ProjectRepository,
    StateRepository,
)

__all__ = [
    # Foundation patterns
    "AbstractRepository",
    # External service interfaces
    "EventPublisher",
    # Repository interfaces
    "JobRepository",
    "MeltanoCLIService",
    "NotificationService",
    "PluginRepository",
    "ProjectRepository",
    "StateRepository",
]
