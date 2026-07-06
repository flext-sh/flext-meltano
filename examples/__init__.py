# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from examples.constants import (
        ExamplesFlextMeltanoConstants as ExamplesFlextMeltanoConstants,
        c as c,
    )
    from examples.models import (
        ExamplesFlextMeltanoModels as ExamplesFlextMeltanoModels,
        m as m,
    )
    from examples.protocols import (
        ExamplesFlextMeltanoProtocols as ExamplesFlextMeltanoProtocols,
        p as p,
    )
    from examples.typings import (
        ExamplesFlextMeltanoTypes as ExamplesFlextMeltanoTypes,
        t as t,
    )
    from examples.utilities import (
        ExamplesFlextMeltanoUtilities as ExamplesFlextMeltanoUtilities,
        u as u,
    )
    from flext_core._root_typing_parts.facades import (
        d as d,
        e as e,
        h as h,
        r as r,
        s as s,
        x as x,
    )
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
        "flext_core._root_typing_parts.facades": (
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
