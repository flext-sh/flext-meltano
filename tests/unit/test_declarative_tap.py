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
            record: t.JsonMapping = {"dn": f"cn={request.stream_name},{base_dn}"}
            return r[m.Meltano.FetchResult].ok(
                m.Meltano.FetchResult(records=[record]),
            )

    @staticmethod
    def _spec() -> m.Meltano.TapSpec:
        stream = m.Meltano.StreamSpec(
            name="users",
            json_schema={
                "type": "object",
                "properties": {"dn": {"type": "string"}},
            },
            primary_keys=("dn",),
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
        stream_ids = [entry["tap_stream_id"] for entry in catalog["streams"]]
        tm.that(exit_code, eq=0)
        tm.that(stream_ids, has="users")


__all__: list[str] = ["TestsFlextMeltanoDeclarativeTap"]
