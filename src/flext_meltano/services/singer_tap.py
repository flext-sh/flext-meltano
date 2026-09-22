"""Singer Tap Abstractions — MRO mixin for FlextMeltano facade.

Concrete source abstraction operations built on the split source mixin.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import FlextMeltanoServiceBase, c, m, p, r

from .tap_source_mixin import FlextMeltanoTapSourceMixin


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
    ) -> p.Result[bool]:
        """Process a source configuration for validation via isinstance narrowing."""

        def _run_process_source() -> p.Result[bool]:
            if isinstance(items, m.Meltano.DataSourceConfig):
                source_type = items.source_type
            elif isinstance(items, m.Meltano.TapConfig):
                source_type = items.tap_type
            else:
                source_type = items.tap_type
            self.logger.debug(
                "Processing source configuration", source_name=source_type
            )
            if not source_type:
                return r[bool].fail("Source configuration must have a type")
            return r[bool].ok(value=True)

        try:
            return _run_process_source()
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception(
                "Source configuration processing failed", error=str(e)
            )
            return r[bool].fail_op("Source configuration processing", e)

    def validate_stream_schema(
        self, stream_def: m.Meltano.StreamDefinition
    ) -> p.Result[bool]:
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
        except c.Meltano.SINGER_SAFE_EXCEPTIONS as e:
            self.logger.exception("Schema validation failed", error=str(e))
            return r[bool].fail_op("Schema validation", e)


__all__: list[str] = ["FlextMeltanoTapAbstractions"]
