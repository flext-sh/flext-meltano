# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_tests import (
        d,
        e,
        h,
        r,
        reset_settings,
        s,
        settings,
        settings_factory,
        td,
        tf,
        tk,
        tm,
        tv,
        x,
    )

    from tests.constants import TestsFlextMeltanoConstants, c
    from tests.models import TestsFlextMeltanoModels, m
    from tests.protocols import TestsFlextMeltanoProtocols, p
    from tests.typings import TestsFlextMeltanoTypes, t
    from tests.utilities import TestsFlextMeltanoUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        ".integration",
        ".unit",
    ),
    build_lazy_import_map(
        {
            ".constants": (
                "TestsFlextMeltanoConstants",
                "c",
            ),
            ".models": (
                "TestsFlextMeltanoModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextMeltanoProtocols",
                "p",
            ),
            ".typings": (
                "TestsFlextMeltanoTypes",
                "t",
            ),
            ".utilities": (
                "TestsFlextMeltanoUtilities",
                "u",
            ),
            "flext_tests": (
                "d",
                "e",
                "h",
                "r",
                "reset_settings",
                "s",
                "settings",
                "settings_factory",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "TestsFlextMeltanoConstants",
    "TestsFlextMeltanoModels",
    "TestsFlextMeltanoProtocols",
    "TestsFlextMeltanoTypes",
    "TestsFlextMeltanoUtilities",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "reset_settings",
    "s",
    "settings",
    "settings_factory",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]
