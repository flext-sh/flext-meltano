"""Enhanced comprehensive tests for m module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests.constants import c
from tests.models import m


class TestsFlextMeltanoModelsUnit:
    """Canonical tests for Meltano model validation and composition."""

    def test_tap_config_with_minimal_data(self) -> None:
        settings = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
        )
        tm.that(settings.tap_type, eq="tap-postgres")
        tm.that(settings.connection_config, eq={"host": "localhost"})
        tm.that(settings.stream_config, empty=True)
        tm.that(settings.tap_version, eq="latest")

    def test_tap_config_with_full_data(self) -> None:
        settings = m.Meltano.TapConfig(
            tap_type="tap-mysql",
            connection_config={
                "host": "db.example.com",
                "port": 3306,
                "user": "etl_user",
                "password": "secret",
            },
            stream_config={
                "users": "public",
                "orders": "commerce",
            },
            tap_version="1.0.0",
        )
        tm.that(settings.tap_type, eq="tap-mysql")
        tm.that(settings.connection_config["host"], eq="db.example.com")
        tm.that(settings.connection_config["port"], eq=3306)
        tm.that(settings.stream_config, has="users")
        tm.that(settings.tap_version, eq="1.0.0")

    def test_tap_config_validation_empty_tap_type(self) -> None:
        with pytest.raises(c.ValidationError, match="tap_type cannot be empty"):
            m.Meltano.TapConfig(tap_type="", connection_config={"host": "localhost"})

    def test_tap_config_validation_invalid_connection_config_type(self) -> None:
        with pytest.raises(
            c.ValidationError,
            match="Input should be a valid dictionary",
        ):
            m.Meltano.TapConfig.model_validate({
                "tap_type": "tap-postgres",
                "connection_config": "invalid",
            })

    def test_target_config_with_minimal_data(self) -> None:
        settings = m.Meltano.TargetConfig(target_type="target-csv")
        tm.that(settings.target_type, eq="target-csv")
        tm.that(settings.connection_config, empty=True)
        tm.that(settings.batch_size, none=True)
        tm.that(settings.batch_wait_limit, none=True)

    def test_target_config_with_full_data(self) -> None:
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
        if settings.batch_wait_limit is not None:
            tm.that(abs(settings.batch_wait_limit - 30.0), lt=1e-9)

    def test_target_config_validation_empty_target_type(self) -> None:
        with pytest.raises(c.ValidationError, match="target_type cannot be empty"):
            m.Meltano.TargetConfig(target_type="")

    def test_target_config_validation_invalid_batch_size_type(self) -> None:
        with pytest.raises(c.ValidationError, match="Input should be a valid integer"):
            m.Meltano.TargetConfig.model_validate({
                "target_type": "target-csv",
                "batch_size": "invalid",
            })

    def test_stream_info_with_minimal_data(self) -> None:
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object", "properties": "id"},
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tm.that(stream.stream_name, eq="users")
        tm.that(stream.stream_schema["type"], eq="object")
        tm.that(stream.status, eq="initialized")
        tm.that(stream.records_loaded, eq=0)
        tm.that(stream.batches_processed, eq=0)
        tm.that(stream.stream_created_at, eq="2025-01-01T00:00:00Z")

    def test_stream_info_with_full_data(self) -> None:
        stream = m.Meltano.StreamInfo(
            stream_name="orders",
            stream_schema={
                "type": "object",
                "properties": "id,order_date,amount",
            },
            key_properties=["id"],
            replication_method="FULL_TABLE",
            replication_key="order_date",
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tm.that(stream.stream_name, eq="orders")
        tm.that(stream.key_properties, eq=["id"])
        tm.that(stream.replication_method, eq="FULL_TABLE")
        tm.that(stream.replication_key, eq="order_date")

    def test_stream_info_validation_empty_stream_name(self) -> None:
        with pytest.raises(
            c.ValidationError,
            match="String should have at least 1 character",
        ):
            m.Meltano.StreamInfo(
                stream_name="",
                stream_schema={"type": "object"},
                stream_created_at="2025-01-01T00:00:00Z",
            )

    def test_stream_info_validation_invalid_schema_type(self) -> None:
        with pytest.raises(
            c.ValidationError,
            match="Input should be a valid dictionary",
        ):
            m.Meltano.StreamInfo.model_validate({
                "stream_name": "users",
                "stream_schema": "invalid",
                "stream_created_at": "2025-01-01T00:00:00Z",
            })

    def test_tap_and_target_config_integration(self) -> None:
        tap_config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "source.db.com", "port": 5432},
        )
        target_config = m.Meltano.TargetConfig(
            target_type="target-postgres",
            connection_config={"host": "target.db.com", "port": 5432},
        )
        tm.that(tap_config.tap_type, eq="tap-postgres")
        tm.that(target_config.target_type, eq="target-postgres")
        tm.that(tap_config.connection_config["host"], eq="source.db.com")
        tm.that(target_config.connection_config["host"], eq="target.db.com")

    def test_stream_info_with_tap_config_integration(self) -> None:
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
        tm.that(stream.key_properties, eq=["id"])
