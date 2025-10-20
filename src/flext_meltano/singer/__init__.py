"""Singer Protocol Implementation for FLEXT Meltano.

This module provides deep integration with singer-sdk following the Singer
specification with FLEXT ecosystem patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.singer.catalog import FlextMeltanoCatalogManager
from flext_meltano.singer.protocols import (
    FlextMeltanoPluginProtocols,
    FlextMeltanoSingerProtocols,
)
from flext_meltano.singer.service import FlextMeltanoSingerService
from flext_meltano.singer.state import FlextMeltanoStateManager
from flext_meltano.singer.tap import (
    FlextMeltanoStream,
    FlextMeltanoTap,
    FlextMeltanoTapAbstractions,
)
from flext_meltano.singer.target import (
    FlextMeltanoTarget,
    FlextMeltanoTargetAbstractions,
)

__all__ = [
    # Managers
    "FlextMeltanoCatalogManager",
    "FlextMeltanoPluginProtocols",
    # Protocols
    "FlextMeltanoSingerProtocols",
    # Service orchestration
    "FlextMeltanoSingerService",
    "FlextMeltanoStateManager",
    # Core SDK wrappers
    "FlextMeltanoStream",
    "FlextMeltanoTap",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTarget",
    "FlextMeltanoTargetAbstractions",
]
