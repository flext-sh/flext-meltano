# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from enum import StrEnum, unique
    from pathlib import Path
    from typing import TYPE_CHECKING, Final

    from flext_tests import FlextTestsConstants, d, e, h, r, td, tf, tk, tm, tv, x

    from . import integration as integration, unit as unit
    from .base import TestsFlextMeltanoServiceBase, TestsFlextMeltanoServiceBase as s
    from .constants import TestsFlextMeltanoConstants, TestsFlextMeltanoConstants as c
    from .models import TestsFlextMeltanoModels, TestsFlextMeltanoModels as m
    from .protocols import TestsFlextMeltanoProtocols, TestsFlextMeltanoProtocols as p
    from .settings import TestsFlextMeltanoSettings
    from .typings import TestsFlextMeltanoTypes, TestsFlextMeltanoTypes as t
    from .utilities import TestsFlextMeltanoUtilities, TestsFlextMeltanoUtilities as u
__all__: tuple[str, ...] = (
    "TYPE_CHECKING",
    "Final",
    "FlextTestsConstants",
    "MappingProxyType",
    "Path",
    "StrEnum",
    "TestsFlextMeltanoConstants",
    "TestsFlextMeltanoModels",
    "TestsFlextMeltanoProtocols",
    "TestsFlextMeltanoServiceBase",
    "TestsFlextMeltanoSettings",
    "TestsFlextMeltanoTypes",
    "TestsFlextMeltanoUtilities",
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
    "tv",
    "u",
    "unique",
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
            "enum": ("StrEnum", "unique"),
            "flext_tests": (
                "FlextTestsConstants",
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
            "pathlib": ("Path",),
            "types": ("MappingProxyType",),
            "typing": ("Final", "TYPE_CHECKING"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
