"""Real tests for the flat public target abstraction surface."""

from __future__ import annotations

from flext_meltano import meltano
from tests.models import m
from tests.utilities import u


class TestsFlextMeltanoTargetAbstractions:
    """Validate target-related behavior through the current public facade."""

    def test_target_factory_returns_bound_service(self) -> None:
        """The flat target factory should bind the returned facade to the sink name."""
        result = meltano.target("target-jsonl")

        assert result.success
        assert result.value.source_name is None
        assert result.value.sink_name == "target-jsonl"
        assert result.value.transformation_name is None

    def test_configure_sink_returns_sink_definition(self) -> None:
        """The facade should convert a sink config into a configured sink definition."""
        sink_config = m.Meltano.DataSinkConfig(
            sink_type="target-jsonl",
            connection_config={"path": "output.jsonl"},
        )

        result = meltano.configure_sink(sink_config)

        assert result.success
        assert result.value.sink_name == "target-jsonl_sink"
        assert result.value.sink_type == "target-jsonl"
        assert result.value.settings["path"] == "output.jsonl"

    def test_create_flext_target_from_mapping(self) -> None:
        """The facade should create a sink instance from a plain mapping payload."""
        result = meltano.create_flext_target({
            "sink_type": "target-jsonl",
            "connection_config": {"path": "output.jsonl"},
        })

        assert result.success
        assert result.value.sink_type == "target-jsonl"
        assert result.value.settings.sink_type == "target-jsonl"
        assert result.value.settings.connection_config["path"] == "output.jsonl"

    def test_utility_helper_methods_remain_available(self) -> None:
        """The test utility layer remains usable for current flat target flows."""
        timestamp = u.generate_iso_timestamp()

        assert isinstance(timestamp, str)
        assert "T" in timestamp
