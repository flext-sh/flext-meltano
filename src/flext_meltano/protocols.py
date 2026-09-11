"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import p

from ._protocols.cli import FlextMeltanoProtocolsBase
from ._protocols.plugin import FlextMeltanoProtocolsPlugin
from ._protocols.project import FlextMeltanoProtocolsProject
from ._protocols.services import FlextMeltanoProtocolsServices
from ._protocols.singer import FlextMeltanoProtocolsSinger


class FlextMeltanoProtocols(p):
    """Unified Meltano protocols extending FlextCliProtocols."""

    class Meltano(
        FlextMeltanoProtocolsPlugin,
        FlextMeltanoProtocolsProject,
        FlextMeltanoProtocolsServices,
        FlextMeltanoProtocolsSinger,
        FlextMeltanoProtocolsBase,
    ):
        """Meltano ELT domain-specific protocols."""


p = FlextMeltanoProtocols
__all__ = ["FlextMeltanoProtocols", "p"]
