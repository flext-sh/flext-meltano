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
    from flext_meltano import cli, config, d, e, h, main, meltano, r, s, settings, x


__all__: tuple[str, ...] = (
    "ExamplesFlextMeltanoConstants",
    "ExamplesFlextMeltanoModels",
    "ExamplesFlextMeltanoProtocols",
    "ExamplesFlextMeltanoSimple",
    "ExamplesFlextMeltanoTargetService",
    "ExamplesFlextMeltanoTargetSink",
    "ExamplesFlextMeltanoTypes",
    "ExamplesFlextMeltanoUtilities",
    "c",
    "cli",
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
        "c": ".constants",
        "cli": "flext_meltano",
        "config": "flext_meltano",
        "d": "flext_meltano",
        "e": "flext_meltano",
        "h": "flext_meltano",
        "m": ".models",
        "main": "flext_meltano",
        "meltano": "flext_meltano",
        "p": ".protocols",
        "r": "flext_meltano",
        "s": "flext_meltano",
        "settings": "flext_meltano",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_meltano",
    }),
    public_exports=__all__,
)
