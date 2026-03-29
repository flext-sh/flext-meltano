"""Singer Tap Protocol Implementation for FLEXT Meltano.

Concrete operations only — abstract contracts live in p.Meltano.Singer.*
protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import r

from flext_meltano import FlextMeltanoServiceBase, c, m
from flext_meltano.singer.tap_source import FlextMeltanoTapSourceMixin


class FlextMeltanoTapAbstractions(FlextMeltanoTapSourceMixin, FlextMeltanoServiceBase):
    """Concrete source abstraction operations.

    Only real implementations live here. Abstract contracts
    (discover_streams, sync_stream, etc.) are defined in
    p.Meltano.Singer.Tap and p.Meltano.Singer.SingerTap protocols.
    Consumers implement those protocols directly.
    """

    def process_source(
        self,
        items: m.Meltano.DataSourceConfig | m.Meltano.TapConfig | m.Meltano.TapInstance,
    ) -> r[bool]:
        """Process a source configuration for validation."""
        try:
            source_type = getattr(items, "source_type", None) or getattr(
                items,
                "tap_type",
                c.IDENTIFIER_UNKNOWN,
            )
            self.logger.debug(
                "Processing source configuration", source_name=source_type
            )
            if not source_type or source_type == c.IDENTIFIER_UNKNOWN:
                return r[bool].fail("Source configuration must have a type")
            return r[bool].ok(value=True)
        except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
            self.logger.exception(
                "Source configuration processing failed", error=str(e)
            )
            return r[bool].fail(f"Source configuration processing failed: {e}")

    def validate_stream_schema(self, stream_def: m.Meltano.StreamDefinition) -> r[bool]:
        """Validate a stream definition's schema."""
        try:
            self.logger.debug(
                "Validating stream schema", stream_name=stream_def.stream_name
            )
            if not stream_def.stream_schema:
                return r[bool].fail("Stream schema cannot be empty")
            if "properties" not in stream_def.stream_schema:
                return r[bool].fail("Stream schema must contain properties")
            return r[bool].ok(value=True)
        except c.Meltano.Singer.SAFE_EXCEPTIONS as e:
            self.logger.exception("Schema validation failed", error=str(e))
            return r[bool].fail(f"Schema validation failed: {e}")


__all__ = ["FlextMeltanoTapAbstractions"]
