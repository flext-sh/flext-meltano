# AUTO-GENERATED FILE — Regenerate with: make gen
"""Typings.meltano package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from typings.meltano import cli as cli, core as core


__all__: tuple[str, ...] = ("cli", "core")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({"cli": ".cli", "core": ".core"}),
    public_exports=__all__,
)
