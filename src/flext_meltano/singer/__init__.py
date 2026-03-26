# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Singer Protocol Implementation for FLEXT Meltano.

This module provides deep integration with singer-sdk following the Singer
specification with FLEXT ecosystem patterns and railway-oriented programming.

NOTE: Heavy modules (service, tap, target) are NOT imported at package level
to avoid circular imports. Import them explicitly when needed:
    from flext_meltano.singer.service import FlextMeltanoSingerService
    from flext_meltano.singer.tap import FlextMeltanoTapAbstractions

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_meltano.singer.catalog import FlextMeltanoCatalogManager
    from flext_meltano.singer.service import FlextMeltanoSingerService
    from flext_meltano.singer.state import FlextMeltanoStateManager
    from flext_meltano.singer.tap import FlextMeltanoTapAbstractions
    from flext_meltano.singer.target import FlextMeltanoTargetAbstractions
    from flext_meltano.singer.translator import FlextMeltanoSingerCliTranslator

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoCatalogManager": ["flext_meltano.singer.catalog", "FlextMeltanoCatalogManager"],
    "FlextMeltanoSingerCliTranslator": ["flext_meltano.singer.translator", "FlextMeltanoSingerCliTranslator"],
    "FlextMeltanoSingerService": ["flext_meltano.singer.service", "FlextMeltanoSingerService"],
    "FlextMeltanoStateManager": ["flext_meltano.singer.state", "FlextMeltanoStateManager"],
    "FlextMeltanoTapAbstractions": ["flext_meltano.singer.tap", "FlextMeltanoTapAbstractions"],
    "FlextMeltanoTargetAbstractions": ["flext_meltano.singer.target", "FlextMeltanoTargetAbstractions"],
}

__all__ = [
    "FlextMeltanoCatalogManager",
    "FlextMeltanoSingerCliTranslator",
    "FlextMeltanoSingerService",
    "FlextMeltanoStateManager",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTargetAbstractions",
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
