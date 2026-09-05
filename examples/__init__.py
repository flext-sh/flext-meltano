# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from typing import Final

    from flext_meltano import FlextMeltanoConstants, d, e, h, r, s, x

    from .constants import (
        ExamplesFlextMeltanoConstants,
        ExamplesFlextMeltanoConstants as c,
    )
    from .models import ExamplesFlextMeltanoModels, ExamplesFlextMeltanoModels as m
    from .protocols import (
        ExamplesFlextMeltanoProtocols,
        ExamplesFlextMeltanoProtocols as p,
    )
    from .typings import ExamplesFlextMeltanoTypes, ExamplesFlextMeltanoTypes as t
    from .utilities import (
        ExamplesFlextMeltanoUtilities,
        ExamplesFlextMeltanoUtilities as u,
    )
__all__: tuple[str, ...] = (
    "ExamplesFlextMeltanoConstants",
    "ExamplesFlextMeltanoModels",
    "ExamplesFlextMeltanoProtocols",
    "ExamplesFlextMeltanoTypes",
    "ExamplesFlextMeltanoUtilities",
    "Final",
    "FlextMeltanoConstants",
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
            "flext_meltano": ("FlextMeltanoConstants", "d", "e", "h", "r", "s", "x"),
            "typing": ("Final",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
