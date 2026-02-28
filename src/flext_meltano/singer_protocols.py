"""FLEXT Meltano Singer Protocols - Protocol definitions for Singer components.

This module provides protocol definitions for Singer taps and targets
following flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Protocol

from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes

m = FlextMeltanoModels
t = FlextMeltanoTypes


class FlextMeltanoSingerProtocols:
    """Unified Singer protocols for Meltano ELT operations.

    This class consolidates all Singer protocol definitions into a single
    namespace following FLEXT 'one class per module' pattern.
    """

    class SingerTap(Protocol):
        """Singer Tap protocol definition."""

        streams: list[str]
        name: str
        state: m.Meltano.SingerStateMessage

        def discover(self) -> m.Meltano.SingerCatalog:
            """Discover and return the tap Singer catalog."""
            ...

        def sync(
            self,
            catalog: m.Meltano.SingerCatalog,
            state: m.Meltano.SingerStateMessage,
        ) -> None:
            """Synchronize records using catalog and state."""
            ...

        def get_records(self, stream_name: str) -> list[m.Meltano.SingerRecordMessage]:
            """Get records for a specific stream."""
            ...

        def get_state(self) -> m.Meltano.SingerStateMessage:
            """Get current state."""
            ...

    class SingerTarget(Protocol):
        """Singer Target protocol definition."""

        name: str


__all__ = ["FlextMeltanoSingerProtocols"]
