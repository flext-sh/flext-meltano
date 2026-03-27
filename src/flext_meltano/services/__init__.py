# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano Services - Service mixins for the Meltano facade.

This package contains service mixin classes that compose via MRO
to form the FlextMeltano public facade in api.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_meltano.services.abstractions import FlextMeltanoAbstractions
    from flext_meltano.services.adapters import FlextMeltanoAdapter
    from flext_meltano.services.bridge import FlextMeltanoBridge
    from flext_meltano.services.cli import FlextMeltanoCLI, main
    from flext_meltano.services.cli_managers import (
        FlextMeltanoCommandRouter,
        FlextMeltanoDbtManager,
        FlextMeltanoPipelineManager,
        FlextMeltanoPluginManager,
        FlextMeltanoSingerManager,
        FlextMeltanoStatusManager,
    )
    from flext_meltano.services.executor import FlextMeltanoExecutor
    from flext_meltano.services.file_managers import FlextMeltanoFileManagers
    from flext_meltano.services.library_runner import FlextMeltanoLibraryRunner
    from flext_meltano.services.project_service import FlextMeltanoProjectService
    from flext_meltano.services.services import FlextMeltanoService
    from flext_meltano.services.validators import FlextMeltanoValidators

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoAbstractions": [
        "flext_meltano.services.abstractions",
        "FlextMeltanoAbstractions",
    ],
    "FlextMeltanoAdapter": ["flext_meltano.services.adapters", "FlextMeltanoAdapter"],
    "FlextMeltanoBridge": ["flext_meltano.services.bridge", "FlextMeltanoBridge"],
    "FlextMeltanoCLI": ["flext_meltano.services.cli", "FlextMeltanoCLI"],
    "FlextMeltanoCommandRouter": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoCommandRouter",
    ],
    "FlextMeltanoDbtManager": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoDbtManager",
    ],
    "FlextMeltanoExecutor": ["flext_meltano.services.executor", "FlextMeltanoExecutor"],
    "FlextMeltanoFileManagers": [
        "flext_meltano.services.file_managers",
        "FlextMeltanoFileManagers",
    ],
    "FlextMeltanoLibraryRunner": [
        "flext_meltano.services.library_runner",
        "FlextMeltanoLibraryRunner",
    ],
    "FlextMeltanoPipelineManager": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoPipelineManager",
    ],
    "FlextMeltanoPluginManager": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoPluginManager",
    ],
    "FlextMeltanoProjectService": [
        "flext_meltano.services.project_service",
        "FlextMeltanoProjectService",
    ],
    "FlextMeltanoService": ["flext_meltano.services.services", "FlextMeltanoService"],
    "FlextMeltanoSingerManager": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoSingerManager",
    ],
    "FlextMeltanoStatusManager": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoStatusManager",
    ],
    "FlextMeltanoValidators": [
        "flext_meltano.services.validators",
        "FlextMeltanoValidators",
    ],
    "main": ["flext_meltano.services.cli", "main"],
}

__all__ = [
    "FlextMeltanoAbstractions",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCLI",
    "FlextMeltanoCommandRouter",
    "FlextMeltanoDbtManager",
    "FlextMeltanoExecutor",
    "FlextMeltanoFileManagers",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoPipelineManager",
    "FlextMeltanoPluginManager",
    "FlextMeltanoProjectService",
    "FlextMeltanoService",
    "FlextMeltanoSingerManager",
    "FlextMeltanoStatusManager",
    "FlextMeltanoValidators",
    "main",
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
