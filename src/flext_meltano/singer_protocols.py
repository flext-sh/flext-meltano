"""FLEXT Meltano Singer Protocols - Protocol definitions for Singer components.

This module provides protocol definitions for Singer taps and targets
following flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Protocol

from flext_core import FlextCore


class FlextMeltanoSingerProtocols:
    """Unified Singer protocols for Meltano ELT operations.

    This class consolidates all Singer protocol definitions into a single
    namespace following FLEXT 'one class per module' pattern.
    """

    class SingerTap(Protocol):
        """Singer Tap protocol definition."""

        streams: FlextCore.Types.StringList
        name: str
        state: FlextCore.Types.Dict

        def get_records(self, stream_name: str) -> list[FlextCore.Types.Dict]:
            """Get records for a specific stream."""
            ...

        def get_state(self) -> FlextCore.Types.Dict:
            """Get current state."""
            ...

    class SingerTarget(Protocol):
        """Singer Target protocol definition."""

        name: str


# Backward compatibility aliases
SingerTap = FlextMeltanoSingerProtocols.SingerTap
SingerTarget = FlextMeltanoSingerProtocols.SingerTarget

__all__ = ["FlextMeltanoSingerProtocols", "SingerTap", "SingerTarget"]
