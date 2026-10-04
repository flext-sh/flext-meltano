# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from examples.constants import ExamplesFlextMeltanoConstants, c
    from examples.models import ExamplesFlextMeltanoModels, m
    from examples.protocols import ExamplesFlextMeltanoProtocols, p
    from examples.typings import ExamplesFlextMeltanoTypes, t
    from examples.utilities import ExamplesFlextMeltanoUtilities, u
    from flext_meltano import d, e, h, r, s, x


__all__: tuple[str, ...] = (
    "ExamplesFlextMeltanoConstants",
    "ExamplesFlextMeltanoModels",
    "ExamplesFlextMeltanoProtocols",
    "ExamplesFlextMeltanoTypes",
    "ExamplesFlextMeltanoUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".constants": ("ExamplesFlextMeltanoConstants", "c"),
            ".models": ("ExamplesFlextMeltanoModels", "m"),
            ".protocols": ("ExamplesFlextMeltanoProtocols", "p"),
            ".typings": ("ExamplesFlextMeltanoTypes", "t"),
            ".utilities": ("ExamplesFlextMeltanoUtilities", "u"),
            "flext_meltano": ("d", "e", "h", "r", "s", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
