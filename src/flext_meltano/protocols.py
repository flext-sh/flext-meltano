"""FLEXT Meltano Protocols - All protocol definitions for the domain.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_cli import FlextCliProtocols

from flext_meltano._protocols import (
    FlextMeltanoProtocolsPlugin,
    FlextMeltanoProtocolsProject,
    FlextMeltanoProtocolsServices,
    FlextMeltanoProtocolsSinger,
)


class FlextMeltanoProtocols(FlextCliProtocols):
    """Unified Meltano protocols extending FlextCliProtocols.

    Extends p to inherit all foundation protocols (Result, Service, etc.)
    and adds Meltano/Singer/DBT-specific protocols in the Meltano namespace.

    Architecture:
    - EXTENDS: p (inherits Foundation, Domain, Application, etc.)
    - ADDS: Meltano/Singer/DBT-specific protocols in Meltano namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_core import p

    # Foundation protocols (inherited)
    result: FlextCliProtocols.Result[str]
    service: FlextCliProtocols.Service[str]

    # Meltano-specific protocols
    tap: FlextCliProtocols.Meltano.Tap
    target: FlextCliProtocols.Meltano.Target
    """

    class Meltano(
        FlextMeltanoProtocolsPlugin,
        FlextMeltanoProtocolsProject,
        FlextMeltanoProtocolsServices,
        FlextMeltanoProtocolsSinger,
    ):
        """Meltano ELT domain-specific protocols.

        Provides protocols for Meltano plugins, Singer taps/targets/streams,
        DBT runners, and service operations.
        """


p = FlextMeltanoProtocols
__all__ = ["FlextMeltanoProtocols", "p"]
