"""FLEXT Singer Sink Base Class - Enterprise Singer SDK Integration.

This module provides FlextSink, a wrapper around singer_sdk.Sink that integrates
FLEXT ecosystem patterns while maintaining complete Singer SDK compatibility.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextLogger
from singer_sdk.sinks import Sink as SingerSink

if TYPE_CHECKING:
    from flext_meltano.singer_target_base import FlextTarget


class FlextSink(SingerSink):
    """FLEXT wrapper for singer_sdk.Sink with ecosystem integration.

    This class wraps singer_sdk.Sink to enforce FLEXT domain library patterns
    while maintaining 100% Singer SDK API compatibility. All flext-target-* projects
    MUST inherit from this class instead of directly importing singer_sdk.Sink.

    Features:
    - FlextLogger integration for consistent ecosystem logging
    - Access to parent target's FlextContainer
    - FLEXT patterns (FlextResult, etc.) available to subclasses
    - Complete Singer SDK compatibility (no breaking changes)

    Example:
        ```python
        from flext_meltano import FlextTarget, FlextSink


        class MySink(FlextSink):
            name = "my_sink"

            def process_record(self, record, context):
                # Use FlextLogger
                self.flext_logger.debug(f"Processing record for {self.stream_name}")
                # Process record...
        ```

    Note:
        This wrapper internally uses singer_sdk.Sink. Sink implementations
        should NEVER import singer_sdk directly - use this wrapper instead.

    """

    def __init__(
        self,
        target: FlextTarget,
        stream_name: str,
        schema: dict,
        key_properties: list[str] | None = None,
    ) -> None:
        """Initialize FlextSink with FLEXT ecosystem integration.

        Args:
            target: Parent FlextTarget instance
            stream_name: Name of the stream this sink handles
            schema: JSON schema for the stream
            key_properties: List of key property names

        """
        # Initialize Singer SDK Sink
        super().__init__(
            target=target,
            stream_name=stream_name,
            schema=schema,
            key_properties=key_properties,
        )

        # FLEXT ecosystem integration
        self._flext_logger = FlextLogger(f"{target.name}.{stream_name}")

        # Log sink initialization
        self._flext_logger.debug(
            f"FlextSink initialized: {stream_name}",
            target_name=target.name,
            key_properties=key_properties or [],
        )

    @property
    def flext_logger(self) -> FlextLogger:
        """Get FLEXT ecosystem logger for this sink.

        Returns:
            FlextLogger instance configured for this sink

        """
        return self._flext_logger


__all__ = ["FlextSink"]
