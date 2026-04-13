"""FLEXT Pipeline Abstractions - Tap-specific Meltano runtime operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Self

from flext_core import p, r
from flext_meltano.constants import FlextMeltanoConstants as c
from flext_meltano.models import FlextMeltanoModels as m
from flext_meltano.services._abstractions_base import FlextMeltanoAbstractionsBase
from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoAbstractions(FlextMeltanoAbstractionsBase):
    """Core abstraction wrapping the imported Meltano runtime with r[T] results."""

    @classmethod
    def create_abstractions_instance(cls) -> p.Result[Self]:
        """Factory method for creating a FlextMeltanoAbstractions instance."""
        instance: Self = cls()
        return r[Self](value=instance, success=True)

    # -- Tap-specific operations (discovery, sync, catalog) --

    def process_tap_config(
        self, settings: m.Meltano.TapConfig
    ) -> p.Result[m.Meltano.TapConfig]:
        """Validate and return tap configuration."""
        return r[m.Meltano.TapConfig].ok(settings)

    def build_tap_instance(
        self,
        tap_instance: m.Meltano.TapInstance,
    ) -> t.RecursiveContainerMapping:
        """Build tap instance representation."""
        return {"tap_id": tap_instance.tap_id, "tap_type": tap_instance.tap_type}

    def discover_streams(
        self,
        tap_instance: m.Meltano.TapInstance,
    ) -> p.Result[t.RecursiveContainerMapping]:
        """Discover available streams via ``meltano select --list``."""
        try:
            cmd_result = self._run_meltano(
                [
                    c.Meltano.CMD_SELECT,
                    tap_instance.tap_type,
                    c.Meltano.CMD_LIST_OPTION,
                    c.Meltano.CMD_ALL_OPTION,
                ],
            )
            if cmd_result.failure:
                return r[t.RecursiveContainerMapping].fail(
                    cmd_result.error or "Stream discovery failed",
                )
            stream_defs: list[t.RecursiveContainerMapping] = []
            for line in cmd_result.value.splitlines():
                name = line.strip()
                if name and not name.startswith("["):
                    stream_defs.append({"stream_name": name, "tap_stream_id": name})
                    if name not in self._stream_registry:
                        self._stream_registry[name] = m.Meltano.StreamDefinition(
                            stream_name=name,
                            stream_schema={"type": "object", "properties": {}},
                            source_type=tap_instance.tap_type,
                        )
            return r[t.RecursiveContainerMapping].ok({"streams": stream_defs})
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"Failed to discover streams: {e}"
            self.logger.exception(error_msg)
            return r[t.RecursiveContainerMapping].fail(error_msg)

    def sync_stream(
        self,
        tap_instance: m.Meltano.TapInstance,
        stream_name: str,
        target_config: m.Meltano.TargetConfig | None = None,
    ) -> p.Result[t.RecursiveContainerMapping]:
        """Sync a single stream via ``meltano elt`` with stream selection."""
        try:
            loader_name = (
                target_config.target_type
                if target_config is not None
                else c.IDENTIFIER_UNKNOWN
            )
            cmd_args = [
                c.Meltano.CMD_ELT,
                tap_instance.tap_type,
                str(loader_name),
                c.Meltano.CMD_SELECT_OPTION,
                stream_name,
            ]
            cmd_result = self._run_meltano(cmd_args)
            status = (
                c.Meltano.StreamStatus.COMPLETED
                if cmd_result.success
                else c.Meltano.StreamStatus.FAILED
            )
            result: t.RecursiveContainerMapping = {
                "stream_name": stream_name,
                "status": status,
                "target_loaded": target_config is not None,
            }
            if cmd_result.failure:
                return r[t.RecursiveContainerMapping].fail(
                    cmd_result.error or "Stream sync failed"
                )
            return r[t.RecursiveContainerMapping].ok(result)
        except c.Meltano.OPERATION_ERRORS as e:
            error_msg = f"Failed to sync stream {stream_name}: {e}"
            self.logger.exception(error_msg)
            return r[t.RecursiveContainerMapping].fail(error_msg)

    def create_tap_from_config(
        self,
        tap_type: str,
        connection_config: t.RecursiveContainerMapping,
        stream_config: t.RecursiveContainerMapping | None = None,
    ) -> p.Result[m.Meltano.TapInstance]:
        """Create a TapInstance from configuration."""
        try:
            tap_cfg = m.Meltano.TapConfig(
                tap_type=tap_type,
                connection_config=connection_config,
                stream_config=stream_config if stream_config is not None else {},
            )
            instance = m.Meltano.TapInstance(
                tap_type=tap_type,
                settings=tap_cfg,
                tap_id=f"{tap_type}_auto",
            )
            return r[m.Meltano.TapInstance].ok(instance)
        except c.Meltano.OPERATION_ERRORS as e:
            return r[m.Meltano.TapInstance].fail(f"Failed to create tap: {e}")

    def generate_catalog(
        self,
        tap_instance: m.Meltano.TapInstance,
    ) -> p.Result[t.RecursiveContainerMapping]:
        """Generate Singer catalog by discovering streams from the tap."""
        discovery = self.discover_streams(tap_instance)
        if discovery.failure:
            return r[t.RecursiveContainerMapping].fail(
                discovery.error or "Catalog generation failed"
            )
        raw = discovery.value
        streams: list[t.RecursiveContainerMapping] = []
        for s in self._extract_raw_streams(raw):
            name = str(s.get("stream_name", ""))
            if name in self._stream_registry:
                entry_r = self._create_catalog_entry_from_stream(
                    self._stream_registry[name],
                )
                if entry_r.success:
                    streams.append(entry_r.value)
        catalog: t.RecursiveContainerMapping = {"version": 1, "streams": streams}
        return r[t.RecursiveContainerMapping].ok(catalog)

    def get_stream_by_name(
        self,
        tap_instance: m.Meltano.TapInstance,
        stream_name: str,
    ) -> p.Result[t.RecursiveContainerMapping]:
        """Get stream definition by name."""
        discovery = self.discover_streams(tap_instance)
        if discovery.failure:
            return r[t.RecursiveContainerMapping].fail(
                discovery.error or "Discovery failed"
            )
        for stream in self._extract_raw_streams(discovery.value):
            if stream.get("stream_name") == stream_name:
                result_stream: t.RecursiveContainerMapping = {
                    **stream,
                    "name": stream_name,
                }
                return r[t.RecursiveContainerMapping].ok(result_stream)
        return r[t.RecursiveContainerMapping].fail(f"Stream '{stream_name}' not found")

    def list_streams(self, tap_instance: m.Meltano.TapInstance) -> t.StrSequence:
        """List stream names available in tap instance."""
        discovery = self.discover_streams(tap_instance)
        if discovery.failure:
            return []
        return [
            str(s.get("stream_name", ""))
            for s in self._extract_raw_streams(discovery.value)
        ]

    @staticmethod
    def _extract_raw_streams(
        raw: t.RecursiveContainerMapping,
    ) -> list[t.RecursiveContainerMapping]:
        """Extract stream dicts from a discovery result mapping."""
        if isinstance(raw, dict):
            raw_val = raw.get("streams")
            if isinstance(raw_val, list):
                return [s for s in raw_val if isinstance(s, dict)]
        return []


__all__: list[str] = ["FlextMeltanoAbstractions"]
