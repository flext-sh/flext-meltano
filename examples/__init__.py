# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_cli.base import s

    from examples.constants import ExamplesFlextMeltanoConstants, c
    from examples.models import ExamplesFlextMeltanoModels, m
    from examples.protocols import ExamplesFlextMeltanoProtocols, p
    from examples.typings import ExamplesFlextMeltanoTypes, t
    from examples.utilities import ExamplesFlextMeltanoUtilities, u
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".constants": (
            "ExamplesFlextMeltanoConstants",
            "c",
        ),
        ".models": (
            "ExamplesFlextMeltanoModels",
            "m",
        ),
        ".protocols": (
            "ExamplesFlextMeltanoProtocols",
            "p",
        ),
        ".typings": (
            "ExamplesFlextMeltanoTypes",
            "t",
        ),
        ".utilities": (
            "ExamplesFlextMeltanoUtilities",
            "u",
        ),
        "flext_cli.base": ("s",),
        "flext_core.decorators": ("d",),
        "flext_core.exceptions": ("e",),
        "flext_core.handlers": ("h",),
        "flext_core.mixins": ("x",),
        "flext_core.result": ("r",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
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
]
