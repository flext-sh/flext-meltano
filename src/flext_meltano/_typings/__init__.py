# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Typings package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._typings.base import FlextMeltanoTypingsBase
    from flext_meltano._typings.domains import FlextMeltanoTypingsDomains
    from flext_meltano._typings.singer import FlextMeltanoTypingsSinger


__all__: tuple[str, ...] = (
    "FlextMeltanoTypingsBase",
    "FlextMeltanoTypingsDomains",
    "FlextMeltanoTypingsSinger",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextMeltanoTypingsBase": ".base",
        "FlextMeltanoTypingsDomains": ".domains",
        "FlextMeltanoTypingsSinger": ".singer",
    }),
    public_exports=__all__,
)
