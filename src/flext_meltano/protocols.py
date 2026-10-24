# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliProtocols

from flext_meltano._protocols import (
    FlextMeltanoProtocolsBase,
    FlextMeltanoProtocolsSinger,
)


class FlextMeltanoProtocols(FlextCliProtocols):
    """Unified Meltano protocols extending FlextCliProtocols."""

    class Meltano(
        FlextMeltanoProtocolsSinger,
        FlextMeltanoProtocolsBase,
    ):
        """Meltano ELT domain-specific protocols."""


p = FlextMeltanoProtocols
__all__ = ["FlextMeltanoProtocols", "p"]
