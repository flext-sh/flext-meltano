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

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.singer import (
        catalog as catalog,
        sdk as sdk,
        service as service,
        state as state,
        tap as tap,
        tap_source as tap_source,
        target as target,
        translator as translator,
    )
    from flext_meltano.singer.catalog import (
        FlextMeltanoCatalogManager as FlextMeltanoCatalogManager,
    )
    from flext_meltano.singer.sdk import (
        FlextMeltanoSingerContext as FlextMeltanoSingerContext,
        FlextMeltanoSingerRecord as FlextMeltanoSingerRecord,
        FlextMeltanoSingerSinkBase as FlextMeltanoSingerSinkBase,
        FlextMeltanoSingerStreamBase as FlextMeltanoSingerStreamBase,
        FlextMeltanoSingerTapBase as FlextMeltanoSingerTapBase,
        FlextMeltanoSingerTargetBase as FlextMeltanoSingerTargetBase,
    )
    from flext_meltano.singer.service import (
        FlextMeltanoSingerService as FlextMeltanoSingerService,
    )
    from flext_meltano.singer.state import (
        FlextMeltanoStateManager as FlextMeltanoStateManager,
    )
    from flext_meltano.singer.tap import (
        FlextMeltanoTapAbstractions as FlextMeltanoTapAbstractions,
    )
    from flext_meltano.singer.tap_source import (
        FlextMeltanoTapSourceMixin as FlextMeltanoTapSourceMixin,
    )
    from flext_meltano.singer.target import (
        FlextMeltanoTargetAbstractions as FlextMeltanoTargetAbstractions,
    )
    from flext_meltano.singer.translator import (
        FlextMeltanoSingerCliTranslator as FlextMeltanoSingerCliTranslator,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoCatalogManager": [
        "flext_meltano.singer.catalog",
        "FlextMeltanoCatalogManager",
    ],
    "FlextMeltanoSingerCliTranslator": [
        "flext_meltano.singer.translator",
        "FlextMeltanoSingerCliTranslator",
    ],
    "FlextMeltanoSingerContext": [
        "flext_meltano.singer.sdk",
        "FlextMeltanoSingerContext",
    ],
    "FlextMeltanoSingerRecord": [
        "flext_meltano.singer.sdk",
        "FlextMeltanoSingerRecord",
    ],
    "FlextMeltanoSingerService": [
        "flext_meltano.singer.service",
        "FlextMeltanoSingerService",
    ],
    "FlextMeltanoSingerSinkBase": [
        "flext_meltano.singer.sdk",
        "FlextMeltanoSingerSinkBase",
    ],
    "FlextMeltanoSingerStreamBase": [
        "flext_meltano.singer.sdk",
        "FlextMeltanoSingerStreamBase",
    ],
    "FlextMeltanoSingerTapBase": [
        "flext_meltano.singer.sdk",
        "FlextMeltanoSingerTapBase",
    ],
    "FlextMeltanoSingerTargetBase": [
        "flext_meltano.singer.sdk",
        "FlextMeltanoSingerTargetBase",
    ],
    "FlextMeltanoStateManager": [
        "flext_meltano.singer.state",
        "FlextMeltanoStateManager",
    ],
    "FlextMeltanoTapAbstractions": [
        "flext_meltano.singer.tap",
        "FlextMeltanoTapAbstractions",
    ],
    "FlextMeltanoTapSourceMixin": [
        "flext_meltano.singer.tap_source",
        "FlextMeltanoTapSourceMixin",
    ],
    "FlextMeltanoTargetAbstractions": [
        "flext_meltano.singer.target",
        "FlextMeltanoTargetAbstractions",
    ],
    "catalog": ["flext_meltano.singer.catalog", ""],
    "sdk": ["flext_meltano.singer.sdk", ""],
    "service": ["flext_meltano.singer.service", ""],
    "state": ["flext_meltano.singer.state", ""],
    "tap": ["flext_meltano.singer.tap", ""],
    "tap_source": ["flext_meltano.singer.tap_source", ""],
    "target": ["flext_meltano.singer.target", ""],
    "translator": ["flext_meltano.singer.translator", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextMeltanoCatalogManager",
    "FlextMeltanoSingerCliTranslator",
    "FlextMeltanoSingerContext",
    "FlextMeltanoSingerRecord",
    "FlextMeltanoSingerService",
    "FlextMeltanoSingerSinkBase",
    "FlextMeltanoSingerStreamBase",
    "FlextMeltanoSingerTapBase",
    "FlextMeltanoSingerTargetBase",
    "FlextMeltanoStateManager",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTapSourceMixin",
    "FlextMeltanoTargetAbstractions",
    "catalog",
    "sdk",
    "service",
    "state",
    "tap",
    "tap_source",
    "target",
    "translator",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
