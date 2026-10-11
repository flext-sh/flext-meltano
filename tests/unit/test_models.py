"""Behavioral tests for the Meltano models public contract.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from types import MappingProxyType

import pytest

from tests import c, m, tm


class TestsFlextMeltanoModelsUnit:
    """Public-contract tests for Meltano tap/target/stream models."""

    @staticmethod
    def test_pipeline_context_mappings_are_normalized_and_immutable(
        tmp_path: Path,
    ) -> None:
        """Test pipeline context mappings are normalized and immutable."""
        project_root = tmp_path / "project"
        execution_context = m.Meltano.PipelineExecutionContext(
            project_root=f" {project_root} ",
            elt_context={"extractor_name": "tap-example"},
            extractor_name=" tap-example ",
            loader_name=" target-example ",
            execution_result={"success": True},
        )
        result_context = m.Meltano.PipelineResultContext(
            project_root=f" {project_root} ",
            execution_result={"success": True},
        )

        tm.that(execution_context.project_root, eq=str(project_root))
        tm.that(execution_context.extractor_name, eq="tap-example")
        tm.that(execution_context.loader_name, eq="target-example")
        tm.that(execution_context.elt_context, eq={"extractor_name": "tap-example"})
        tm.that(execution_context.execution_result, eq={"success": True})
        tm.that(result_context.execution_result, eq={"success": True})
        assert isinstance(execution_context.elt_context, MappingProxyType)
        assert isinstance(execution_context.execution_result, MappingProxyType)
        assert isinstance(result_context.execution_result, MappingProxyType)

    # ---- TapConfig ---------------------------------------------------------

    @staticmethod
    def test_tap_config_exposes_defaults_for_optional_fields() -> None:
        """Test tap config exposes defaults for optional fields."""
        settings = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
        )
        tm.that(settings.tap_type, eq="tap-postgres")
        tm.that(settings.connection_config, eq={"host": "localhost"})
        tm.that(settings.stream_config, empty=True)
        tm.that(settings.tap_version, eq="latest")

    @staticmethod
    def test_tap_config_retains_full_supplied_state() -> None:
        """Test tap config retains full supplied state."""
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

    @staticmethod
    def test_tap_config_computed_fields_derive_from_state() -> None:
        """Test tap config computed fields derive from state."""
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

    @staticmethod
    def test_tap_config_has_stream_config_false_when_absent() -> None:
        """Test tap config has stream config false when absent."""
        settings = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
        )
        tm.that(settings.has_stream_config, eq=False)
        tm.that(settings.config_size, eq=1)

    @staticmethod
    @pytest.mark.parametrize("blank_tap_type", ["", "   "])
    def test_tap_config_rejects_blank_tap_type(blank_tap_type: str) -> None:
        """Test tap config rejects blank tap type."""
        with pytest.raises(c.ValidationError, match="tap_type cannot be empty"):
            m.Meltano.TapConfig(
                tap_type=blank_tap_type,
                connection_config={"host": "localhost"},
            )

    @staticmethod
    def test_tap_config_rejects_empty_connection_config() -> None:
        """Test tap config rejects empty connection config."""
        with pytest.raises(
            c.ValidationError,
            match="Connection configuration cannot be empty",
        ):
            m.Meltano.TapConfig(tap_type="tap-postgres", connection_config={})

    @staticmethod
    def test_tap_config_rejects_non_mapping_connection_config() -> None:
        """Test tap config rejects non mapping connection config."""
        with pytest.raises(c.ValidationError, match="valid dictionary"):
            m.Meltano.TapConfig.model_validate({
                "tap_type": "tap-postgres",
                "connection_config": "invalid",
            })

    # ---- TargetConfig ------------------------------------------------------

    @staticmethod
    def test_target_config_exposes_defaults_for_optional_fields() -> None:
        """Test target config exposes defaults for optional fields."""
        settings = m.Meltano.TargetConfig(target_type="target-csv")
        tm.that(settings.target_type, eq="target-csv")
        tm.that(settings.connection_config, empty=True)
        tm.that(settings.batch_size, none=True)
        tm.that(settings.batch_wait_limit, none=True)
        tm.that(settings.target_version, eq="latest")

    @staticmethod
    def test_target_config_retains_full_supplied_state() -> None:
        """Test target config retains full supplied state."""
        settings = m.Meltano.TargetConfig(
            target_type="target-postgres",
            connection_config={
                "host": "localhost",
                "port": 5432,
                "database": "analytics",
                "user": "etl_user",
                "password": "p" + "8" * 8,
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

    @staticmethod
    def test_target_config_computed_fields_derive_from_state() -> None:
        """Test target config computed fields derive from state."""
        settings = m.Meltano.TargetConfig(
            target_type="target-postgres",
            connection_config={"host": "localhost", "port": 5432},
            target_version="3.0.0",
        )
        tm.that(settings.config_size, eq=2)
        tm.that(settings.has_connection_config, eq=True)
        tm.that(settings.target_identifier, eq="target-postgres:3.0.0")

    @staticmethod
    def test_target_config_has_connection_config_false_when_empty() -> None:
        """Test target config has connection config false when empty."""
        settings = m.Meltano.TargetConfig(target_type="target-csv")
        tm.that(settings.has_connection_config, eq=False)
        tm.that(settings.config_size, eq=0)

    @staticmethod
    def test_target_config_rejects_blank_target_type() -> None:
        """Test target config rejects blank target type."""
        with pytest.raises(c.ValidationError, match="target_type cannot be empty"):
            m.Meltano.TargetConfig(target_type="")

    @staticmethod
    def test_target_config_rejects_non_integer_batch_size() -> None:
        """Test target config rejects non integer batch size."""
        with pytest.raises(c.ValidationError, match="valid integer"):
            m.Meltano.TargetConfig.model_validate({
                "target_type": "target-csv",
                "batch_size": "invalid",
            })

    # ---- Composition -------------------------------------------------------

    @staticmethod
    def test_tap_and_target_configs_are_independent() -> None:
        """Test tap and target configs are independent."""
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

    @staticmethod
    def test_stream_name_maps_into_tap_stream_config() -> None:
        """Test stream name maps into tap stream config."""
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object", "properties": "id"},
            key_properties=("id",),
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tap_config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
            stream_config={"users": "public"},
        )
        tm.that(tap_config.stream_config, has=stream.stream_name)
        tm.that(stream.key_properties, has="id")


class TestsFlextMeltanoModelsStreamInfo:
    """StreamInfo model contract tests."""

    # ---- StreamInfo --------------------------------------------------------

    @staticmethod
    def test_stream_info_exposes_defaults_for_optional_fields() -> None:
        """Test stream info exposes defaults for optional fields."""
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

    @staticmethod
    def test_stream_info_retains_full_supplied_state() -> None:
        """Test stream info retains full supplied state."""
        stream = m.Meltano.StreamInfo(
            stream_name="orders",
            stream_schema={"type": "object", "properties": "id,order_date,amount"},
            key_properties=("id",),
            replication_method="FULL_TABLE",
            replication_key="order_date",
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tm.that(stream.stream_name, eq="orders")
        tm.that(stream.key_properties, has="id")
        tm.that(stream.replication_method, eq="FULL_TABLE")
        tm.that(stream.replication_key, eq="order_date")

    @staticmethod
    def test_stream_info_computed_fields_for_unprocessed_stream() -> None:
        """Test stream info computed fields for unprocessed stream."""
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object"},
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tm.that(stream.average_records_per_batch, eq=0.0)
        tm.that(stream.has_processed_data, eq=False)
        tm.that(stream.processing_status, eq=str(c.Meltano.StreamStatus.PENDING))

    @staticmethod
    def test_stream_info_average_records_per_batch_divides_totals() -> None:
        """Test stream info average records per batch divides totals."""
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object"},
            stream_created_at="2025-01-01T00:00:00Z",
            records_loaded=10,
            batches_processed=2,
        )
        tm.that(stream.average_records_per_batch, eq=5.0)
        tm.that(stream.has_processed_data, eq=True)

    @staticmethod
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
        status: str,
        records_loaded: int,
        batches_processed: int,
        expected: str,
    ) -> None:
        """Test stream info processing status reflects progress."""
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object"},
            stream_created_at="2025-01-01T00:00:00Z",
            status=status,
            records_loaded=records_loaded,
            batches_processed=batches_processed,
        )
        tm.that(stream.processing_status, eq=expected)

    @staticmethod
    def test_stream_info_rejects_empty_stream_name() -> None:
        """Test stream info rejects empty stream name."""
        with pytest.raises(c.ValidationError, match="at least 1 character"):
            m.Meltano.StreamInfo(
                stream_name="",
                stream_schema={"type": "object"},
                stream_created_at="2025-01-01T00:00:00Z",
            )

    @staticmethod
    def test_stream_info_rejects_records_without_batches() -> None:
        """Test stream info rejects records without batches."""
        with pytest.raises(
            c.ValidationError,
            match="Records loaded but no batches processed",
        ):
            m.Meltano.StreamInfo(
                stream_name="users",
                stream_schema={"type": "object"},
                stream_created_at="2025-01-01T00:00:00Z",
                records_loaded=5,
                batches_processed=0,
            )

    @staticmethod
    def test_stream_info_rejects_unknown_status() -> None:
        """Test stream info rejects unknown status."""
        with pytest.raises(c.ValidationError, match="Status must be one of"):
            m.Meltano.StreamInfo(
                stream_name="users",
                stream_schema={"type": "object"},
                stream_created_at="2025-01-01T00:00:00Z",
                status="not-a-real-status",
            )

    @staticmethod
    def test_stream_info_rejects_non_mapping_schema() -> None:
        """Test stream info rejects non mapping schema."""
        with pytest.raises(c.ValidationError, match="valid dictionary"):
            m.Meltano.StreamInfo.model_validate({
                "stream_name": "users",
                "stream_schema": "invalid",
                "stream_created_at": "2025-01-01T00:00:00Z",
            })
