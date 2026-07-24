"""Behavioral tests for the public target abstraction surface of FlextMeltano.

Exercises only the observable contract of the flat ``meltano`` facade:
``target``, ``configure_sink``, ``create_flext_target``, ``create_sink_instance``
and ``validate_sink_config`` — asserting returned ``r[T]`` outcomes and public
model state, never private attributes or internal collaborators.
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_meltano import meltano
from tests import m, p, t


class TestsFlextMeltanoTargetAbstractions:
    """Validate target-related behavior through the current public facade."""

    @pytest.fixture
    def sink_config(self) -> p.Meltano.DataSinkConfig:
        """Return a valid data-sink configuration modelled via the public m.* facade."""
        return m.Meltano.DataSinkConfig(
            sink_type="target-jsonl", connection_config={"path": "output.jsonl"}
        )

    def test_target_factory_binds_sink_name_and_leaves_other_roles_unset(self) -> None:
        """target() returns a success bound to the sink name, source/xform unset."""
        result = meltano.target("target-jsonl")

        tm.ok(result)
        service = result.value
        tm.that(service.sink_name, eq="target-jsonl")
        tm.that(service.source_name, none=True)
        tm.that(service.transformation_name, none=True)

    @pytest.mark.parametrize(
        "sink_name", ["target-jsonl", "target-postgres", "target-snowflake"]
    )
    def test_target_factory_echoes_requested_sink_name(self, sink_name: str) -> None:
        """target() binds exactly the requested sink name for any target kind."""
        result = meltano.target(sink_name)

        tm.ok(result)
        tm.that(result.value.sink_name, eq=sink_name)

    def test_configure_sink_derives_definition_from_config(
        self, sink_config: p.Meltano.DataSinkConfig
    ) -> None:
        """configure_sink() maps a config to a configured DataSinkDefinition."""
        result = meltano.configure_sink(sink_config)

        tm.ok(result)
        definition = result.value
        tm.that(definition.sink_name, eq="target-jsonl_sink")
        tm.that(definition.sink_type, eq="target-jsonl")
        tm.that(definition.settings["path"], eq="output.jsonl")
        tm.that(definition.status, eq="configured")

    def test_configure_sink_is_deterministic_for_equal_input(
        self, sink_config: p.Meltano.DataSinkConfig
    ) -> None:
        """configure_sink() yields the same public definition for equal input."""
        first = meltano.configure_sink(sink_config)
        second = meltano.configure_sink(sink_config)

        tm.ok(first)
        tm.ok(second)
        tm.that(first.value.sink_name, eq=second.value.sink_name)
        tm.that(first.value.sink_type, eq=second.value.sink_type)
        tm.that(first.value.settings, eq=second.value.settings)
        tm.that(first.value.status, eq=second.value.status)

    def test_create_flext_target_from_mapping_builds_sink_instance(self) -> None:
        """create_flext_target() accepts a plain mapping and builds a sink instance."""
        payload: t.JsonMapping = {
            "sink_type": "target-jsonl",
            "connection_config": {"path": "output.jsonl"},
        }

        result = meltano.create_flext_target(payload)

        tm.ok(result)
        instance = result.value
        tm.that(instance.sink_type, eq="target-jsonl")
        tm.that(instance.settings.sink_type, eq="target-jsonl")
        tm.that(instance.settings.connection_config["path"], eq="output.jsonl")

    def test_create_flext_target_accepts_config_model_directly(
        self, sink_config: p.Meltano.DataSinkConfig
    ) -> None:
        """create_flext_target() passes an existing config model straight through."""
        result = meltano.create_flext_target(sink_config)

        tm.ok(result)
        tm.that(result.value.settings.sink_type, eq=sink_config.sink_type)
        tm.that(
            result.value.settings.connection_config, eq=sink_config.connection_config
        )

    def test_create_flext_target_rejects_mapping_missing_sink_type(self) -> None:
        """create_flext_target() fails with a descriptive error on invalid input."""
        result = meltano.create_flext_target({"connection_config": {"path": "x"}})

        tm.fail(result)
        tm.that(result.error, none=False)
        tm.that(result.error, has="Invalid target settings")

    def test_create_sink_instance_matches_create_flext_target(
        self, sink_config: p.Meltano.DataSinkConfig
    ) -> None:
        """create_sink_instance() and create_flext_target() agree for a model input."""
        via_instance = meltano.create_sink_instance(sink_config)
        via_target = meltano.create_flext_target(sink_config)

        tm.ok(via_instance)
        tm.ok(via_target)
        tm.that(via_instance.value.sink_type, eq=via_target.value.sink_type)
        tm.that(
            via_instance.value.settings.connection_config,
            eq=via_target.value.settings.connection_config,
        )
        tm.that(via_instance.value.status, eq=via_target.value.status)

    def test_validate_sink_config_accepts_valid_config(
        self, sink_config: p.Meltano.DataSinkConfig
    ) -> None:
        """validate_sink_config() reports success for a well-formed config."""
        result = meltano.validate_sink_config(sink_config)

        tm.ok(result)
        tm.that(result.value, eq=True)


__all__: list[str] = ["TestsFlextMeltanoTargetAbstractions"]
