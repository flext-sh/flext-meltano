# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
<<<<<<< HEAD
    from flext_cli import cli

    from flext_core import (
        core,
        d,
        e,
        h,
        lazy,
        lazy_attribute,
        normalize_lazy_imports,
        r,
        x,
    )
    from flext_meltano import config, main, meltano, s, settings
=======
    from flext_meltano import d, e, h, r, s, x
>>>>>>> recovery/rope-automation-20260921

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
    "c",
    "d",
    "e",
    "h",
<<<<<<< HEAD
    "lazy",
    "lazy_attribute",
    "m",
    "main",
    "meltano",
    "normalize_lazy_imports",
    "p",
    "r",
    "s",
    "settings",
=======
    "m",
    "p",
    "r",
    "s",
>>>>>>> recovery/rope-automation-20260921
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
<<<<<<< HEAD
            "flext_cli": ("cli",),
            "flext_core": (
                "core",
                "d",
                "e",
                "h",
                "lazy",
                "lazy_attribute",
                "normalize_lazy_imports",
                "r",
                "x",
            ),
            "flext_meltano": ("config", "main", "meltano", "s", "settings"),
=======
            "flext_meltano": ("d", "e", "h", "r", "s", "x"),
>>>>>>> recovery/rope-automation-20260921
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
