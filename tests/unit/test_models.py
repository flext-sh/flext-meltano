"""Behavioral tests for the Meltano models public contract.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableMapping
from operator import methodcaller
from pathlib import Path
from types import MappingProxyType

import pytest
from jsonschema import Draft202012Validator, ValidationError, validate

from tests import c, m, t, tm, u


class TestsPipelineContext:
    """Public contract for immutable pipeline execution and result contexts."""

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
        tm.that(isinstance(execution_context.elt_context, MappingProxyType), truth=True)
        tm.that(
            isinstance(execution_context.execution_result, MappingProxyType),
            truth=True,
        )
        tm.that(
            isinstance(result_context.execution_result, MappingProxyType),
            truth=True,
        )


class TestsTapConfig:
    """Public contract for tap configuration defaults and validation."""

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
        tm.that(
            settings.tap_version,
            eq=m.Meltano.TapConfig.model_fields["tap_version"].default,
        )

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


class TestsTargetConfig:
    """Public contract for target configuration defaults and validation."""

    @staticmethod
    def test_target_config_exposes_defaults_for_optional_fields() -> None:
        """Test target config exposes defaults for optional fields."""
        settings = m.Meltano.TargetConfig(target_type="target-csv")
        tm.that(settings.target_type, eq="target-csv")
        tm.that(settings.connection_config, empty=True)
        tm.that(
            settings.batch_size,
            eq=m.Meltano.TargetConfig.model_fields["batch_size"].default,
        )
        tm.that(
            settings.batch_wait_limit,
            eq=m.Meltano.TargetConfig.model_fields["batch_wait_limit"].default,
        )
        tm.that(
            settings.target_version,
            eq=m.Meltano.TargetConfig.model_fields["target_version"].default,
        )

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
        tm.that(settings.batch_wait_limit, eq=30.0)

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


class TestsModelComposition:
    """Public contract for model composition and serialization."""

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

    @staticmethod
    def test_connection_serialization_redacts_without_mutating_inputs() -> None:
        """Public dumps redact secrets while preserving supplied non-sensitive data."""
        marker = "serialization-input-marker"
        database: t.JsonDict = {"password": marker, "name": "analytics"}
        option: t.JsonDict = {"token": marker, "label": "nested-option"}
        connection: t.JsonDict = {
            "password": marker,
            "api_token": marker,
            "display_name": "serialization-consumer",
            "database": database,
            "options": [option],
        }
        configs = (
            m.Meltano.TapConfig(
                tap_type="tap-serialization-consumer",
                connection_config=connection,
            ),
            m.Meltano.TargetConfig(
                target_type="target-serialization-consumer",
                connection_config=connection,
            ),
        )
        for config in configs:
            payloads = (
                config.model_dump(mode="json"),
                u.Cli.JSON_MAPPING_ADAPTER.validate_json(config.model_dump_json()),
            )
            for payload in payloads:
                exported = u.Cli.JSON_MAPPING_ADAPTER.validate_python(
                    payload["connection_config"],
                )
                tm.that(exported["display_name"], eq=connection["display_name"])
                tm.that(list(exported.values()), lacks=marker)
                exported_database = u.Cli.JSON_MAPPING_ADAPTER.validate_python(
                    exported["database"],
                )
                tm.that(exported_database["password"], ne=marker)
                tm.that(exported_database["name"], eq=database["name"])
                exported_options = exported["options"]
                tm.that(isinstance(exported_options, list), truth=True)
                exported_option = u.Cli.JSON_MAPPING_ADAPTER.validate_python(
                    exported_options[0],
                )
                tm.that(exported_option["token"], ne=marker)
                tm.that(exported_option["label"], eq=option["label"])
            tm.that(config.connection_config, eq=connection)
        tm.that(connection["password"], eq=marker)
        tm.that(connection["api_token"], eq=marker)
        tm.that(database["password"], eq=marker)
        tm.that(option["token"], eq=marker)

    @staticmethod
    @pytest.mark.parametrize("supplied", [False, True])
    def test_readonly_stream_config_serialization_roundtrip(*, supplied: bool) -> None:
        """Exporting default or supplied stream mappings keeps their readonly state."""
        stream_input: t.JsonDict = {"users": "public"}
        payload: t.JsonDict = {"connection_config": {"host": "source.example"}}
        if supplied:
            payload["stream_config"] = stream_input
        configs = (
            m.Meltano.TapConfig.model_validate({
                **payload,
                "tap_type": "tap-serialization-consumer",
            }),
        )
        for config in configs:
            tm.that(
                config.model_dump(mode="json")["stream_config"],
                eq=config.stream_config,
            )
            restored = type(config).model_validate_json(
                config.model_dump_json(round_trip=True),
            )
            for stream_config in (config.stream_config, restored.stream_config):
                tm.that(not isinstance(stream_config, MutableMapping), truth=True)
                with pytest.raises(AttributeError, match="update"):
                    methodcaller("update", {"users": "changed"})(stream_config)
                tm.that(stream_config, eq=config.stream_config)
        tm.that(stream_input, eq={"users": "public"})

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

    @staticmethod
    def test_stream_definition_exports_a_schema_for_real_record_validation() -> None:
        """The exported schema accepts integer IDs and rejects protocol violations."""
        schema_input: t.JsonDict = {
            "properties": {"id": {"type": "integer"}},
            "required": ["id"],
        }
        stream = m.Meltano.StreamDefinition(
            stream_name="serialization-consumer",
            source_type="serialization-consumer",
            stream_schema=schema_input,
        )
        payloads = (
            stream.model_dump(mode="json"),
            u.Cli.JSON_MAPPING_ADAPTER.validate_json(stream.model_dump_json()),
        )
        for payload in payloads:
            schema = u.Cli.JSON_MAPPING_ADAPTER.validate_python(
                payload["stream_schema"],
            )
            Draft202012Validator.check_schema(schema)
            validate({"id": 1}, schema, cls=Draft202012Validator)
            for invalid in ({"id": "not-an-integer"}, {}, [{"id": 1}]):
                with pytest.raises(ValidationError):
                    validate(invalid, schema, cls=Draft202012Validator)
        tm.that(stream.stream_schema, eq=schema_input)
        tm.that(schema_input, lacks="type")


class TestsStreamInfo:
    """Public contract for stream state and validation."""

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
