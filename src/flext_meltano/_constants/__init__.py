# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._constants.base import FlextMeltanoConstantsBase
    from flext_meltano._constants.enums import FlextMeltanoConstantsEnums
    from flext_meltano._constants.settings import FlextMeltanoConstantsSettings


__all__: tuple[str, ...] = (
    "FlextMeltanoConstantsBase",
    "FlextMeltanoConstantsEnums",
    "FlextMeltanoConstantsSettings",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextMeltanoConstantsBase": ".base",
        "FlextMeltanoConstantsEnums": ".enums",
        "FlextMeltanoConstantsSettings": ".settings",
    }),
    public_exports=__all__,
)
