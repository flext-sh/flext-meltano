# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.examples.constants import (
        ExamplesFlextMeltanoConstants as ExamplesFlextMeltanoConstants,
        c as c,
    )
    from flext_meltano.examples.models import (
        ExamplesFlextMeltanoModels as ExamplesFlextMeltanoModels,
        m as m,
    )
    from flext_meltano.examples.protocols import (
        ExamplesFlextMeltanoProtocols as ExamplesFlextMeltanoProtocols,
        p as p,
    )
    from flext_meltano.examples.typings import (
        ExamplesFlextMeltanoTypes as ExamplesFlextMeltanoTypes,
        t as t,
    )
    from flext_meltano.examples.utilities import (
        ExamplesFlextMeltanoUtilities as ExamplesFlextMeltanoUtilities,
        u as u,
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
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
