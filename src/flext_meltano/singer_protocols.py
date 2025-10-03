"""FLEXT Meltano Singer Protocols - Protocol definitions for Singer components.

This module provides protocol definitions for Singer taps and targets
following flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol

from flext_core import FlextTypes


class SingerTap(Protocol):
    """Singer Tap protocol definition."""

    streams: FlextTypes.StringList
    name: str
    state: FlextTypes.Dict

    def get_records(self, stream_name: str) -> list[FlextTypes.Dict]: ...  # noqa: D102
    def get_state(self) -> FlextTypes.Dict: ...  # noqa: D102


class SingerTarget(Protocol):
    """Singer Target protocol definition."""

    name: str


__all__ = ["SingerTap", "SingerTarget"]
