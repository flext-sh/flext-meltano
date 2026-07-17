"""Real tests for the declarative Singer tap builder (flat Singer CLI)."""

from __future__ import annotations

import contextlib
import io
import json
from pathlib import Path

from flext_tests import tm

from flext_meltano import m, p, r, t
from flext_meltano.services.declarative_tap import FlextMeltanoDeclarativeTap


class TestsFlextMeltanoDeclarativeTap:
    """Validate the declarative tap through its real flat Singer CLI surface."""

    class _Fetcher:
        """A record fetcher that echoes one record derived from the config."""

        def fetch(
            self,
            request: m.Meltano.FetchRequest,
        ) -> p.Result[m.Meltano.FetchResult]:
            base_dn = request.config.get("base_dn", "")
            record: t.JsonMapping = {
                "dn": f"cn={request.stream_name},{base_dn}",
                "updated_at": "2026-07-17T00:00:00Z",
            }
            return r[m.Meltano.FetchResult].ok(
                m.Meltano.FetchResult(records=[record]),
            )

    @staticmethod
    def _spec() -> m.Meltano.TapSpec:
        stream = m.Meltano.StreamSpec(
            name="users",
            json_schema={
                "type": "object",
                "properties": {
                    "dn": {"type": "string"},
                    "updated_at": {"type": "string", "format": "date-time"},
                },
            },
            primary_keys=("dn",),
            replication_key="updated_at",
        )
        return m.Meltano.TapSpec(
            tap_name="tap-sample",
            config_jsonschema={
                "type": "object",
                "properties": {"base_dn": {"type": "string"}},
            },
            streams=(stream,),
        )

    def test_discover_emits_catalog_with_declared_stream(
        self,
        tmp_path: Path,
    ) -> None:
        """A flat ``--config --discover`` run emits the declared stream catalog."""
        instance = FlextMeltanoDeclarativeTap.build(self._spec(), self._Fetcher())
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"base_dn": "dc=example"}))

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            exit_code = instance.run_cli(
                ["--config", str(config_path), "--discover"],
                "tap-sample",
            )

        catalog = json.loads(buffer.getvalue())
        stream = catalog["streams"][0]
        tm.that(exit_code, eq=0)
        tm.that(stream["tap_stream_id"], eq="users")
        tm.that(stream["key_properties"], eq=["dn"])
        tm.that(stream["replication_key"], eq="updated_at")

    def test_sync_emits_fetched_record(self, tmp_path: Path) -> None:
        """A flat ``--config`` run emits the fetcher's validated Singer record."""
        instance = FlextMeltanoDeclarativeTap.build(self._spec(), self._Fetcher())
        config_path = tmp_path / "config.json"
        config_path.write_text(json.dumps({"base_dn": "dc=example"}))

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            exit_code = instance.run_cli(
                ["--config", str(config_path)],
                "tap-sample",
            )

        messages: list[t.JsonMapping] = [
            t.json_dict_adapter().validate_json(line)
            for line in buffer.getvalue().splitlines()
        ]
        records = [
            message["record"] for message in messages if message.get("type") == "RECORD"
        ]
        tm.that(exit_code, eq=0)
        tm.that(
            records,
            has={
                "dn": "cn=users,dc=example",
                "updated_at": "2026-07-17T00:00:00Z",
            },
        )


__all__: list[str] = ["TestsFlextMeltanoDeclarativeTap"]
