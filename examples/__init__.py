# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from examples.constants import (
        ExamplesFlextMeltanoConstants,
        ExamplesFlextMeltanoConstants as c,
    )
    from examples.models import (
        ExamplesFlextMeltanoModels,
        ExamplesFlextMeltanoModels as m,
    )
    from examples.protocols import (
        ExamplesFlextMeltanoProtocols,
        ExamplesFlextMeltanoProtocols as p,
    )
    from examples.typings import (
        ExamplesFlextMeltanoTypes,
        ExamplesFlextMeltanoTypes as t,
    )
    from examples.utilities import (
        ExamplesFlextMeltanoUtilities,
        ExamplesFlextMeltanoUtilities as u,
    )
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
    from flext_core.service import s
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".constants": ("ExamplesFlextMeltanoConstants",),
        ".models": ("ExamplesFlextMeltanoModels",),
        ".protocols": ("ExamplesFlextMeltanoProtocols",),
        ".typings": ("ExamplesFlextMeltanoTypes",),
        ".utilities": ("ExamplesFlextMeltanoUtilities",),
        "flext_core.decorators": ("d",),
        "flext_core.exceptions": ("e",),
        "flext_core.handlers": ("h",),
        "flext_core.mixins": ("x",),
        "flext_core.result": ("r",),
        "flext_core.service": ("s",),
    },
    alias_groups={
        ".constants": (("c", "ExamplesFlextMeltanoConstants"),),
        ".models": (("m", "ExamplesFlextMeltanoModels"),),
        ".protocols": (("p", "ExamplesFlextMeltanoProtocols"),),
        ".typings": (("t", "ExamplesFlextMeltanoTypes"),),
        ".utilities": (("u", "ExamplesFlextMeltanoUtilities"),),
    },
)

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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
