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
    from flext_cli import d, e, h, r, x

    from ._config import FlextMeltanoConfig, config
    from ._settings import FlextMeltanoSettings, settings
    from .api import FlextMeltano, meltano
    from .base import FlextMeltanoServiceBase, s
    from .cli import FlextMeltanoCli, main
    from .constants import FlextMeltanoConstants, FlextMeltanoConstants as c
    from .models import FlextMeltanoModels, FlextMeltanoModels as m
    from .protocols import FlextMeltanoProtocols, FlextMeltanoProtocols as p
    from .services.consumer_bases.dbt_service_base import FlextMeltanoDbtServiceBase
    from .typings import FlextMeltanoTypes, FlextMeltanoTypes as t
    from .utilities import FlextMeltanoUtilities, FlextMeltanoUtilities as u

    _ = (
        c,
        FlextMeltanoConstants,
        t,
        FlextMeltanoTypes,
        p,
        FlextMeltanoProtocols,
        m,
        FlextMeltanoModels,
        u,
        FlextMeltanoUtilities,
        d,
        e,
        h,
        r,
        x,
        s,
        FlextMeltanoServiceBase,
        main,
        FlextMeltanoCli,
        config,
        FlextMeltanoConfig,
        FlextMeltanoDbtServiceBase,
        FlextMeltanoSettings,
        settings,
        FlextMeltano,
        meltano,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextMeltanoConfig", "config"),
    "._settings": ("FlextMeltanoSettings", "settings"),
    ".api": ("FlextMeltano", "meltano"),
    ".base": ("FlextMeltanoServiceBase", "s"),
    ".services.consumer_bases.dbt_service_base": ("FlextMeltanoDbtServiceBase",),
    ".cli": ("FlextMeltanoCli", "main"),
    ".constants": ("FlextMeltanoConstants", "c"),
    ".models": ("FlextMeltanoModels", "m"),
    ".protocols": ("FlextMeltanoProtocols", "p"),
    ".typings": ("FlextMeltanoTypes", "t"),
    ".utilities": ("FlextMeltanoUtilities", "u"),
    "flext_cli": ("d", "e", "h", "r", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_DIRECT_IMPORTS: tuple[str, ...] = (
    "FlextMeltano",
    "FlextMeltanoCli",
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
    "build_lazy_import_map",
    "c",
    "config",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "m",
    "main",
    "meltano",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)

__all__: tuple[str, ...] = (
    "FlextMeltano",
    "FlextMeltanoCli",
    "FlextMeltanoConfig",
    "FlextMeltanoConstants",
    "FlextMeltanoDbtServiceBase",
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
    "config",
    "d",
    "e",
    "h",
    "m",
    "main",
    "meltano",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
