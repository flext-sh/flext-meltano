"""FLEXT Pipeline Abstractions - Tap-specific Meltano runtime operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Self

from flext_meltano import c, e, m, p, r, t
from flext_meltano.services.abstractions_base import FlextMeltanoAbstractionsBase


class FlextMeltanoAbstractions(FlextMeltanoAbstractionsBase):
    """Core abstraction wrapping the imported Meltano runtime with r[T] results."""

    @classmethod
    def create_abstractions_instance(cls) -> p.Result[Self]:
        """Create a FlextMeltanoAbstractions instance."""
        instance: Self = cls()
        ok_result: p.Result[Self] = r.ok(instance)
        return ok_result

    # -- Tap-specific operations (discovery, sync, catalog) --

    def process_tap_config(
        self, settings: p.Meltano.TapConfig
    ) -> p.Result[p.Meltano.TapConfig]:
        """Validate and return tap configuration."""
        return r[p.Meltano.TapConfig].ok(settings)

    def build_tap_instance(self, tap_instance: p.Meltano.TapInstance) -> t.JsonMapping:
        """Build tap instance representation."""
        return {
            c.Meltano.PayloadKey.TAP_ID: tap_instance.tap_id,
            c.Meltano.PayloadKey.TAP_TYPE: tap_instance.tap_type,
        }

    def discover_streams(
        self, tap_instance: p.Meltano.TapInstance
    ) -> p.Result[t.JsonMapping]:
        """Discover available streams via ``meltano select --list``."""

        def _run_discover_streams() -> p.Result[t.JsonMapping]:
            cmd_result = self._run_meltano([
                c.Meltano.CMD_SELECT,
                tap_instance.tap_type,
                c.Meltano.CMD_LIST_OPTION,
                c.Meltano.CMD_ALL_OPTION,
            ])
            if cmd_result.failure:
                return r[t.JsonMapping].fail(
                    cmd_result.error or c.Meltano.ERROR_STREAM_DISCOVERY_FAILED
                )
            stream_defs: t.JsonValueList = []
            for line in cmd_result.value.splitlines():
                name = line.strip()
                if name and not name.startswith("["):
                    stream_defs.append({
                        c.Meltano.PayloadKey.STREAM_NAME: name,
                        c.Meltano.PayloadKey.TAP_STREAM_ID: name,
                    })
                    if name not in self._stream_registry:
                        self._stream_registry[name] = m.Meltano.StreamDefinition(
                            stream_name=name,
                            stream_schema={
                                c.Meltano.SchemaKey.TYPE: c.Meltano.SchemaKey.OBJECT,
                                c.Meltano.SchemaKey.PROPERTIES: {},
                            },
                            source_type=tap_instance.tap_type,
                        )
            payload: t.JsonDict = {c.Meltano.PayloadKey.STREAMS: stream_defs}
            return r[t.JsonMapping].ok(payload)

        try:
            return _run_discover_streams()
        except c.Meltano.OPERATION_ERRORS as exc:
            self.logger.exception(
                c.Meltano.LOG_MESSAGE_DISCOVER_STREAMS_FAILED, error=str(exc)
            )
            return e.fail_operation(
                c.Meltano.OPERATION_DISCOVER_STREAMS, exc, result_type=r[t.JsonMapping]
            )

    def sync_stream(
        self,
        tap_instance: p.Meltano.TapInstance,
        stream_name: str,
        target_config: p.Meltano.TargetConfig | None = None,
    ) -> p.Result[t.JsonMapping]:
        """Sync a single stream via ``meltano elt`` with stream selection."""

        def _run_sync_stream() -> p.Result[t.JsonMapping]:
            loader_name = (
                target_config.target_type
                if target_config is not None
                else c.IDENTIFIER_UNKNOWN
            )
            cmd_args = [
                c.Meltano.CMD_ELT,
                tap_instance.tap_type,
                loader_name,
                c.Meltano.CMD_SELECT_OPTION,
                stream_name,
            ]
            cmd_result = self._run_meltano(cmd_args)
            status = (
                c.Meltano.StreamStatus.COMPLETED
                if cmd_result.success
                else c.Meltano.StreamStatus.FAILED
            )
            result: t.JsonDict = {
                c.Meltano.PayloadKey.STREAM_NAME: stream_name,
                c.Meltano.PayloadKey.STATUS: status,
                c.Meltano.PayloadKey.TARGET_LOADED: target_config is not None,
            }
            if cmd_result.failure:
                return r[t.JsonMapping].fail(
                    cmd_result.error or c.Meltano.ERROR_STREAM_SYNC_FAILED
                )
            return r[t.JsonMapping].ok(result)

        try:
            return _run_sync_stream()
        except c.Meltano.OPERATION_ERRORS as exc:
            self.logger.exception(
                c.Meltano.LOG_MESSAGE_SYNC_STREAM_FAILED,
                stream=stream_name,
                error=str(exc),
            )
            return e.fail_operation(
                f"{c.Meltano.OPERATION_SYNC_STREAM} {stream_name}",
                exc,
                result_type=r[t.JsonMapping],
            )

    def create_tap_from_config(
        self,
        tap_type: str,
        connection_config: t.JsonMapping,
        stream_config: t.JsonMapping | None = None,
        tap_version: str = "1.0.0",
    ) -> p.Result[p.Meltano.TapInstance]:
        """Create a TapInstance from configuration."""
        try:
            tap_cfg = m.Meltano.TapConfig(
                tap_type=tap_type,
                connection_config=connection_config,
                stream_config=stream_config if stream_config is not None else {},
                tap_version=tap_version,
            )
            instance = m.Meltano.TapInstance(
                tap_type=tap_type,
                settings=tap_cfg,
                tap_id=(f"{tap_type}_{c.Meltano.PAYLOAD_TAP_ID_AUTO_SUFFIX}"),
            )
            return r[p.Meltano.TapInstance].ok(instance)
        except c.Meltano.OPERATION_ERRORS as exc:
            return e.fail_operation(
                c.Meltano.OPERATION_CREATE_TAP,
                exc,
                result_type=r[p.Meltano.TapInstance],
            )

    def generate_catalog(
        self, tap_instance: p.Meltano.TapInstance
    ) -> p.Result[t.JsonMapping]:
        """Generate Singer catalog by discovering streams from the tap."""
        discovery = self.discover_streams(tap_instance)
        if discovery.failure:
            return r[t.JsonMapping].fail(
                discovery.error or c.Meltano.ERROR_CATALOG_GENERATION_FAILED
            )
        raw = discovery.value
        streams: list[p.Meltano.SingerCatalogEntry] = []
        for s in self._extract_raw_streams(raw):
            name = str(s.get(c.Meltano.PayloadKey.STREAM_NAME, c.DEFAULT_EMPTY_STRING))
            if name in self._stream_registry:
                entry_r = self._create_catalog_entry_from_stream(
                    self._stream_registry[name]
                )
                if entry_r.success:
                    streams.append(entry_r.value)
        catalog_model = m.Meltano.SingerCatalog(streams=streams)
        catalog_payload = t.json_dict_adapter().validate_python(
            catalog_model.model_dump(mode="json", by_alias=True)
        )
        catalog: t.JsonDict = {
            c.Meltano.PayloadKey.VERSION: c.Meltano.PAYLOAD_SINGER_CATALOG_VERSION,
            c.Meltano.PayloadKey.STREAMS: catalog_payload[c.Meltano.PayloadKey.STREAMS],
        }
        return r[t.JsonMapping].ok(catalog)

    def fetch_stream_by_name(
        self, tap_instance: p.Meltano.TapInstance, stream_name: str
    ) -> p.Result[t.JsonMapping]:
        """Get stream definition by name."""
        discovery = self.discover_streams(tap_instance)
        if discovery.failure:
            return r[t.JsonMapping].fail(
                discovery.error or c.Meltano.ERROR_DISCOVERY_FAILED
            )
        for stream in self._extract_raw_streams(discovery.value):
            if stream.get(c.Meltano.PayloadKey.STREAM_NAME) == stream_name:
                result_stream: t.JsonDict = {
                    **stream,
                    c.Meltano.PayloadKey.NAME: stream_name,
                }
                return r[t.JsonMapping].ok(result_stream)
        return e.fail_not_found(
            c.Meltano.PAYLOAD_STREAM_ENTITY, stream_name, result_type=r[t.JsonMapping]
        )

    def list_streams(self, tap_instance: p.Meltano.TapInstance) -> t.StrSequence:
        """List stream names available in tap instance."""
        discovery = self.discover_streams(tap_instance)
        if discovery.failure:
            return []
        return [
            str(s.get(c.Meltano.PayloadKey.STREAM_NAME, c.DEFAULT_EMPTY_STRING))
            for s in self._extract_raw_streams(discovery.value)
        ]

    @staticmethod
    def _extract_raw_streams(raw: t.JsonMapping) -> t.SequenceOf[t.JsonDict]:
        """Extract stream dicts from a discovery result mapping."""
        return t.json_dict_sequence_adapter().validate_python(
            raw.get(c.Meltano.PayloadKey.STREAMS, [])
        )


__all__: list[str] = ["FlextMeltanoAbstractions"]
