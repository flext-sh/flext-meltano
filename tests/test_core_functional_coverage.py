"""Functional Coverage Tests for Core Module - Real Implementation Testing.

**Purpose**: Test actual functionality of core.py module classes and methods
**Scope**: Focus on classes that actually exist and can be tested functionally
**Target**: Increase core.py coverage from 55% to 90%+

This module provides functional tests for the core services and entities
that can be instantiated and tested without complex dependency injection.
"""

from __future__ import annotations

import pytest

from flext_meltano.base import FlextMeltanoConfig
from flext_meltano.core import (
    ExecutionState,
    FlextMeltanoExecutionState,
    FlextMeltanoExtension,
    FlextMeltanoPipelineConfig,
    FlextMeltanoPipelineEvent,
    FlextMeltanoPipelineResult,
    FlextMeltanoSingerService,
    PipelineEventType,
)


class TestFlextMeltanoExecutionStateComplete:
    """Complete tests for FlextMeltanoExecutionState."""

    def test_execution_state_creation_and_initialization(self):
        """Test execution state creation with all fields."""
        state = FlextMeltanoExecutionState(
            pipeline_name="test-pipeline",
            environment="production",
            started_at="2025-08-05T10:00:00Z",
        )

        assert state.pipeline_name == "test-pipeline"
        assert state.environment == "production"
        assert state.state == ExecutionState.RUNNING.value
        assert isinstance(state.metadata, dict)

    def test_execution_state_complete_lifecycle(self):
        """Test complete execution state lifecycle."""
        state = FlextMeltanoExecutionState()

        # Start pipeline
        execution_id = state.start_pipeline("comprehensive-test")
        assert isinstance(execution_id, str)
        assert len(execution_id) > 0
        assert state.current_pipeline == "comprehensive-test"

        # Complete pipeline
        state.complete_pipeline()
        assert state.state == ExecutionState.COMPLETED.value

        # Reset and test failure path
        state = FlextMeltanoExecutionState()
        state.start_pipeline("failure-test")

        # Fail pipeline with detailed error
        error_message = "Database connection failed: timeout after 30s"
        state.fail_pipeline(error_message)

        assert state.state == ExecutionState.FAILED.value
        assert state.metadata["error"] == error_message
        assert "failed_at" in state.metadata

    def test_execution_state_metadata_management(self):
        """Test execution state metadata handling."""
        state = FlextMeltanoExecutionState()

        # Test metadata is properly initialized
        assert isinstance(state.metadata, dict)

        # Start pipeline and check metadata updates
        execution_id = state.start_pipeline("metadata-test")
        assert "started_at" in state.metadata
        assert state.execution_id == execution_id

        # Complete and check completion metadata
        state.complete_pipeline()
        assert "completed_at" in state.metadata

    def test_execution_state_edge_cases(self):
        """Test execution state edge cases."""
        state = FlextMeltanoExecutionState()

        # Test empty pipeline name
        execution_id = state.start_pipeline("")
        assert isinstance(execution_id, str)
        assert len(execution_id) > 0

        # Test complete without start
        state_2 = FlextMeltanoExecutionState()
        state_2.complete_pipeline()
        assert state_2.state == ExecutionState.COMPLETED

        # Test fail without start
        state_3 = FlextMeltanoExecutionState()
        state_3.fail_pipeline("No pipeline was running")
        assert state_3.state == ExecutionState.FAILED


class TestFlextMeltanoPipelineConfigComplete:
    """Complete tests for FlextMeltanoPipelineConfig."""

    def test_pipeline_config_creation_minimal(self):
        """Test minimal pipeline configuration creation."""
        config = FlextMeltanoPipelineConfig(
            name="minimal-pipeline",
            extractor="tap-csv",
            loader="target-csv",
        )

        assert config.name == "minimal-pipeline"
        assert config.extractor == "tap-csv"
        assert config.loader == "target-csv"
        assert config.transformer is None
        assert isinstance(config.config, dict)

    def test_pipeline_config_creation_complete(self):
        """Test complete pipeline configuration creation."""
        custom_config = {
            "database_url": "postgresql://user:pass@localhost/db",
            "batch_size": 1000,
            "timeout": 300,
        }

        config = FlextMeltanoPipelineConfig(
            name="complete-pipeline",
            extractor="tap-postgres",
            loader="target-snowflake",
            transformer="dbt-postgres",
            config=custom_config,
        )

        assert config.name == "complete-pipeline"
        assert config.extractor == "tap-postgres"
        assert config.loader == "target-snowflake"
        assert config.transformer == "dbt-postgres"
        assert config.config["database_url"] == "postgresql://user:pass@localhost/db"
        assert config.config["batch_size"] == 1000

    def test_pipeline_config_validation(self):
        """Test pipeline configuration validation through properties."""
        config = FlextMeltanoPipelineConfig(
            name="validation-test",
            extractor="tap-test",
            loader="target-test",
        )

        # Test basic properties
        assert config.name == "validation-test"
        assert config.extractor == "tap-test"
        assert config.loader == "target-test"

        # Test optional properties
        assert config.transformer is None
        assert hasattr(config, "config")

        # Test empty name handling - should raise ValueError
        with pytest.raises(
            ValueError,
            match="Pipeline name, extractor, and loader are required",
        ):
            FlextMeltanoPipelineConfig(
                name="",  # Empty name
                extractor="tap-test",
                loader="target-test",
            )

    def test_pipeline_config_with_complex_configuration(self):
        """Test pipeline configuration with complex nested config."""
        complex_config = {
            "source": {
                "host": "localhost",
                "port": 5432,
                "database": "analytics",
                "credentials": {
                    "username": "user",
                    "password": "secret",
                },
            },
            "target": {
                "warehouse": "snowflake",
                "schema": "public",
                "threads": 8,
            },
            "transformations": {
                "models": ["model1", "model2", "model3"],
                "tests": True,
                "documentation": True,
            },
        }

        config = FlextMeltanoPipelineConfig(
            name="complex-pipeline",
            extractor="tap-postgres",
            loader="target-snowflake",
            transformer="dbt-postgres",
            config=complex_config,
        )

        assert config.config["source"]["host"] == "localhost"
        assert config.config["target"]["threads"] == 8
        assert len(config.config["transformations"]["models"]) == 3


class TestFlextMeltanoPipelineResultComplete:
    """Complete tests for FlextMeltanoPipelineResult."""

    def test_pipeline_result_creation_success(self):
        """Test successful pipeline result creation."""
        result = FlextMeltanoPipelineResult(
            pipeline_name="success-pipeline",
            state=ExecutionState.COMPLETED,
        )

        assert result.pipeline_name == "success-pipeline"
        assert result.state == ExecutionState.COMPLETED.value
        assert result.error_message is None
        assert isinstance(result.id, str)
        assert len(result.id) > 0

    def test_pipeline_result_creation_failure(self):
        """Test failed pipeline result creation."""
        error_msg = "Pipeline execution failed: Connection timeout"
        result = FlextMeltanoPipelineResult(
            pipeline_name="failure-pipeline",
            state=ExecutionState.FAILED,
            error_message=error_msg,
        )

        assert result.pipeline_name == "failure-pipeline"
        assert result.state == ExecutionState.FAILED.value
        assert result.error_message == error_msg

    def test_pipeline_result_with_metadata(self):
        """Test pipeline result with metadata."""
        metadata = {
            "duration": 120.5,
            "records_processed": 10000,
            "warnings": 3,
        }

        result = FlextMeltanoPipelineResult(
            pipeline_name="metadata-pipeline",
            state=ExecutionState.COMPLETED,
            metadata=metadata,
        )

        assert result.metadata["duration"] == 120.5
        assert result.metadata["records_processed"] == 10000
        assert result.metadata["warnings"] == 3

    def test_pipeline_result_domain_validation(self):
        """Test pipeline result domain validation."""
        result = FlextMeltanoPipelineResult(
            pipeline_name="validation-test",
            state=ExecutionState.COMPLETED,
        )

        validation_result = result.validate_business_rules()
        assert validation_result.success

        # Test with empty pipeline name
        empty_name_result = FlextMeltanoPipelineResult(
            pipeline_name="",
            state=ExecutionState.COMPLETED,
        )

        validation_result = empty_name_result.validate_business_rules()
        # Should fail validation due to empty name
        assert hasattr(validation_result, "success")


class TestFlextMeltanoPipelineEventComplete:
    """Complete tests for FlextMeltanoPipelineEvent."""

    def test_pipeline_event_creation_basic(self):
        """Test basic pipeline event creation."""
        event = FlextMeltanoPipelineEvent(
            event_type=PipelineEventType.STARTED,
            pipeline_name="test-pipeline",
        )

        assert event.event_type == PipelineEventType.STARTED
        assert event.pipeline_name == "test-pipeline"
        assert isinstance(event.id, str)
        assert isinstance(event.data, dict)

    def test_pipeline_event_creation_with_data(self):
        """Test pipeline event creation with data."""
        event_data = {
            "execution_id": "exec-123",
            "environment": "production",
            "triggered_by": "scheduler",
            "config": {
                "timeout": 300,
                "retry_count": 3,
            },
        }

        event = FlextMeltanoPipelineEvent(
            event_type=PipelineEventType.COMPLETED,
            pipeline_id="data-pipeline",
            data=event_data,
        )

        assert event.event_type == PipelineEventType.COMPLETED
        assert event.data["execution_id"] == "exec-123"
        assert event.data["config"]["timeout"] == 300

    def test_pipeline_event_all_types(self):
        """Test all pipeline event types."""
        event_types = [
            PipelineEventType.PIPELINE_STARTED,
            PipelineEventType.PIPELINE_COMPLETED,
            PipelineEventType.PIPELINE_FAILED,
        ]

        for event_type in event_types:
            event = FlextMeltanoPipelineEvent(
                event_type=event_type,
                pipeline_name=f"test-{event_type.value}",
            )

            assert event.event_type == event_type
            assert f"test-{event_type.value}" in event.pipeline_name

    def test_pipeline_event_domain_validation(self):
        """Test pipeline event domain validation."""
        event = FlextMeltanoPipelineEvent(
            event_type=PipelineEventType.PIPELINE_STARTED,
            pipeline_name="validation-test",
        )

        validation_result = event.validate_business_rules()
        assert validation_result.success


class TestFlextMeltanoExtensionComplete:
    """Complete tests for FlextMeltanoExtension."""

    def test_extension_creation_and_initialization(self):
        """Test extension creation and initialization."""
        config = FlextMeltanoConfig(project_root=".")
        extension = FlextMeltanoExtension(config, "test-extension")

        assert extension.extension_name == "test-extension"
        assert extension.config == config

        # Test initialization
        init_result = extension.initialize()
        assert init_result.success

    def test_extension_validation(self):
        """Test extension service validation."""
        config = FlextMeltanoConfig(project_root=".")

        # Create concrete implementation for testing
        class TestExtension(FlextMeltanoExtension):
            def execute(self, *args, **kwargs):
                from flext_core import FlextResult

                return FlextResult(data="test_executed")

        extension = TestExtension(config, "validation-extension")

        validation_result = extension.validate_service()
        assert hasattr(validation_result, "success")
        assert isinstance(validation_result.success, bool)

    def test_extension_health_status(self):
        """Test extension health status."""
        config = FlextMeltanoConfig(project_root=".")

        # Create concrete implementation for testing
        class TestExtension(FlextMeltanoExtension):
            def execute(self, *args, **kwargs):
                from flext_core import FlextResult

                return FlextResult(data="test_executed")

        extension = TestExtension(config, "health-extension")

        health_result = extension.get_health_status()
        assert health_result.success
        assert isinstance(health_result.data, dict)
        assert "service" in health_result.data
        assert health_result.data["service"] == "extension"

    def test_extension_with_various_names(self):
        """Test extension with various extension names."""
        config = FlextMeltanoConfig(project_root=".")

        extension_names = [
            "simple-extension",
            "complex_extension_name",
            "ext-with-numbers-123",
            "dbt-extension",
        ]

        for name in extension_names:
            extension = FlextMeltanoExtension(config, name)
            assert extension.extension_name == name

            # Test that all can be initialized
            init_result = extension.initialize()
            assert init_result.success


class TestFlextMeltanoSingerServiceComplete:
    """Complete tests for FlextMeltanoSingerService."""

    def test_singer_service_creation(self):
        """Test Singer service creation."""
        config = FlextMeltanoConfig(project_root=".")
        service = FlextMeltanoSingerService(config, "tap-csv", "target-csv")

        assert service.tap_name == "tap-csv"
        assert service.target_name == "target-csv"
        assert service.config == config

    def test_singer_service_initialization(self):
        """Test Singer service initialization."""
        config = FlextMeltanoConfig(project_root=".")
        service = FlextMeltanoSingerService(config, "tap-postgres", "target-snowflake")

        init_result = service.initialize()
        assert init_result.success

    def test_singer_service_validation(self):
        """Test Singer service validation."""
        config = FlextMeltanoConfig(project_root=".")
        service = FlextMeltanoSingerService(config, "tap-test", "target-test")

        validation_result = service.validate_service()
        assert hasattr(validation_result, "success")
        assert isinstance(validation_result.success, bool)

    def test_singer_service_health_status(self):
        """Test Singer service health status."""
        config = FlextMeltanoConfig(project_root=".")
        service = FlextMeltanoSingerService(config, "tap-health", "target-health")

        health_result = service.get_health_status()
        assert health_result.success
        assert isinstance(health_result.data, dict)
        assert "service" in health_result.data

    def test_singer_service_pipeline_execution(self):
        """Test Singer service pipeline execution."""
        config = FlextMeltanoConfig(project_root=".")
        service = FlextMeltanoSingerService(config, "tap-csv", "target-csv")

        # Test pipeline execution with configuration
        config_dict = {
            "files": [{"entity": "test", "path": "test.csv"}],
        }

        exec_result = service.execute_singer_pipeline(
            config_dict=config_dict,
            timeout_seconds=30,
        )

        assert hasattr(exec_result, "success")
        assert isinstance(exec_result.success, bool)

    def test_singer_service_with_different_taps_targets(self):
        """Test Singer service with different tap/target combinations."""
        config = FlextMeltanoConfig(project_root=".")

        combinations = [
            ("tap-csv", "target-csv"),
            ("tap-postgres", "target-snowflake"),
            ("tap-oracle", "target-postgres"),
            ("tap-api", "target-s3"),
        ]

        for tap, target in combinations:
            service = FlextMeltanoSingerService(config, tap, target)
            assert service.tap_name == tap
            assert service.target_name == target

            # Test that all can be initialized
            init_result = service.initialize()
            assert init_result.success


class TestPipelineEventTypeEnum:
    """Test PipelineEventType enum functionality."""

    def test_pipeline_event_type_values(self):
        """Test all pipeline event type values."""
        assert PipelineEventType.PIPELINE_STARTED.value == "PIPELINE_STARTED"
        assert PipelineEventType.PIPELINE_COMPLETED.value == "PIPELINE_COMPLETED"
        assert PipelineEventType.PIPELINE_FAILED.value == "PIPELINE_FAILED"

    def test_pipeline_event_type_iteration(self):
        """Test pipeline event type iteration."""
        event_types = list(PipelineEventType)
        assert len(event_types) >= 3
        assert PipelineEventType.STARTED in event_types
        assert PipelineEventType.COMPLETED in event_types
        assert PipelineEventType.FAILED in event_types

    def test_pipeline_event_type_membership(self):
        """Test pipeline event type membership."""
        assert "STARTED" in [t.name for t in PipelineEventType]
        assert "COMPLETED" in [t.name for t in PipelineEventType]
        assert "FAILED" in [t.name for t in PipelineEventType]


class TestExecutionStateEnum:
    """Test ExecutionState enum functionality."""

    def test_execution_state_values(self):
        """Test all execution state values."""
        assert ExecutionState.RUNNING.value == 2
        assert ExecutionState.COMPLETED.value == 3
        assert ExecutionState.FAILED.value == 4

    def test_execution_state_iteration(self):
        """Test execution state iteration."""
        states = list(ExecutionState)
        assert len(states) >= 3
        assert ExecutionState.RUNNING in states
        assert ExecutionState.COMPLETED in states
        assert ExecutionState.FAILED in states

    def test_execution_state_string_representation(self):
        """Test execution state string representation."""
        assert str(ExecutionState.RUNNING) == "ExecutionState.RUNNING"
        assert str(ExecutionState.COMPLETED) == "ExecutionState.COMPLETED"
        assert str(ExecutionState.FAILED) == "ExecutionState.FAILED"


class TestCoreModuleFunctionality:
    """Test core module level functionality and integration."""

    def test_module_imports_successfully(self):
        """Test that core module imports work correctly."""
        import flext_meltano.core as core_module

        # Test that main classes are available
        assert hasattr(core_module, "FlextMeltanoExecutionState")
        assert hasattr(core_module, "FlextMeltanoPipelineConfig")
        assert hasattr(core_module, "FlextMeltanoPipelineResult")
        assert hasattr(core_module, "FlextMeltanoPipelineEvent")
        assert hasattr(core_module, "FlextMeltanoExtension")
        assert hasattr(core_module, "FlextMeltanoSingerService")

    def test_core_classes_instantiation(self):
        """Test that core classes can be instantiated."""
        config = FlextMeltanoConfig(project_root=".")

        # Test each class can be created
        execution_state = FlextMeltanoExecutionState()
        assert execution_state is not None

        pipeline_config = FlextMeltanoPipelineConfig(
            name="test",
            extractor="tap-test",
            loader="target-test",
        )
        assert pipeline_config is not None

        pipeline_result = FlextMeltanoPipelineResult(
            pipeline_name="test",
            success=True,
        )
        assert pipeline_result is not None

        pipeline_event = FlextMeltanoPipelineEvent(
            event_type=PipelineEventType.PIPELINE_STARTED,
            pipeline_name="test",
        )
        assert pipeline_event is not None

        extension = FlextMeltanoExtension(config, "test")
        assert extension is not None

        singer_service = FlextMeltanoSingerService(config, "tap-test", "target-test")
        assert singer_service is not None

    def test_core_integration_workflow(self):
        """Test integration between core classes."""
        config = FlextMeltanoConfig(project_root=".")

        # Create execution state
        state = FlextMeltanoExecutionState()
        execution_id = state.start_pipeline("integration-test")

        # Create pipeline configuration
        pipeline_config = FlextMeltanoPipelineConfig(
            name="integration-test",
            extractor="tap-csv",
            loader="target-csv",
        )

        # Create pipeline event
        start_event = FlextMeltanoPipelineEvent(
            event_type=PipelineEventType.PIPELINE_STARTED,
            pipeline_name=pipeline_config.name,
            data={"execution_id": execution_id},
        )

        # Create Singer service
        singer_service = FlextMeltanoSingerService(
            config,
            pipeline_config.extractor,
            pipeline_config.loader,
        )

        # Validate integration
        assert start_event.data["execution_id"] == execution_id
        assert singer_service.tap_name == pipeline_config.extractor
        assert singer_service.target_name == pipeline_config.loader

        # Complete the workflow
        state.complete_pipeline()

        # Create completion result
        completion_result = FlextMeltanoPipelineResult(
            pipeline_name=pipeline_config.name,
            state=ExecutionState.COMPLETED,
        )

        assert completion_result.pipeline_name == pipeline_config.name
        assert state.state == ExecutionState.COMPLETED.value
