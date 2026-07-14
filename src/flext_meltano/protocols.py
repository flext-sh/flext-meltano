"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import p
from flext_meltano._protocols.cli import FlextMeltanoProtocolsBase
from flext_meltano._protocols.plugin import FlextMeltanoProtocolsPlugin
from flext_meltano._protocols.project import FlextMeltanoProtocolsProject
from flext_meltano._protocols.services import FlextMeltanoProtocolsServices
from flext_meltano._protocols.singer import FlextMeltanoProtocolsSinger


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


# mro-wkii.17 (Codex): make the canonical facade rebind visible to Mypy.
del p
p = FlextMeltanoProtocols
__all__: list[str] = ["FlextMeltanoProtocols", "p"]
