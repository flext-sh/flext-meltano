"""FLEXT Singer Stream Base Class - Enterprise Singer SDK Integration.

This module provides FlextStream, a wrapper around singer_sdk.Stream that integrates
FLEXT ecosystem patterns while maintaining complete Singer SDK compatibility.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextLogger
from singer_sdk.streams import Stream as SingerStream

if TYPE_CHECKING:
    from flext_meltano.singer_tap_base import FlextTap


class FlextStream(SingerStream):
    """FLEXT wrapper for singer_sdk.Stream with ecosystem integration.

    This class wraps singer_sdk.Stream to enforce FLEXT domain library patterns
    while maintaining 100% Singer SDK API compatibility. All flext-tap-* projects
    MUST inherit from this class instead of directly importing singer_sdk.Stream.

    Features:
    - FlextLogger integration for consistent ecosystem logging
    - Access to parent tap's FlextContainer
    - FLEXT patterns (FlextResult, etc.) available to subclasses
    - Complete Singer SDK compatibility (no breaking changes)

    Example:
        ```python
        from flext_meltano import FlextTap, FlextStream


        class MyStream(FlextStream):
            name = "my_stream"
            schema = {...}

            def get_records(self, context):
                # Use FlextLogger
                self.flext_logger.info(f"Fetching records for {self.name}")
                yield from data_source
        ```

    Note:
        This wrapper internally uses singer_sdk.Stream. Stream implementations
        should NEVER import singer_sdk directly - use this wrapper instead.

    """

    def __init__(
        self,
        tap: FlextTap,
        name: str | None = None,
        schema: dict | None = None,
        path: str | None = None,
    ) -> None:
        """Initialize FlextStream with FLEXT ecosystem integration.

        Args:
            tap: Parent FlextTap instance
            name: Stream name (optional if class attribute exists)
            schema: Stream JSON schema (optional if class attribute exists)
            path: Stream API path (optional)

        """
        # Initialize Singer SDK Stream
        super().__init__(tap=tap, name=name, schema=schema, path=path)

        # FLEXT ecosystem integration
        self._flext_logger = FlextLogger(f"{tap.name}.{self.name}")

        # Log stream initialization
        self._flext_logger.debug(
            f"FlextStream initialized: {self.name}",
            tap_name=tap.name,
            schema_defined=schema is not None,
        )

    @property
    def flext_logger(self) -> FlextLogger:
        """Get FLEXT ecosystem logger for this stream.

        Returns:
            FlextLogger instance configured for this stream

        """
        return self._flext_logger


__all__ = ["FlextStream"]
