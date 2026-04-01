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
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_meltano.singer.catalog import *
    from flext_meltano.singer.sdk import *
    from flext_meltano.singer.service import *
    from flext_meltano.singer.state import *
    from flext_meltano.singer.tap import *
    from flext_meltano.singer.tap_source import *
    from flext_meltano.singer.target import *
    from flext_meltano.singer.translator import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextMeltanoCatalogManager": "flext_meltano.singer.catalog",
    "FlextMeltanoSingerCliTranslator": "flext_meltano.singer.translator",
    "FlextMeltanoSingerContext": "flext_meltano.singer.sdk",
    "FlextMeltanoSingerRecord": "flext_meltano.singer.sdk",
    "FlextMeltanoSingerService": "flext_meltano.singer.service",
    "FlextMeltanoSingerSinkBase": "flext_meltano.singer.sdk",
    "FlextMeltanoSingerStreamBase": "flext_meltano.singer.sdk",
    "FlextMeltanoSingerTapBase": "flext_meltano.singer.sdk",
    "FlextMeltanoSingerTargetBase": "flext_meltano.singer.sdk",
    "FlextMeltanoStateManager": "flext_meltano.singer.state",
    "FlextMeltanoTapAbstractions": "flext_meltano.singer.tap",
    "FlextMeltanoTapSourceMixin": "flext_meltano.singer.tap_source",
    "FlextMeltanoTargetAbstractions": "flext_meltano.singer.target",
    "catalog": "flext_meltano.singer.catalog",
    "sdk": "flext_meltano.singer.sdk",
    "service": "flext_meltano.singer.service",
    "state": "flext_meltano.singer.state",
    "tap": "flext_meltano.singer.tap",
    "tap_source": "flext_meltano.singer.tap_source",
    "target": "flext_meltano.singer.target",
    "translator": "flext_meltano.singer.translator",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
