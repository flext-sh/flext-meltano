# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from examples.constants import ExamplesFlextMeltanoConstants, c
    from examples.models import ExamplesFlextMeltanoModels, m
    from examples.protocols import ExamplesFlextMeltanoProtocols, p
    from examples.typings import ExamplesFlextMeltanoTypes, t
    from examples.utilities import ExamplesFlextMeltanoUtilities, u
    from flext_meltano import d, e, h, r, s, x
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
        "flext_meltano": (
            "d",
            "e",
            "h",
            "r",
            "s",
            "x",
        ),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
