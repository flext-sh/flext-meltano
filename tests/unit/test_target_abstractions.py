"""Behavioral tests for the public target abstraction surface of FlextMeltano.

Exercises only the observable contract of the flat ``meltano`` facade:
``target``, ``configure_sink``, ``create_flext_target``, ``create_sink_instance``
and ``validate_sink_config`` — asserting returned ``r[T]`` outcomes and public
model state, never private attributes or internal collaborators.
"""

from __future__ import annotations

import pytest

from flext_meltano import meltano
from tests.models import m
from tests.typings import t


class TestsFlextMeltanoTargetAbstractions:
    """Validate target-related behavior through the current public facade."""

    @pytest.fixture
    def sink_config(self) -> m.Meltano.DataSinkConfig:
        """Return a valid data-sink configuration modelled via the public m.* facade."""
        return m.Meltano.DataSinkConfig(
            sink_type="target-jsonl",
            connection_config={"path": "output.jsonl"},
        )

    def test_target_factory_binds_sink_name_and_leaves_other_roles_unset(
        self,
    ) -> None:
        """target() returns a success bound to the sink name, source/xform unset."""
        result = meltano.target("target-jsonl")

        assert result.success
        service = result.value
        assert service.sink_name == "target-jsonl"
        assert service.source_name is None
        assert service.transformation_name is None

    @pytest.mark.parametrize(
        "sink_name",
        ["target-jsonl", "target-postgres", "target-snowflake"],
    )
    def test_target_factory_echoes_requested_sink_name(self, sink_name: str) -> None:
        """target() binds exactly the requested sink name for any target kind."""
        result = meltano.target(sink_name)

        assert result.success
        assert result.value.sink_name == sink_name

    def test_configure_sink_derives_definition_from_config(
        self,
        sink_config: m.Meltano.DataSinkConfig,
    ) -> None:
        """configure_sink() maps a config to a configured DataSinkDefinition."""
        result = meltano.configure_sink(sink_config)

        assert result.success
        definition = result.value
        assert definition.sink_name == "target-jsonl_sink"
        assert definition.sink_type == "target-jsonl"
        assert definition.settings["path"] == "output.jsonl"
        assert definition.status == "configured"

    def test_configure_sink_is_deterministic_for_equal_input(
        self,
        sink_config: m.Meltano.DataSinkConfig,
    ) -> None:
        """configure_sink() yields the same public definition for equal input."""
        first = meltano.configure_sink(sink_config)
        second = meltano.configure_sink(sink_config)

        assert first.success
        assert second.success
        assert first.value.sink_name == second.value.sink_name
        assert first.value.sink_type == second.value.sink_type
        assert first.value.settings == second.value.settings
        assert first.value.status == second.value.status

    def test_create_flext_target_from_mapping_builds_sink_instance(self) -> None:
        """create_flext_target() accepts a plain mapping and builds a sink instance."""
        payload: t.JsonMapping = {
            "sink_type": "target-jsonl",
            "connection_config": {"path": "output.jsonl"},
        }

        result = meltano.create_flext_target(payload)

        assert result.success
        instance = result.value
        assert instance.sink_type == "target-jsonl"
        assert instance.settings.sink_type == "target-jsonl"
        assert instance.settings.connection_config["path"] == "output.jsonl"

    def test_create_flext_target_accepts_config_model_directly(
        self,
        sink_config: m.Meltano.DataSinkConfig,
    ) -> None:
        """create_flext_target() passes an existing config model straight through."""
        result = meltano.create_flext_target(sink_config)

        assert result.success
        assert result.value.settings == sink_config

    def test_create_flext_target_rejects_mapping_missing_sink_type(self) -> None:
        """create_flext_target() fails with a descriptive error on invalid input."""
        result = meltano.create_flext_target({"connection_config": {"path": "x"}})

        assert not result.success
        assert result.error is not None
        assert "Invalid target settings" in result.error

    def test_create_sink_instance_matches_create_flext_target(
        self,
        sink_config: m.Meltano.DataSinkConfig,
    ) -> None:
        """create_sink_instance() and create_flext_target() agree for a model input."""
        via_instance = meltano.create_sink_instance(sink_config)
        via_target = meltano.create_flext_target(sink_config)

        assert via_instance.success
        assert via_target.success
        assert via_instance.value.sink_type == via_target.value.sink_type
        assert via_instance.value.settings == via_target.value.settings
        assert via_instance.value.status == via_target.value.status

    def test_validate_sink_config_accepts_valid_config(
        self,
        sink_config: m.Meltano.DataSinkConfig,
    ) -> None:
        """validate_sink_config() reports success for a well-formed config."""
        result = meltano.validate_sink_config(sink_config)

        assert result.success
        assert result.value is True


__all__: list[str] = ["TestsFlextMeltanoTargetAbstractions"]
