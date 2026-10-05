# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._protocols.base import FlextMeltanoProtocolsBase
    from flext_meltano._protocols.plugin import FlextMeltanoProtocolsPlugin
    from flext_meltano._protocols.project import FlextMeltanoProtocolsProject
    from flext_meltano._protocols.services import FlextMeltanoProtocolsServices
    from flext_meltano._protocols.singer import FlextMeltanoProtocolsSinger


__all__: tuple[str, ...] = (
    "FlextMeltanoProtocolsBase",
    "FlextMeltanoProtocolsPlugin",
    "FlextMeltanoProtocolsProject",
    "FlextMeltanoProtocolsServices",
    "FlextMeltanoProtocolsSinger",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextMeltanoProtocolsBase": ".base",
        "FlextMeltanoProtocolsPlugin": ".plugin",
        "FlextMeltanoProtocolsProject": ".project",
        "FlextMeltanoProtocolsServices": ".services",
        "FlextMeltanoProtocolsSinger": ".singer",
    }),
    public_exports=__all__,
)
