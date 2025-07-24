"""FlextMeltano Project Module.

Project domain models and services following Clean Architecture patterns.
"""

from flext_meltano.project.manager import FlextMeltanoProjectManager
from flext_meltano.project.models import FlextMeltanoProject

__all__ = [
    "FlextMeltanoProject",
    "FlextMeltanoProjectManager",
]
