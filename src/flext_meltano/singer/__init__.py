"""Singer Protocol Implementation for FLEXT Meltano.

This module provides deep integration with singer-sdk following the Singer
specification with FLEXT ecosystem patterns and railway-oriented programming.

NOTE: Heavy modules (service, tap, target) are NOT imported at package level
to avoid circular imports. Import them explicitly when needed:
    from flext_meltano.singer.service import FlextMeltanoSingerService
    from flext_meltano.singer.tap import FlextMeltanoTap

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.singer.protocols import (
    FlextMeltanoPluginProtocols,
    FlextMeltanoSingerProtocols,
)

__all__ = [
    # Protocols only - other modules must be imported explicitly
    "FlextMeltanoPluginProtocols",
    "FlextMeltanoSingerProtocols",
]
