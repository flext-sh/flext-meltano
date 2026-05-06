"""Real tests for the flat public tap abstraction surface."""

from __future__ import annotations

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

        assert result.success
        assert result.value.tap_type == "tap-postgres"
        assert result.value.tap_version == "v1.2.0"
        assert result.value.stream_config["users"] == "selected"

    def test_build_tap_instance_returns_public_mapping(self) -> None:
        """The facade should expose the tap instance through the public mapping shape."""
        settings = m.Meltano.TapConfig(
            tap_type="tap-csv",
            connection_config={"file_path": "data.csv"},
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-csv",
            settings=settings,
            tap_id="tap_csv_123",
            status="initialized",
        )

        payload = meltano.build_tap_instance(tap_instance)

        assert payload["tap_id"] == "tap_csv_123"
        assert payload["tap_type"] == "tap-csv"

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

        assert result.success
        assert result.value.tap_type == "tap-postgres"
        assert result.value.tap_id == "tap-postgres_auto"
        assert result.value.settings.tap_version == "1.2.3"
        assert result.value.settings.stream_config["users"] == "selected"

    def test_tap_factory_returns_bound_service(self) -> None:
        """The flat tap factory should bind the returned facade to the source name."""
        result = meltano.tap("tap-csv")

        assert result.success
        assert result.value.source_name == "tap-csv"
        assert result.value.sink_name is None
        assert result.value.transformation_name is None
