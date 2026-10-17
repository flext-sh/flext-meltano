# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_meltano.__version__ import __version__

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, x

    from flext_meltano import services as services
    from flext_meltano.__version__ import (
        FlextMeltanoVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version_info__,
    )
    from flext_meltano._config import FlextMeltanoConfig, config
    from flext_meltano._settings import FlextMeltanoSettings, settings
    from flext_meltano.api import FlextMeltano, meltano
    from flext_meltano.base import FlextMeltanoServiceBase, s
    from flext_meltano.cli import FlextMeltanoCli, main
    from flext_meltano.constants import FlextMeltanoConstants, c
    from flext_meltano.models import FlextMeltanoModels, m
    from flext_meltano.pipeline_mgr import FlextMeltanoPipelineManager
    from flext_meltano.protocols import FlextMeltanoProtocols, p
    from flext_meltano.service_bases import (
        FlextMeltanoDbtServiceBase,
        FlextMeltanoLibraryRunner,
        FlextMeltanoTapServiceBase,
        FlextMeltanoTargetServiceBase,
    )
    from flext_meltano.typings import FlextMeltanoTypes, t
    from flext_meltano.utilities import FlextMeltanoUtilities, u


__all__: tuple[str, ...] = (
    "FlextMeltano",
    "FlextMeltanoCli",
    "FlextMeltanoConfig",
    "FlextMeltanoConstants",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoModels",
    "FlextMeltanoPipelineManager",
    "FlextMeltanoProtocols",
    "FlextMeltanoServiceBase",
    "FlextMeltanoSettings",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTargetServiceBase",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoVersion",
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
    "services",
    "settings",
    "t",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextMeltano": ".api",
        "FlextMeltanoCli": ".cli",
        "FlextMeltanoConfig": "._config",
        "FlextMeltanoConstants": ".constants",
        "FlextMeltanoDbtServiceBase": ".service_bases",
        "FlextMeltanoLibraryRunner": ".service_bases",
        "FlextMeltanoModels": ".models",
        "FlextMeltanoPipelineManager": ".pipeline_mgr",
        "FlextMeltanoProtocols": ".protocols",
        "FlextMeltanoServiceBase": ".base",
        "FlextMeltanoSettings": "._settings",
        "FlextMeltanoTapServiceBase": ".service_bases",
        "FlextMeltanoTargetServiceBase": ".service_bases",
        "FlextMeltanoTypes": ".typings",
        "FlextMeltanoUtilities": ".utilities",
        "FlextMeltanoVersion": ".__version__",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version_info__": ".__version__",
        "c": ".constants",
        "config": "._config",
        "d": "flext_cli",
        "e": "flext_cli",
        "h": "flext_cli",
        "m": ".models",
        "main": ".cli",
        "meltano": ".api",
        "p": ".protocols",
        "r": "flext_cli",
        "s": ".base",
        "services": ".services",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_cli",
    }),
    public_exports=__all__,
)
