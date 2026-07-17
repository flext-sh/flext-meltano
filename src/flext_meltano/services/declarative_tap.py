"""Declarative Singer tap builder — the only tap-side ``singer_sdk`` bridge.

Turns a declarative ``m.Meltano.TapSpec`` plus a consumer ``p.Meltano.RecordFetcher``
into a real ``singer_sdk`` tap with a working flat Singer CLI. Consumer tap
projects declare streams as data and fetch records with their own domain library;
they never import ``singer_sdk`` — this module is the single place that does.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, override

from singer_sdk import Stream, Tap

from flext_meltano import m, p, t

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping


class FlextMeltanoDeclarativeTap:
    """Build and run a ``singer_sdk`` tap from declarative FLEXT specs."""

    class Instance:
        """Adapt a declarative Singer tap class to the internal runtime contract."""

        def __init__(self, tap_class: type[Tap]) -> None:
            """Store the built Singer tap class used for flat-CLI dispatch."""
            self._tap_class = tap_class

        @property
        def settings(self) -> t.JsonMapping:
            """Declarative taps carry no eager config; the CLI parses it."""
            empty: t.JsonMapping = {}
            return empty

        def run_cli(self, args: t.StrSequence, prog_name: str) -> int:
            """Run the Singer flat CLI (``--config/--discover/--catalog/--state``)."""
            command = self._tap_class.get_singer_command()
            try:
                _ = command.main(
                    args=list(args),
                    prog_name=prog_name,
                    standalone_mode=False,
                )
            except SystemExit as exc:
                return exc.code if isinstance(exc.code, int) else 1
            return 0

        def discover_streams(
            self,
        ) -> t.SequenceOf[p.Meltano.SingerStreamInfo]:
            """Discover streams through a config-free tap instance."""
            streams: t.SequenceOf[p.Meltano.SingerStreamInfo] = self._tap_class(
                config=None,
                validate_config=False,
            ).discover_streams()
            return streams

        def sync_all(self) -> None:
            """Direct sync is CLI-driven for declarative taps."""

    @classmethod
    def build(
        cls,
        spec: m.Meltano.TapSpec,
        fetcher: p.Meltano.RecordFetcher,
    ) -> p.Meltano.SingerTapInstance:
        """Return a Singer tap instance driven by ``spec`` and ``fetcher``."""
        stream_specs = tuple(spec.streams)

        class _DeclarativeStream(Stream):
            """A Singer stream whose records come from the FLEXT fetcher."""

            def __init__(
                self,
                tap: Tap,
                stream_spec: m.Meltano.StreamSpec,
                config: t.JsonMapping,
            ) -> None:
                super().__init__(
                    tap,
                    schema=dict(stream_spec.json_schema),
                    name=stream_spec.name,
                )
                # Assign singer_sdk Stream's backing fields directly (its property setters do the same); a bare `self.<prop> =` reads as an untagged member override that cannot take @override.
                self._primary_keys: t.StrSequence = list(stream_spec.primary_keys)
                self._replication_key: str | None = stream_spec.replication_key
                self._config: t.JsonMapping = config

            @override
            def get_records(
                self,
                context: Mapping[str, object] | None,
            ) -> Iterable[t.JsonMapping]:
                _ = context
                request = m.Meltano.FetchRequest(
                    stream_name=self.name,
                    config=self._config,
                )
                result = fetcher.fetch(request)
                return list(result.value.records) if result.success else []

        class _DeclarativeTap(Tap):
            """A Singer tap that discovers the declared streams."""

            @override
            def discover_streams(self) -> list[Stream]:
                config: t.JsonMapping = dict(self.config)
                return [
                    _DeclarativeStream(self, stream_spec, config)
                    for stream_spec in stream_specs
                ]

        _DeclarativeTap.name = spec.tap_name
        _DeclarativeTap.config_jsonschema = dict(spec.config_jsonschema)
        return cls.Instance(_DeclarativeTap)


__all__: list[str] = ["FlextMeltanoDeclarativeTap"]
