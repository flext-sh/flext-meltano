# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from examples.constants import ExamplesFlextMeltanoConstants, c
    from examples.models import ExamplesFlextMeltanoModels, m
    from examples.protocols import ExamplesFlextMeltanoProtocols, p
    from examples.simple_working import ExamplesFlextMeltanoSimple
    from examples.target_service import ExamplesFlextMeltanoTargetService
    from examples.target_sink import ExamplesFlextMeltanoTargetSink
    from examples.typings import ExamplesFlextMeltanoTypes, t
    from examples.utilities import ExamplesFlextMeltanoUtilities, u
    from flext_meltano import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        cli,
        config,
        core,
        d,
        e,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        main,
        meltano,
        merge_lazy_imports,
        normalize_lazy_imports,
        r,
        resolve_lazy_members,
        s,
        settings,
        x,
    )


__all__: tuple[str, ...] = (
    "ExamplesFlextMeltanoConstants",
    "ExamplesFlextMeltanoModels",
    "ExamplesFlextMeltanoProtocols",
    "ExamplesFlextMeltanoSimple",
    "ExamplesFlextMeltanoTargetService",
    "ExamplesFlextMeltanoTargetSink",
    "ExamplesFlextMeltanoTypes",
    "ExamplesFlextMeltanoUtilities",
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
        "ExamplesFlextMeltanoConstants": ".constants",
        "ExamplesFlextMeltanoModels": ".models",
        "ExamplesFlextMeltanoProtocols": ".protocols",
        "ExamplesFlextMeltanoSimple": ".simple_working",
        "ExamplesFlextMeltanoTargetService": ".target_service",
        "ExamplesFlextMeltanoTargetSink": ".target_sink",
        "ExamplesFlextMeltanoTypes": ".typings",
        "ExamplesFlextMeltanoUtilities": ".utilities",
        "build_lazy_import_map": "flext_meltano",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_meltano",
        "cli": "flext_meltano",
        "config": "flext_meltano",
        "core": "flext_meltano",
        "d": "flext_meltano",
        "e": "flext_meltano",
        "h": "flext_meltano",
        "install_lazy_exports": "flext_meltano",
        "lazy": "flext_meltano",
        "lazy_getattr": "flext_meltano",
        "lazy_member": "flext_meltano",
        "m": ".models",
        "main": "flext_meltano",
        "meltano": "flext_meltano",
        "merge_lazy_imports": "flext_meltano",
        "normalize_lazy_imports": "flext_meltano",
        "p": ".protocols",
        "r": "flext_meltano",
        "resolve_lazy_members": "flext_meltano",
        "s": "flext_meltano",
        "settings": "flext_meltano",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_meltano",
    }),
    public_exports=__all__,
)
