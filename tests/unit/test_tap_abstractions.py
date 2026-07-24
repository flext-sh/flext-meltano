"""Real tests for the flat public tap abstraction surface."""

from __future__ import annotations

from flext_tests import tm

from flext_meltano import meltano
from tests import m


class TestsFlextMeltanoTapAbstractions:
    """Validate tap-related behavior through the current public facade."""

    def test_process_tap_config_returns_validated_config(self) -> None:
        """The facade should accept and return a valid tap config unchanged."""
        settings = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={
                "host": "localhost",
                "port": 5432,
                "database": "test_db",
            },
            stream_config={"users": "selected"},
            tap_version="v1.2.0",
        )

        result = meltano.process_tap_config(settings)

        tm.ok(result)
        tm.that(result.value.tap_type, eq="tap-postgres")
        tm.that(result.value.tap_version, eq="v1.2.0")
        tm.that(result.value.stream_config["users"], eq="selected")

    def test_build_tap_instance_returns_public_mapping(self) -> None:
        """The facade should expose the tap instance through the public mapping shape."""
        settings = m.Meltano.TapConfig(
            tap_type="tap-csv", connection_config={"file_path": "data.csv"}
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-csv",
            settings=settings,
            tap_id="tap_csv_123",
            status="initialized",
        )

        payload = meltano.build_tap_instance(tap_instance)

        tm.that(payload["tap_id"], eq="tap_csv_123")
        tm.that(payload["tap_type"], eq="tap-csv")

    def test_create_tap_from_config_builds_tap_instance(self) -> None:
        """The facade should build a tap instance directly from raw config."""
        result = meltano.create_tap_from_config(
            tap_type="tap-postgres",
            connection_config={
                "host": "localhost",
                "port": 5432,
                "database": "test_db",
                "username": "test_user",
            },
            stream_config={"users": "selected", "orders": "not_selected"},
            tap_version="1.2.3",
        )

        tm.ok(result)
        tm.that(result.value.tap_type, eq="tap-postgres")
        tm.that(result.value.tap_id, eq="tap-postgres_auto")
        tm.that(result.value.settings.tap_version, eq="1.2.3")
        tm.that(result.value.settings.stream_config["users"], eq="selected")

    def test_tap_factory_returns_bound_service(self) -> None:
        """The flat tap factory should bind the returned facade to the source name."""
        result = meltano.tap("tap-csv")

        tm.ok(result)
        tm.that(result.value.source_name, eq="tap-csv")
        tm.that(result.value.sink_name, none=True)
        tm.that(result.value.transformation_name, none=True)
