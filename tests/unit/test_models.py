"""Behavioral tests for the Meltano models public contract.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import c, m

__all__ = ["TestsFlextMeltanoModelsUnit"]


class TestsFlextMeltanoModelsUnit:
    """Public-contract tests for Meltano tap/target/stream models."""

    # ---- TapConfig ---------------------------------------------------------

    def test_tap_config_exposes_defaults_for_optional_fields(self) -> None:
        settings = m.Meltano.TapConfig(
            tap_type="tap-postgres", connection_config={"host": "localhost"}
        )
        tm.that(settings.tap_type, eq="tap-postgres")
        tm.that(settings.connection_config, eq={"host": "localhost"})
        tm.that(settings.stream_config, empty=True)
        tm.that(settings.tap_version, eq="latest")

    def test_tap_config_retains_full_supplied_state(self) -> None:
        settings = m.Meltano.TapConfig(
            tap_type="tap-mysql",
            connection_config={
                "host": "db.example.com",
                "port": 3306,
                "user": "etl_user",
                "password": "secret",
            },
            stream_config={"users": "public", "orders": "commerce"},
            tap_version="1.0.0",
        )
        tm.that(settings.tap_type, eq="tap-mysql")
        tm.that(settings.connection_config["host"], eq="db.example.com")
        tm.that(settings.connection_config["port"], eq=3306)
        tm.that(settings.stream_config, has="users")
        tm.that(settings.tap_version, eq="1.0.0")

    def test_tap_config_computed_fields_derive_from_state(self) -> None:
        settings = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost", "port": 5432},
            stream_config={"users": "public"},
            tap_version="2.1.0",
        )
        # config_size = connection_config keys + stream_config keys
        tm.that(settings.config_size, eq=3)
        tm.that(settings.has_stream_config, eq=True)
        tm.that(settings.tap_identifier, eq="tap-postgres:2.1.0")

    def test_tap_config_has_stream_config_false_when_absent(self) -> None:
        settings = m.Meltano.TapConfig(
            tap_type="tap-postgres", connection_config={"host": "localhost"}
        )
        tm.that(settings.has_stream_config, eq=False)
        tm.that(settings.config_size, eq=1)

    @pytest.mark.parametrize("blank_tap_type", ["", "   "])
    def test_tap_config_rejects_blank_tap_type(self, blank_tap_type: str) -> None:
        with pytest.raises(c.ValidationError, match="tap_type cannot be empty"):
            m.Meltano.TapConfig(
                tap_type=blank_tap_type, connection_config={"host": "localhost"}
            )

    def test_tap_config_rejects_empty_connection_config(self) -> None:
        with pytest.raises(
            c.ValidationError, match="Connection configuration cannot be empty"
        ):
            m.Meltano.TapConfig(tap_type="tap-postgres", connection_config={})

    def test_tap_config_rejects_non_mapping_connection_config(self) -> None:
        with pytest.raises(c.ValidationError, match="valid dictionary"):
            m.Meltano.TapConfig.model_validate({
                "tap_type": "tap-postgres",
                "connection_config": "invalid",
            })

    # ---- TargetConfig ------------------------------------------------------

    def test_target_config_exposes_defaults_for_optional_fields(self) -> None:
        settings = m.Meltano.TargetConfig(target_type="target-csv")
        tm.that(settings.target_type, eq="target-csv")
        tm.that(settings.connection_config, empty=True)
        tm.that(settings.batch_size, none=True)
        tm.that(settings.batch_wait_limit, none=True)
        tm.that(settings.target_version, eq="latest")

    def test_target_config_retains_full_supplied_state(self) -> None:
        settings = m.Meltano.TargetConfig(
            target_type="target-postgres",
            connection_config={
                "host": "localhost",
                "port": 5432,
                "database": "analytics",
                "user": "etl_user",
                "password": "etl_pass",
            },
            batch_size=1000,
            batch_wait_limit=30.0,
        )
        tm.that(settings.target_type, eq="target-postgres")
        tm.that(settings.connection_config["database"], eq="analytics")
        tm.that(settings.batch_size, eq=1000)
        batch_wait_limit = settings.batch_wait_limit
        assert batch_wait_limit is not None
        tm.that(abs(batch_wait_limit - 30.0), lt=1e-9)

    def test_target_config_computed_fields_derive_from_state(self) -> None:
        settings = m.Meltano.TargetConfig(
            target_type="target-postgres",
            connection_config={"host": "localhost", "port": 5432},
            target_version="3.0.0",
        )
        tm.that(settings.config_size, eq=2)
        tm.that(settings.has_connection_config, eq=True)
        tm.that(settings.target_identifier, eq="target-postgres:3.0.0")

    def test_target_config_has_connection_config_false_when_empty(self) -> None:
        settings = m.Meltano.TargetConfig(target_type="target-csv")
        tm.that(settings.has_connection_config, eq=False)
        tm.that(settings.config_size, eq=0)

    def test_target_config_rejects_blank_target_type(self) -> None:
        with pytest.raises(c.ValidationError, match="target_type cannot be empty"):
            m.Meltano.TargetConfig(target_type="")

    def test_target_config_rejects_non_integer_batch_size(self) -> None:
        with pytest.raises(c.ValidationError, match="valid integer"):
            m.Meltano.TargetConfig.model_validate({
                "target_type": "target-csv",
                "batch_size": "invalid",
            })

    # ---- StreamInfo --------------------------------------------------------

    def test_stream_info_exposes_defaults_for_optional_fields(self) -> None:
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object", "properties": "id"},
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tm.that(stream.stream_name, eq="users")
        tm.that(stream.stream_schema["type"], eq="object")
        tm.that(stream.status, eq=c.Meltano.StreamStatus.INITIALIZED)
        tm.that(stream.records_loaded, eq=0)
        tm.that(stream.batches_processed, eq=0)
        tm.that(stream.stream_created_at, eq="2025-01-01T00:00:00Z")

    def test_stream_info_retains_full_supplied_state(self) -> None:
        stream = m.Meltano.StreamInfo(
            stream_name="orders",
            stream_schema={"type": "object", "properties": "id,order_date,amount"},
            key_properties=["id"],
            replication_method="FULL_TABLE",
            replication_key="order_date",
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tm.that(stream.stream_name, eq="orders")
        tm.that(stream.key_properties, has="id")
        tm.that(stream.replication_method, eq="FULL_TABLE")
        tm.that(stream.replication_key, eq="order_date")

    def test_stream_info_computed_fields_for_unprocessed_stream(self) -> None:
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object"},
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tm.that(stream.average_records_per_batch, eq=0.0)
        tm.that(stream.has_processed_data, eq=False)
        tm.that(stream.processing_status, eq=str(c.Meltano.StreamStatus.PENDING))

    def test_stream_info_average_records_per_batch_divides_totals(self) -> None:
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object"},
            stream_created_at="2025-01-01T00:00:00Z",
            records_loaded=10,
            batches_processed=2,
        )
        tm.that(stream.average_records_per_batch, eq=5.0)
        tm.that(stream.has_processed_data, eq=True)

    @pytest.mark.parametrize(
        ("status", "records_loaded", "batches_processed", "expected"),
        [
            (
                c.Meltano.StreamStatus.COMPLETED,
                4,
                1,
                str(c.Meltano.StreamStatus.SUCCESS),
            ),
            (c.Meltano.StreamStatus.ERROR, 0, 0, str(c.Meltano.StreamStatus.FAILED)),
            (
                c.Meltano.StreamStatus.PROCESSING,
                3,
                1,
                str(c.Meltano.StreamStatus.IN_PROGRESS),
            ),
            (
                c.Meltano.StreamStatus.INITIALIZED,
                0,
                0,
                str(c.Meltano.StreamStatus.PENDING),
            ),
        ],
    )
    def test_stream_info_processing_status_reflects_progress(
        self, status: str, records_loaded: int, batches_processed: int, expected: str
    ) -> None:
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object"},
            stream_created_at="2025-01-01T00:00:00Z",
            status=status,
            records_loaded=records_loaded,
            batches_processed=batches_processed,
        )
        tm.that(stream.processing_status, eq=expected)

    def test_stream_info_rejects_empty_stream_name(self) -> None:
        with pytest.raises(c.ValidationError, match="at least 1 character"):
            m.Meltano.StreamInfo(
                stream_name="",
                stream_schema={"type": "object"},
                stream_created_at="2025-01-01T00:00:00Z",
            )

    def test_stream_info_rejects_records_without_batches(self) -> None:
        with pytest.raises(
            c.ValidationError, match="Records loaded but no batches processed"
        ):
            m.Meltano.StreamInfo(
                stream_name="users",
                stream_schema={"type": "object"},
                stream_created_at="2025-01-01T00:00:00Z",
                records_loaded=5,
                batches_processed=0,
            )

    def test_stream_info_rejects_unknown_status(self) -> None:
        with pytest.raises(c.ValidationError, match="Status must be one of"):
            m.Meltano.StreamInfo(
                stream_name="users",
                stream_schema={"type": "object"},
                stream_created_at="2025-01-01T00:00:00Z",
                status="not-a-real-status",
            )

    def test_stream_info_rejects_non_mapping_schema(self) -> None:
        with pytest.raises(c.ValidationError, match="valid dictionary"):
            m.Meltano.StreamInfo.model_validate({
                "stream_name": "users",
                "stream_schema": "invalid",
                "stream_created_at": "2025-01-01T00:00:00Z",
            })

    # ---- Composition -------------------------------------------------------

    def test_tap_and_target_configs_are_independent(self) -> None:
        tap_config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "source.db.com", "port": 5432},
        )
        target_config = m.Meltano.TargetConfig(
            target_type="target-postgres",
            connection_config={"host": "target.db.com", "port": 5432},
        )
        tm.that(tap_config.connection_config["host"], eq="source.db.com")
        tm.that(target_config.connection_config["host"], eq="target.db.com")
        tm.that(tap_config.tap_identifier, eq="tap-postgres:latest")
        tm.that(target_config.target_identifier, eq="target-postgres:latest")

    def test_stream_name_maps_into_tap_stream_config(self) -> None:
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object", "properties": "id"},
            key_properties=["id"],
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tap_config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
            stream_config={"users": "public"},
        )
        tm.that(tap_config.stream_config, has=stream.stream_name)
        tm.that(stream.key_properties, has="id")
