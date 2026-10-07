# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._utilities.base import FlextMeltanoUtilitiesBase
    from flext_meltano._utilities.runtime import FlextMeltanoUtilitiesRuntime
    from flext_meltano._utilities.singer import FlextMeltanoUtilitiesSinger


__all__: tuple[str, ...] = (
    "FlextMeltanoUtilitiesBase",
    "FlextMeltanoUtilitiesRuntime",
    "FlextMeltanoUtilitiesSinger",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextMeltanoUtilitiesBase": ".base",
        "FlextMeltanoUtilitiesRuntime": ".runtime",
        "FlextMeltanoUtilitiesSinger": ".singer",
    }),
    public_exports=__all__,
)
