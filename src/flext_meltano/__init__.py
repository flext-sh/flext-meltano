# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        cli,
        core,
        d,
        e,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        merge_lazy_imports,
        normalize_lazy_imports,
        r,
        resolve_lazy_members,
        x,
    )

    from flext_meltano.__version__ import (
        FlextMeltanoVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
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
        FlextMeltanoAbstractions,
        FlextMeltanoDbtServiceBase,
        FlextMeltanoLibraryRunner,
        FlextMeltanoSingerTapAdapter,
        FlextMeltanoTapServiceBase,
        FlextMeltanoTargetAbstractions,
        FlextMeltanoTargetServiceBase,
    )
    from flext_meltano.typings import FlextMeltanoTypes, t
    from flext_meltano.utilities import FlextMeltanoUtilities, u


__all__: tuple[str, ...] = (
    "FlextMeltano",
    "FlextMeltanoAbstractions",
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
    "FlextMeltanoSingerTapAdapter",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTargetAbstractions",
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
    "build_lazy_import_map",
    "c",
    "cleanup_submodule_namespace",
    "cli",
    "config",
    "core",
    "d",
    "e",
    "h",
    "install_lazy_exports",
    "lazy",
    "lazy_getattr",
    "lazy_member",
    "m",
    "main",
    "meltano",
    "merge_lazy_imports",
    "normalize_lazy_imports",
    "p",
    "r",
    "resolve_lazy_members",
    "s",
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
        "FlextMeltanoAbstractions": ".service_bases",
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
        "FlextMeltanoSingerTapAdapter": ".service_bases",
        "FlextMeltanoTapServiceBase": ".service_bases",
        "FlextMeltanoTargetAbstractions": ".service_bases",
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
        "build_lazy_import_map": "flext_cli",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_cli",
        "cli": "flext_cli",
        "config": "._config",
        "core": "flext_cli",
        "d": "flext_cli",
        "e": "flext_cli",
        "h": "flext_cli",
        "install_lazy_exports": "flext_cli",
        "lazy": "flext_cli",
        "lazy_getattr": "flext_cli",
        "lazy_member": "flext_cli",
        "m": ".models",
        "main": ".cli",
        "meltano": ".api",
        "merge_lazy_imports": "flext_cli",
        "normalize_lazy_imports": "flext_cli",
        "p": ".protocols",
        "r": "flext_cli",
        "resolve_lazy_members": "flext_cli",
        "s": ".base",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_cli",
    }),
    public_exports=__all__,
)

if not TYPE_CHECKING:
    from flext_meltano.__version__ import __version__
