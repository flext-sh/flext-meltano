# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
from flext_meltano.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import d as d, e as e, h as h, r as r, s as s, x as x
    from flext_meltano.api import FlextMeltano as FlextMeltano, meltano as meltano
    from flext_meltano.base import FlextMeltanoServiceBase as FlextMeltanoServiceBase
    from flext_meltano.cli import (
        FlextMeltanoCLI as FlextMeltanoCLI,
        cli as cli,
        main as main,
    )
    from flext_meltano.constants import (
        FlextMeltanoConstants as FlextMeltanoConstants,
        c as c,
    )
    from flext_meltano.models import FlextMeltanoModels as FlextMeltanoModels, m as m
    from flext_meltano.protocols import (
        FlextMeltanoProtocols as FlextMeltanoProtocols,
        p as p,
    )
    from flext_meltano.settings import FlextMeltanoSettings as FlextMeltanoSettings
    from flext_meltano.typings import FlextMeltanoTypes as FlextMeltanoTypes, t as t
    from flext_meltano.utilities import (
        FlextMeltanoUtilities as FlextMeltanoUtilities,
        u as u,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".api": (
            "FlextMeltano",
            "meltano",
        ),
        ".base": ("FlextMeltanoServiceBase",),
        ".cli": (
            "FlextMeltanoCLI",
            "cli",
            "main",
        ),
        ".constants": (
            "FlextMeltanoConstants",
            "c",
        ),
        ".models": (
            "FlextMeltanoModels",
            "m",
        ),
        ".protocols": (
            "FlextMeltanoProtocols",
            "p",
        ),
        ".settings": ("FlextMeltanoSettings",),
        ".typings": (
            "FlextMeltanoTypes",
            "t",
        ),
        ".utilities": (
            "FlextMeltanoUtilities",
            "u",
        ),
        "flext_cli": (
            "d",
            "e",
            "h",
            "r",
            "s",
            "x",
        ),
    },
)


__all__: tuple[str, ...] = (
    "FlextMeltano",
    "FlextMeltanoCLI",
    "FlextMeltanoConstants",
    "FlextMeltanoModels",
    "FlextMeltanoProtocols",
    "FlextMeltanoServiceBase",
    "FlextMeltanoSettings",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "cli",
    "d",
    "e",
    "h",
    "m",
    "main",
    "meltano",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
