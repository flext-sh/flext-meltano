# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

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
