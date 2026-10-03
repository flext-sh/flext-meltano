# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, d, e, h, r, td, tf, tk, tm, x

    from tests import integration, unit
    from tests.base import TestsFlextMeltanoServiceBase, s
    from tests.constants import TestsFlextMeltanoConstants, c
    from tests.models import TestsFlextMeltanoModels, m
    from tests.protocols import TestsFlextMeltanoProtocols, p
    from tests.settings import TestsFlextMeltanoSettings
    from tests.typings import TestsFlextMeltanoTypes, t
    from tests.utilities import TestsFlextMeltanoUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextMeltanoConstants",
    "TestsFlextMeltanoModels",
    "TestsFlextMeltanoProtocols",
    "TestsFlextMeltanoServiceBase",
    "TestsFlextMeltanoSettings",
    "TestsFlextMeltanoTypes",
    "TestsFlextMeltanoUtilities",
    "api",
    "c",
    "d",
    "e",
    "h",
    "integration",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextMeltanoServiceBase", "s"),
            ".constants": ("TestsFlextMeltanoConstants", "c"),
            ".integration": ("integration",),
            ".models": ("TestsFlextMeltanoModels", "m"),
            ".protocols": ("TestsFlextMeltanoProtocols", "p"),
            ".settings": ("TestsFlextMeltanoSettings",),
            ".typings": ("TestsFlextMeltanoTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextMeltanoUtilities", "u"),
            "flext_tests": ("api", "d", "e", "h", "r", "td", "tf", "tk", "tm", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
