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

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_meltano.meltano.bridge import FlextMeltanoBridge
    from flext_meltano.meltano.pipelines import FlextMeltanoOrchestrationService
    from flext_meltano.meltano.plugins import FlextMeltanoComponentService
    from flext_meltano.meltano.project import FlextMeltanoProjectManager
    from flext_meltano.meltano.runner import (
        FlextMeltanoDbtTransformationRunner,
        FlextMeltanoLibraryRunner,
    )
    from flext_meltano.meltano.service import FlextMeltanoMeltanoService

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoBridge": ["flext_meltano.meltano.bridge", "FlextMeltanoBridge"],
    "FlextMeltanoComponentService": ["flext_meltano.meltano.plugins", "FlextMeltanoComponentService"],
    "FlextMeltanoDbtTransformationRunner": ["flext_meltano.meltano.runner", "FlextMeltanoDbtTransformationRunner"],
    "FlextMeltanoLibraryRunner": ["flext_meltano.meltano.runner", "FlextMeltanoLibraryRunner"],
    "FlextMeltanoMeltanoService": ["flext_meltano.meltano.service", "FlextMeltanoMeltanoService"],
    "FlextMeltanoOrchestrationService": ["flext_meltano.meltano.pipelines", "FlextMeltanoOrchestrationService"],
    "FlextMeltanoProjectManager": ["flext_meltano.meltano.project", "FlextMeltanoProjectManager"],
}

__all__ = [
    "FlextMeltanoBridge",
    "FlextMeltanoComponentService",
    "FlextMeltanoDbtTransformationRunner",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoMeltanoService",
    "FlextMeltanoOrchestrationService",
    "FlextMeltanoProjectManager",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
