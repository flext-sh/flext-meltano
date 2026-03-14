# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Meltano Integration for FLEXT Ecosystem.

This module provides deep integration with meltano-sdk for project management,
plugin operations, and pipeline orchestration with FLEXT ecosystem patterns
and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_meltano.meltano.bridge import FlextMeltanoBridge
    from flext_meltano.meltano.pipelines import (
        FlextMeltanoOrchestrationService,
        FlextMeltanoOrchestrationService as s,
    )
    from flext_meltano.meltano.plugins import FlextMeltanoComponentService
    from flext_meltano.meltano.project import FlextMeltanoProjectManager
    from flext_meltano.meltano.runner import FlextMeltanoLibraryRunner
    from flext_meltano.meltano.service import FlextMeltanoMeltanoService

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextMeltanoBridge": ("flext_meltano.meltano.bridge", "FlextMeltanoBridge"),
    "FlextMeltanoComponentService": (
        "flext_meltano.meltano.plugins",
        "FlextMeltanoComponentService",
    ),
    "FlextMeltanoLibraryRunner": (
        "flext_meltano.meltano.runner",
        "FlextMeltanoLibraryRunner",
    ),
    "FlextMeltanoMeltanoService": (
        "flext_meltano.meltano.service",
        "FlextMeltanoMeltanoService",
    ),
    "FlextMeltanoOrchestrationService": (
        "flext_meltano.meltano.pipelines",
        "FlextMeltanoOrchestrationService",
    ),
    "FlextMeltanoProjectManager": (
        "flext_meltano.meltano.project",
        "FlextMeltanoProjectManager",
    ),
    "s": ("flext_meltano.meltano.pipelines", "FlextMeltanoOrchestrationService"),
}

__all__ = [
    "FlextMeltanoBridge",
    "FlextMeltanoComponentService",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoMeltanoService",
    "FlextMeltanoOrchestrationService",
    "FlextMeltanoProjectManager",
    "s",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
