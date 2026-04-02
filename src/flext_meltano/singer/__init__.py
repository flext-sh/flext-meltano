# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Singer SDK type aliases for consumer subclassing.

This package provides ONLY Singer SDK re-exports (Tap, Target, Stream, Sink).
All service logic lives in ``flext_meltano.services.singer_*`` modules.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_meltano.singer import sdk
    from flext_meltano.singer.sdk import (
        FlextMeltanoSingerContext,
        FlextMeltanoSingerRecord,
        FlextMeltanoSingerSinkBase,
        FlextMeltanoSingerStreamBase,
        FlextMeltanoSingerTapBase,
        FlextMeltanoSingerTargetBase,
    )

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextMeltanoSingerContext": "flext_meltano.singer.sdk",
    "FlextMeltanoSingerRecord": "flext_meltano.singer.sdk",
    "FlextMeltanoSingerSinkBase": "flext_meltano.singer.sdk",
    "FlextMeltanoSingerStreamBase": "flext_meltano.singer.sdk",
    "FlextMeltanoSingerTapBase": "flext_meltano.singer.sdk",
    "FlextMeltanoSingerTargetBase": "flext_meltano.singer.sdk",
    "sdk": "flext_meltano.singer.sdk",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
