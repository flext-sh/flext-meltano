"""Comprehensive unit tests for FlextMeltanoModels.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile
from datetime import UTC, datetime
from pathlib import Path

import pytest
from flext_core import FlextConstants

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels


class TestFlextMeltanoModelsTapConfig:
    """Test FlextMeltanoModels.TapConfig validation and functionality."""

    def test_tap_config_valid_creation(self) -> None:
        """Test creating a valid TapConfig."""
        config = FlextMeltanoModels.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost", "port": 5432},
            stream_config={"users": {"schema": "public"}},
            version="1.0.0",
        )

        assert config.tap_type == "tap-postgres"
        assert config.connection_config["host"] == "localhost"
        assert config.connection_config["port"] == 5432
        assert config.stream_config["users"]["schema"] == "public"
        assert config.version == "1.0.0"

    def test_tap_config_default_values(self) -> None:
        """Test TapConfig with default values."""
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            config = FlextMeltanoModels.TapConfig(
                tap_type="tap-csv",
                connection_config={"file_path": temp_file.name},
            )

        assert config.tap_type == "tap-csv"
        assert config.stream_config == {}
        assert config.version == "latest"

    def test_tap_config_validation_empty_tap_type(self) -> None:
        """Test TapConfig validation with empty tap_type."""
        with pytest.raises(ValueError, match="tap_type cannot be empty"):
            FlextMeltanoModels.TapConfig(
                tap_type="", connection_config={"host": "localhost"}
            )

    def test_tap_config_validation_whitespace_tap_type(self) -> None:
        """Test TapConfig validation with whitespace-only tap_type."""
        with pytest.raises(ValueError, match="tap_type cannot be empty"):
            FlextMeltanoModels.TapConfig(
                tap_type="   ", connection_config={"host": "localhost"}
            )

    def test_tap_config_validation_empty_connection_config(self) -> None:
        """Test TapConfig validation with empty connection_config."""
        with pytest.raises(
            ValueError, match="Connection configuration cannot be empty"
        ):
            FlextMeltanoModels.TapConfig(tap_type="tap-postgres", connection_config={})

    def test_tap_config_validation_invalid_connection_config_type(self) -> None:
        """Test TapConfig validation with invalid connection_config type."""
        with pytest.raises(ValueError, match="Input should be a valid dictionary"):
            FlextMeltanoModels.TapConfig(
                tap_type="tap-postgres",
                connection_config="invalid",
            )


class TestFlextMeltanoModelsStreamDefinition:
    """Test FlextMeltanoModels.StreamDefinition functionality."""

    def test_stream_definition_valid_creation(self) -> None:
        """Test creating a valid StreamDefinition."""
        stream = FlextMeltanoModels.StreamDefinition(
            stream_name="users",
            stream_schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            tap_type="tap-postgres",
            status="discovered",
            records_extracted=100,
        )

        assert stream.stream_name == "users"
        assert stream.stream_schema["type"] == "object"
        assert stream.tap_type == "tap-postgres"
        assert stream.status == "discovered"
        assert stream.records_extracted == 100

    def test_stream_definition_default_values(self) -> None:
        """Test StreamDefinition with default values."""
        stream = FlextMeltanoModels.StreamDefinition(
            stream_name="orders", stream_schema={"type": "object"}, tap_type="tap-mysql"
        )

        assert stream.stream_name == "orders"
        assert stream.status == "discovered"
        assert stream.records_extracted == 0


class TestFlextMeltanoModelsTapInstance:
    """Test FlextMeltanoModels.TapInstance functionality."""

    def test_tap_instance_valid_creation(self) -> None:
        """Test creating a valid TapInstance."""
        tap_config = FlextMeltanoModels.TapConfig(
            tap_type="tap-postgres", connection_config={"host": "localhost"}
        )

        tap_instance = FlextMeltanoModels.TapInstance(
            tap_type="tap-postgres",
            config=tap_config,
            tap_id="tap-001",
            status="ready",
            discovered=True,
        )

        assert tap_instance.tap_type == "tap-postgres"
        assert tap_instance.config.tap_type == "tap-postgres"
        assert tap_instance.tap_id == "tap-001"
        assert tap_instance.status == "ready"
        assert tap_instance.discovered is True
        assert tap_instance.streams == {}
        assert tap_instance.metadata == {}

    def test_tap_instance_default_values(self) -> None:
        """Test TapInstance with default values."""
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            tap_config = FlextMeltanoModels.TapConfig(
                tap_type="tap-csv",
                connection_config={"file_path": temp_file.name},
            )

        tap_instance = FlextMeltanoModels.TapInstance(
            tap_type="tap-csv", config=tap_config, tap_id="tap-002"
        )

        assert tap_instance.adapter is None
        assert tap_instance.status == "initialized"
        assert tap_instance.discovered is False


class TestFlextMeltanoModelsTargetConfig:
    """Test FlextMeltanoModels.TargetConfig validation and functionality."""

    def test_target_config_valid_creation(self) -> None:
        """Test creating a valid TargetConfig."""
        config = FlextMeltanoModels.TargetConfig(
            target_type="target-postgres",
            connection_config={"host": "localhost", "port": 5432},
            batch_size=1000,
            max_batches=50,
        )

        assert config.target_type == "target-postgres"
        assert config.connection_config["host"] == "localhost"
        assert config.batch_size == 1000
        assert config.max_batches == 50

    def test_target_config_default_values(self) -> None:
        """Test TargetConfig with default values."""
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            config = FlextMeltanoModels.TargetConfig(
                target_type="target-csv",
                connection_config={"file_path": temp_file.name},
            )

        assert (
            config.batch_size == FlextConstants.Performance.BatchProcessing.DEFAULT_SIZE
        )
        assert config.max_batches == 100

    def test_target_config_validation_empty_target_type(self) -> None:
        """Test TargetConfig validation with empty target_type."""
        with pytest.raises(ValueError, match="Target type must be non-empty string"):
            FlextMeltanoModels.TargetConfig(
                target_type="", connection_config={"host": "localhost"}
            )

    def test_target_config_validation_invalid_target_type_type(self) -> None:
        """Test TargetConfig validation with invalid target_type type."""
        with pytest.raises(ValueError, match="Input should be a valid string"):
            FlextMeltanoModels.TargetConfig(
                target_type=123,
                connection_config={"host": "localhost"},
            )

    def test_target_config_validation_empty_connection_config(self) -> None:
        """Test TargetConfig validation with empty connection_config."""
        with pytest.raises(
            ValueError, match="Connection configuration cannot be empty"
        ):
            FlextMeltanoModels.TargetConfig(
                target_type="target-postgres", connection_config={}
            )

    def test_target_config_validation_invalid_batch_size(self) -> None:
        """Test TargetConfig validation with invalid batch_size."""
        with pytest.raises(ValueError, match="Batch size must be positive integer"):
            FlextMeltanoModels.TargetConfig(
                target_type="target-postgres",
                connection_config={"host": "localhost"},
                batch_size=0,
            )

    def test_target_config_validation_invalid_max_batches(self) -> None:
        """Test TargetConfig validation with invalid max_batches."""
        with pytest.raises(ValueError, match="Max batches must be positive integer"):
            FlextMeltanoModels.TargetConfig(
                target_type="target-postgres",
                connection_config={"host": "localhost"},
                max_batches=-1,
            )


class TestFlextMeltanoModelsStreamInfo:
    """Test FlextMeltanoModels.StreamInfo functionality."""

    def test_stream_info_valid_creation(self) -> None:
        """Test creating a valid StreamInfo."""
        stream_info = FlextMeltanoModels.StreamInfo(
            stream_name="users",
            schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            status="loaded",
            records_loaded=500,
            batches_processed=5,
            created_at="2025-01-01T00:00:00Z",
        )

        assert stream_info.stream_name == "users"
        assert stream_info.stream_schema["type"] == "object"
        assert stream_info.status == "loaded"
        assert stream_info.records_loaded == 500
        assert stream_info.batches_processed == 5
        assert stream_info.created_at == "2025-01-01T00:00:00Z"

    def test_stream_info_default_values(self) -> None:
        """Test StreamInfo with default values."""
        stream_info = FlextMeltanoModels.StreamInfo(
            stream_name="orders",
            schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            created_at="2025-01-01T00:00:00Z",
        )

        assert stream_info.status == "initialized"
        assert stream_info.records_loaded == 0
        assert stream_info.batches_processed == 0

    def test_stream_info_validation_empty_stream_name(self) -> None:
        """Test StreamInfo validation with empty stream_name."""
        with pytest.raises(ValueError, match="Stream name must be non-empty string"):
            FlextMeltanoModels.StreamInfo(
                stream_name="",
                schema={"type": "object", "properties": {"id": {"type": "integer"}}},
                created_at="2025-01-01T00:00:00Z",
            )

    def test_stream_info_validation_missing_schema_properties(self) -> None:
        """Test StreamInfo validation with schema missing properties."""
        with pytest.raises(ValueError, match="Schema must contain properties"):
            FlextMeltanoModels.StreamInfo(
                stream_name="users",
                schema={"type": "object"},
                created_at="2025-01-01T00:00:00Z",
            )


class TestFlextMeltanoModelsMeltanoProjectModel:
    """Test FlextMeltanoModels.MeltanoProjectModel functionality."""

    def test_meltano_project_valid_creation(self) -> None:
        """Test creating a valid MeltanoProjectModel."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_project_path = Path(temp_dir)
            project = FlextMeltanoModels.MeltanoProjectModel(
                version=1,
                project_id="my-meltano-project",
                default_environment="development",
                project_root=temp_project_path,
                environments=["development", "staging", "production"],
            )

            assert project.version == 1
            assert project.project_id == "my-meltano-project"
            assert project.default_environment == "development"
            assert project.project_root == temp_project_path
            assert project.environments == ["development", "staging", "production"]

    def test_meltano_project_default_values(self) -> None:
        """Test MeltanoProjectModel with default values."""
        project = FlextMeltanoModels.MeltanoProjectModel(
            version=1, project_id="test-project"
        )

        assert project.default_environment == "dev"
        assert project.project_root == Path.cwd()
        assert project.environments == ["dev", "staging", "prod"]

    def test_meltano_project_validation_empty_project_id(self) -> None:
        """Test MeltanoProjectModel validation with empty project_id."""
        with pytest.raises(ValueError, match="String should have at least 1 character"):
            FlextMeltanoModels.MeltanoProjectModel(version=1, project_id="")

    def test_meltano_project_validation_project_id_with_spaces(self) -> None:
        """Test MeltanoProjectModel validation with project_id containing spaces."""
        with pytest.raises(ValueError, match="Project ID cannot contain spaces"):
            FlextMeltanoModels.MeltanoProjectModel(version=1, project_id="my project")

    def test_meltano_project_validation_project_id_invalid_characters(self) -> None:
        """Test MeltanoProjectModel validation with project_id containing invalid characters."""
        with pytest.raises(
            ValueError,
            match="Project ID can only contain letters, numbers, hyphens, and underscores",
        ):
            FlextMeltanoModels.MeltanoProjectModel(version=1, project_id="my@project")


class TestFlextMeltanoModelsPluginModel:
    """Test FlextMeltanoModels.PluginModel functionality."""

    def test_plugin_model_valid_creation(self) -> None:
        """Test creating a valid PluginModel."""
        plugin = FlextMeltanoModels.PluginModel(
            name="tap-postgres",
            namespace="tap_postgres",
            pip_url="pipelinewise-tap-postgres",
            executable="tap-postgres",
            variant="meltanolabs",
            settings={"debug": True},
        )

        assert plugin.name == "tap-postgres"
        assert plugin.namespace == "tap_postgres"
        assert plugin.pip_url == "pipelinewise-tap-postgres"
        assert plugin.executable == "tap-postgres"
        assert plugin.variant == "meltanolabs"
        assert plugin.settings["debug"] is True

    def test_plugin_model_default_values(self) -> None:
        """Test PluginModel with default values."""
        plugin = FlextMeltanoModels.PluginModel(name="tap-csv", namespace="tap_csv")

        assert plugin.pip_url is None
        assert plugin.executable is None
        assert plugin.variant == FlextMeltanoConstants.PLUGIN_DEFAULT_VARIANT
        assert plugin.settings == {}

    def test_plugin_model_validation_empty_name(self) -> None:
        """Test PluginModel validation with empty name."""
        with pytest.raises(ValueError, match="String should have at least 1 character"):
            FlextMeltanoModels.PluginModel(name="", namespace="tap_csv")

    def test_plugin_model_validation_name_with_spaces(self) -> None:
        """Test PluginModel validation with name containing spaces."""
        with pytest.raises(ValueError, match="Plugin name cannot contain spaces"):
            FlextMeltanoModels.PluginModel(name="tap csv", namespace="tap_csv")


class TestFlextMeltanoModelsDbtProjectModel:
    """Test FlextMeltanoModels.DbtProjectModel functionality."""

    def test_dbt_project_valid_creation(self) -> None:
        """Test creating a valid DbtProjectModel."""
        dbt_project = FlextMeltanoModels.DbtProjectModel(
            name="analytics",
            version="1.0.0",
            profile="analytics_profile",
            model_paths=["models", "staging"],
            analysis_paths=["analysis"],
            test_paths=["tests"],
            seed_paths=["seeds"],
            macro_paths=["macros"],
        )

        assert dbt_project.name == "analytics"
        assert dbt_project.version == "1.0.0"
        assert dbt_project.profile == "analytics_profile"
        assert dbt_project.model_paths == ["models", "staging"]
        assert dbt_project.analysis_paths == ["analysis"]
        assert dbt_project.test_paths == ["tests"]
        assert dbt_project.seed_paths == ["seeds"]
        assert dbt_project.macro_paths == ["macros"]

    def test_dbt_project_default_values(self) -> None:
        """Test DbtProjectModel with default values."""
        dbt_project = FlextMeltanoModels.DbtProjectModel(
            name="analytics", version="1.0.0", profile="analytics_profile"
        )

        assert dbt_project.model_paths == ["models"]
        assert dbt_project.analysis_paths == ["analysis"]
        assert dbt_project.test_paths == ["tests"]
        assert dbt_project.seed_paths == ["seeds"]
        assert dbt_project.macro_paths == ["macros"]

    def test_dbt_project_validation_empty_name(self) -> None:
        """Test DbtProjectModel validation with empty name."""
        with pytest.raises(ValueError, match="String should have at least 1 character"):
            FlextMeltanoModels.DbtProjectModel(
                name="", version="1.0.0", profile="analytics_profile"
            )

    def test_dbt_project_validation_name_with_spaces(self) -> None:
        """Test DbtProjectModel validation with name containing spaces."""
        with pytest.raises(ValueError, match="DBT project name cannot contain spaces"):
            FlextMeltanoModels.DbtProjectModel(
                name="my analytics", version="1.0.0", profile="analytics_profile"
            )


class TestFlextMeltanoModelsDbtExecutionModel:
    """Test FlextMeltanoModels.DbtExecutionModel functionality."""

    def test_dbt_execution_valid_creation(self) -> None:
        """Test creating a valid DbtExecutionModel."""
        execution = FlextMeltanoModels.DbtExecutionModel(
            command="run",
            models=["model1", "model2"],
            exclude=["model3"],
            full_refresh=True,
            fail_fast=False,
            threads=4,
        )

        assert execution.command == "run"
        assert execution.models == ["model1", "model2"]
        assert execution.exclude == ["model3"]
        assert execution.full_refresh is True
        assert execution.fail_fast is False
        assert execution.threads == 4

    def test_dbt_execution_default_values(self) -> None:
        """Test DbtExecutionModel with default values."""
        execution = FlextMeltanoModels.DbtExecutionModel(command="test")

        assert execution.models == []
        assert execution.exclude == []
        assert execution.full_refresh is False
        assert execution.fail_fast is True
        assert execution.threads == 1

    def test_dbt_execution_validation_invalid_command(self) -> None:
        """Test DbtExecutionModel validation with invalid command."""
        with pytest.raises(ValueError, match="DBT command must be one of"):
            FlextMeltanoModels.DbtExecutionModel(command="invalid_command")


class TestFlextMeltanoModelsExecutionResult:
    """Test FlextMeltanoModels.ExecutionResult functionality."""

    def test_execution_result_valid_creation(self) -> None:
        """Test creating a valid ExecutionResult."""
        start_time = datetime.now(tz=UTC)
        end_time = datetime.now(tz=UTC)

        result = FlextMeltanoModels.ExecutionResult(
            operation="extract",
            status="success",
            start_time=start_time,
            end_time=end_time,
            duration_seconds=120.5,
            records_processed=1000,
            error_message=None,
            metadata={"source": "postgres"},
        )

        assert result.operation == "extract"
        assert result.status == "success"
        assert result.start_time == start_time
        assert result.end_time == end_time
        assert result.duration_seconds == 120.5
        assert result.records_processed == 1000
        assert result.error_message is None
        assert result.metadata["source"] == "postgres"

    def test_execution_result_default_values(self) -> None:
        """Test ExecutionResult with default values."""
        result = FlextMeltanoModels.ExecutionResult(operation="load", status="running")

        assert result.end_time is None
        assert result.duration_seconds is None
        assert result.records_processed == 0
        assert result.error_message is None
        assert result.metadata == {}

    def test_execution_result_validation_invalid_status(self) -> None:
        """Test ExecutionResult validation with invalid status."""
        with pytest.raises(ValueError, match="Status must be one of"):
            FlextMeltanoModels.ExecutionResult(
                operation="extract", status="invalid_status"
            )


class TestFlextMeltanoModelsPipelineResult:
    """Test FlextMeltanoModels.PipelineResult functionality."""

    def test_pipeline_result_valid_creation(self) -> None:
        """Test creating a valid PipelineResult."""
        tap_result = FlextMeltanoModels.ExecutionResult(
            operation="extract", status="success"
        )

        target_result = FlextMeltanoModels.ExecutionResult(
            operation="load", status="success"
        )

        pipeline = FlextMeltanoModels.PipelineResult(
            pipeline_id="pipeline-001",
            tap_result=tap_result,
            target_result=target_result,
            overall_status="success",
            total_records=1000,
            pipeline_metadata={"environment": "production"},
        )

        assert pipeline.pipeline_id == "pipeline-001"
        assert pipeline.tap_result == tap_result
        assert pipeline.target_result == target_result
        assert pipeline.overall_status == "success"
        assert pipeline.total_records == 1000
        assert pipeline.pipeline_metadata["environment"] == "production"

    def test_pipeline_result_default_values(self) -> None:
        """Test PipelineResult with default values."""
        pipeline = FlextMeltanoModels.PipelineResult(pipeline_id="pipeline-002")

        assert pipeline.tap_result is None
        assert pipeline.target_result is None
        assert pipeline.dbt_result is None
        assert pipeline.overall_status == "pending"
        assert pipeline.total_records == 0
        assert pipeline.pipeline_metadata == {}

    def test_pipeline_result_validation_invalid_overall_status(self) -> None:
        """Test PipelineResult validation with invalid overall_status."""
        with pytest.raises(ValueError, match="Overall status must be one of"):
            FlextMeltanoModels.PipelineResult(
                pipeline_id="pipeline-003", overall_status="invalid_status"
            )


class TestFlextMeltanoModelsIntegration:
    """Integration tests for FlextMeltanoModels."""

    def test_complete_pipeline_workflow(self) -> None:
        """Test a complete pipeline workflow using all models."""
        # Create tap configuration
        tap_config = FlextMeltanoModels.TapConfig(
            tap_type="tap-postgres",
            connection_config={
                "host": "localhost",
                "port": 5432,
                "database": "source_db",
            },
            stream_config={"users": {"schema": "public"}},
            version="1.0.0",
        )

        # Create tap instance
        tap_instance = FlextMeltanoModels.TapInstance(
            tap_type="tap-postgres", config=tap_config, tap_id="tap-001", status="ready"
        )

        # Create stream definition
        stream_def = FlextMeltanoModels.StreamDefinition(
            stream_name="users",
            stream_schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            tap_type="tap-postgres",
            records_extracted=100,
        )

        # Add stream to tap instance
        tap_instance.streams["users"] = stream_def
        tap_instance.discovered = True

        # Create target configuration
        target_config = FlextMeltanoModels.TargetConfig(
            target_type="target-postgres",
            connection_config={
                "host": "localhost",
                "port": 5432,
                "database": "target_db",
            },
            batch_size=1000,
        )

        # Create execution results
        tap_result = FlextMeltanoModels.ExecutionResult(
            operation="extract", status="success", records_processed=100
        )

        target_result = FlextMeltanoModels.ExecutionResult(
            operation="load", status="success", records_processed=100
        )

        # Create pipeline result
        pipeline_result = FlextMeltanoModels.PipelineResult(
            pipeline_id="pipeline-001",
            tap_result=tap_result,
            target_result=target_result,
            overall_status="success",
            total_records=100,
        )

        # Verify the complete workflow
        assert tap_instance.tap_type == "tap-postgres"
        assert tap_instance.discovered is True
        assert len(tap_instance.streams) == 1
        assert tap_instance.streams["users"].records_extracted == 100

        assert target_config.batch_size == 1000
        assert pipeline_result.overall_status == "success"
        assert pipeline_result.total_records == 100

    def test_model_serialization(self) -> None:
        """Test model serialization and deserialization."""
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp_file:
            temp_file_path = temp_file.name
        tap_config = FlextMeltanoModels.TapConfig(
            tap_type="tap-csv", connection_config={"file_path": temp_file_path}
        )

        # Test model_dump
        config_dict = tap_config.model_dump()
        assert config_dict["tap_type"] == "tap-csv"
        assert config_dict["connection_config"]["file_path"] == temp_file_path

        # Test model_validate
        new_config = FlextMeltanoModels.TapConfig.model_validate(config_dict)
        assert new_config.tap_type == tap_config.tap_type
        assert new_config.connection_config == tap_config.connection_config
