# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import (
        api,
        config,
        d,
        e,
        h,
        install_local_packages,
        r,
        settings,
        td,
        tf,
        tk,
        tm,
        x,
    )

    from flext_meltano import cli, main, meltano
    from tests.base import TestsFlextMeltanoServiceBase, s
    from tests.constants import TestsFlextMeltanoConstants, c
    from tests.models import TestsFlextMeltanoModels, m
    from tests.protocols import TestsFlextMeltanoProtocols, p
    from tests.settings import TestsFlextMeltanoSettings
    from tests.typings import TestsFlextMeltanoTypes, t
    from tests.utilities import TestsFlextMeltanoUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextMeltanoConstants",
    "TestsFlextMeltanoModels",
    "TestsFlextMeltanoProtocols",
    "TestsFlextMeltanoServiceBase",
    "TestsFlextMeltanoSettings",
    "TestsFlextMeltanoTypes",
    "TestsFlextMeltanoUtilities",
    "api",
    "c",
    "cli",
    "config",
    "d",
    "e",
    "h",
    "install_local_packages",
    "m",
    "main",
    "meltano",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "TestsFlextMeltanoConstants": ".constants",
        "TestsFlextMeltanoModels": ".models",
        "TestsFlextMeltanoProtocols": ".protocols",
        "TestsFlextMeltanoServiceBase": ".base",
        "TestsFlextMeltanoSettings": ".settings",
        "TestsFlextMeltanoTypes": ".typings",
        "TestsFlextMeltanoUtilities": ".utilities",
        "api": "flext_tests",
        "c": ".constants",
        "cli": "flext_meltano",
        "config": "flext_tests",
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "install_local_packages": "flext_tests",
        "m": ".models",
        "main": "flext_meltano",
        "meltano": "flext_meltano",
        "p": ".protocols",
        "r": "flext_tests",
        "s": ".base",
        "settings": "flext_tests",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_tests",
    }),
    public_exports=__all__,
)
