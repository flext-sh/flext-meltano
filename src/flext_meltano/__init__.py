# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from flext_cli import d as d
    from flext_cli import e as e
    from flext_cli import h as h
    from flext_cli import r as r
    from flext_cli import x as x

    from ._config import FlextMeltanoConfig as FlextMeltanoConfig
    from ._config import config as config
    from ._settings import FlextMeltanoSettings as FlextMeltanoSettings
    from ._settings import settings as settings
    from .api import FlextMeltano as FlextMeltano
    from .api import FlextMeltanoAbstractions as FlextMeltanoAbstractions
    from .api import meltano as meltano
    from .base import FlextMeltanoServiceBase as FlextMeltanoServiceBase
    from .service_bases import FlextMeltanoDbtServiceBase as FlextMeltanoDbtServiceBase
    from .service_bases import FlextMeltanoLibraryRunner as FlextMeltanoLibraryRunner
    from .service_bases import FlextMeltanoTapServiceBase as FlextMeltanoTapServiceBase
    from .service_bases import FlextMeltanoTargetServiceBase as FlextMeltanoTargetServiceBase

    s: type[FlextMeltanoServiceBase]
    from .cli import FlextMeltanoCli as FlextMeltanoCli
    from .cli import main as main
    from .constants import FlextMeltanoConstants as FlextMeltanoConstants

    c: type[FlextMeltanoConstants]
    from .models import FlextMeltanoModels as FlextMeltanoModels

    m: type[FlextMeltanoModels]
    from .protocols import FlextMeltanoProtocols as FlextMeltanoProtocols

    p: type[FlextMeltanoProtocols]
    from .typings import FlextMeltanoTypes as FlextMeltanoTypes

    t: type[FlextMeltanoTypes]
    from .utilities import FlextMeltanoUtilities as FlextMeltanoUtilities

    u: type[FlextMeltanoUtilities]

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextMeltanoConfig", "config"),
    "._settings": ("FlextMeltanoSettings", "settings"),
    ".api": ("FlextMeltano", "FlextMeltanoAbstractions", "meltano"),
    ".base": ("FlextMeltanoServiceBase", "s"),
    ".service_bases": (
        "FlextMeltanoDbtServiceBase",
        "FlextMeltanoLibraryRunner",
        "FlextMeltanoTapServiceBase",
        "FlextMeltanoTargetServiceBase",
    ),
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

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextMeltano",
    "FlextMeltanoAbstractions",
    "FlextMeltanoCli",
    "FlextMeltanoConfig",
    "FlextMeltanoConstants",
    "FlextMeltanoModels",
    "FlextMeltanoProtocols",
    "FlextMeltanoServiceBase",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTargetServiceBase",
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

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
