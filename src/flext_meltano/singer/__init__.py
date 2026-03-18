# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
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

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_meltano.singer.catalog import FlextMeltanoCatalogManager
    from flext_meltano.singer.protocols import (
        FlextMeltanoPluginProtocols,
        FlextMeltanoPluginProtocols as p,
        FlextMeltanoSingerProtocols,
    )
    from flext_meltano.singer.service import (
        FlextMeltanoSingerService,
        FlextMeltanoSingerService as s,
    )
    from flext_meltano.singer.state import FlextMeltanoStateManager
    from flext_meltano.singer.tap import FlextMeltanoTapAbstractions
    from flext_meltano.singer.target import FlextMeltanoTargetAbstractions
    from flext_meltano.singer.translator import FlextMeltanoSingerCliTranslator

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextMeltanoCatalogManager": ("flext_meltano.singer.catalog", "FlextMeltanoCatalogManager"),
    "FlextMeltanoPluginProtocols": ("flext_meltano.singer.protocols", "FlextMeltanoPluginProtocols"),
    "FlextMeltanoSingerCliTranslator": ("flext_meltano.singer.translator", "FlextMeltanoSingerCliTranslator"),
    "FlextMeltanoSingerProtocols": ("flext_meltano.singer.protocols", "FlextMeltanoSingerProtocols"),
    "FlextMeltanoSingerService": ("flext_meltano.singer.service", "FlextMeltanoSingerService"),
    "FlextMeltanoStateManager": ("flext_meltano.singer.state", "FlextMeltanoStateManager"),
    "FlextMeltanoTapAbstractions": ("flext_meltano.singer.tap", "FlextMeltanoTapAbstractions"),
    "FlextMeltanoTargetAbstractions": ("flext_meltano.singer.target", "FlextMeltanoTargetAbstractions"),
    "p": ("flext_meltano.singer.protocols", "FlextMeltanoPluginProtocols"),
    "s": ("flext_meltano.singer.service", "FlextMeltanoSingerService"),
}

__all__ = [
    "FlextMeltanoCatalogManager",
    "FlextMeltanoPluginProtocols",
    "FlextMeltanoSingerCliTranslator",
    "FlextMeltanoSingerProtocols",
    "FlextMeltanoSingerService",
    "FlextMeltanoStateManager",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTargetAbstractions",
    "p",
    "s",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
