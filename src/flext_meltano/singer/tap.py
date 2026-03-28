"""Singer Tap Protocol Implementation for FLEXT Meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import r

from flext_meltano import FlextMeltanoServiceBase, c, m, t
from flext_meltano.singer.tap_source import FlextMeltanoTapSourceMixin


class FlextMeltanoTapAbstractions(FlextMeltanoTapSourceMixin, FlextMeltanoServiceBase):
    """UNIFIED Source Abstractions class consolidating ALL source functionality."""

    def discover_streams(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
    ) -> r[t.Meltano.Singer.StreamCatalog]:
        """Discover available streams for a source configuration."""
        _ = source_config
        msg = "Singer protocol: requires singer-sdk tap integration to run tap --discover and parse catalog output"
        raise NotImplementedError(msg)

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute source abstraction operations (implements Service)."""
        msg = "Singer protocol: requires tap configuration and discovery before execution - use discover_streams() first"
        raise NotImplementedError(msg)

    def generate_catalog(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
    ) -> r[t.Dict]:
        """Generate a legacy Singer catalog from configuration."""
        _ = source_config
        msg = "Singer protocol: requires singer-sdk tap integration to generate catalog from tap discovery output"
        raise NotImplementedError(msg)

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
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception(
                "Source configuration processing failed", error=str(e)
            )
            return r[bool].fail(f"Source configuration processing failed: {e}")

    def sync_stream(
        self,
        source_config: m.Meltano.DataSourceConfig
        | m.Meltano.TapConfig
        | m.Meltano.TapInstance,
        stream_name: str,
        target: m.Meltano.TargetConfig | None = None,
    ) -> r[t.Dict]:
        """Synchronize a single stream from source to target."""
        _ = source_config, stream_name, target
        msg = "Singer protocol: requires singer-sdk integration to pipe tap stream output into target stdin"
        raise NotImplementedError(msg)

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
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Schema validation failed", error=str(e))
            return r[bool].fail(f"Schema validation failed: {e}")


__all__ = ["FlextMeltanoTapAbstractions"]
