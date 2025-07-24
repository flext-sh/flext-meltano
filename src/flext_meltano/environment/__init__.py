"""FLEXT Meltano environment management module.

This module provides environment management functionality for FLEXT Meltano,
including environment creation, configuration, and lifecycle management.
"""

from __future__ import annotations

from flext_meltano.environment.manager import FlextMeltanoEnvironmentManager
from flext_meltano.environment.models import FlextMeltanoEnvironment

__all__ = [
    "FlextMeltanoEnvironment",
    "FlextMeltanoEnvironmentManager",
]
