"""FLEXT Meltano state management module.

This module provides state management functionality for FLEXT Meltano,
including state persistence, retrieval, and lifecycle management.
"""

from __future__ import annotations

from flext_meltano.state.manager import FlextMeltanoStateManager
from flext_meltano.state.models import FlextMeltanoState

__all__ = [
    "FlextMeltanoState",
    "FlextMeltanoStateManager",
]
