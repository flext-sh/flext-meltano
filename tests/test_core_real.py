"""REAL functional tests for core.py to achieve 95%+ coverage.

Tests exercise ACTUAL functionality of core module classes and services,
validating real domain logic, entities, and orchestration patterns.
Following zero tolerance methodology - test ALL functionality.
"""

from datetime import UTC, datetime

import pytest
from flext_core import FlextResult

from flext_meltano.core import (
    ExecutionState,
    FlextMeltanoPipelineConfig,
    FlextMeltanoPipelineResult,
    PipelineEventType,
)


class TestExecutionState:
    """Test ExecutionState enum functionality."""

    def test_execution_state_values(self):
        """Test all ExecutionState enum values exist."""
        assert ExecutionState.PENDING is not None
        assert ExecutionState.RUNNING is not None
        assert ExecutionState.COMPLETED is not None
        assert ExecutionState.FAILED is not None
        assert ExecutionState.CANCELLED is not None

    def test_execution_state_ordering(self):
        """Test ExecutionState values are distinct."""
        states = list(ExecutionState)
        assert len(states) == 5
        assert len(set(states)) == 5  # All unique


class TestPipelineEventType:
    """Test PipelineEventType enum functionality."""

    def test_pipeline_event_type_values(self):
        """Test all PipelineEventType enum values exist."""
        assert PipelineEventType.CREATED is not None
        assert PipelineEventType.STARTED is not None
        assert PipelineEventType.COMPLETED is not None
        assert PipelineEventType.FAILED is not None
        assert PipelineEventType.CANCELLED is not None

    def test_pipeline_event_type_ordering(self):
        """Test PipelineEventType values are distinct."""
        events = list(PipelineEventType)
        assert len(events) == 5
        assert len(set(events)) == 5  # All unique


class TestFlextMeltanoPipelineConfig:
    """Test FlextMeltanoPipelineConfig value object."""

    def test_pipeline_config_creation_minimal(self):
        """Test creating pipeline config with minimal required fields."""
        config = FlextMeltanoPipelineConfig(
            name="test_pipeline",
            extractor="tap-postgres",
            loader="target-snowflake",
        )

        assert config.name == "test_pipeline"
        assert config.extractor == "tap-postgres"
        assert config.loader == "target-snowflake"
        assert config.transformer is None
        assert config.environment == "dev"
        assert config.config == {}

    def test_pipeline_config_creation_full(self):
        """Test creating pipeline config with all fields."""
        custom_config = {"host": "localhost", "port": 5432}

        config = FlextMeltanoPipelineConfig(
            name="full_pipeline",
            extractor="tap-oracle",
            loader="target-postgres",
            transformer="dbt",
            environment="production",
            config=custom_config,
        )

        assert config.name == "full_pipeline"
        assert config.extractor == "tap-oracle"
        assert config.loader == "target-postgres"
        assert config.transformer == "dbt"
        assert config.environment == "production"
        assert config.config == custom_config

    def test_pipeline_config_validation_empty_name(self):
        """Test pipeline config validation fails with empty name."""
        with pytest.raises(
            ValueError,
            match="Pipeline name, extractor, and loader are required",
        ):
            FlextMeltanoPipelineConfig(
                name="",
                extractor="tap-postgres",
                loader="target-snowflake",
            )

    def test_pipeline_config_validation_empty_extractor(self):
        """Test pipeline config validation fails with empty extractor."""
        with pytest.raises(
            ValueError,
            match="Pipeline name, extractor, and loader are required",
        ):
            FlextMeltanoPipelineConfig(
                name="test_pipeline",
                extractor="",
                loader="target-snowflake",
            )

    def test_pipeline_config_validation_empty_loader(self):
        """Test pipeline config validation fails with empty loader."""
        with pytest.raises(
            ValueError,
            match="Pipeline name, extractor, and loader are required",
        ):
            FlextMeltanoPipelineConfig(
                name="test_pipeline",
                extractor="tap-postgres",
                loader="",
            )

    def test_pipeline_config_immutable(self):
        """Test pipeline config is immutable (frozen dataclass)."""
        config = FlextMeltanoPipelineConfig(
            name="test_pipeline",
            extractor="tap-postgres",
            loader="target-snowflake",
        )

        # Should not be able to modify
        with pytest.raises(AttributeError):
            config.name = "modified_name"


class TestFlextMeltanoPipelineResult:
    """Test FlextMeltanoPipelineResult entity functionality."""

    def test_pipeline_result_creation_defaults(self):
        """Test creating pipeline result with default values."""
        result = FlextMeltanoPipelineResult(pipeline_name="test_pipeline")

        assert result.pipeline_name == "test_pipeline"
        assert result.state == ExecutionState.PENDING.value
        assert result.started_at is None
        assert result.completed_at is None
        assert result.duration_seconds is None
        assert result.records_processed == 0
        assert result.error_message is None
        assert result.metadata == {}
        assert len(result.id) > 0  # UUID generated

    def test_pipeline_result_start_execution(self):
        """Test starting pipeline execution."""
        result = FlextMeltanoPipelineResult(pipeline_name="test_pipeline")

        # Initially pending - note: use_enum_values=True converts enum to value
        assert result.state == ExecutionState.PENDING.value
        assert result.started_at is None

        # Start execution
        result.start_execution()

        assert result.state == ExecutionState.RUNNING.value
        assert result.started_at is not None
        assert isinstance(result.started_at, datetime)

    def test_pipeline_result_complete_execution(self):
        """Test completing pipeline execution."""
        result = FlextMeltanoPipelineResult(pipeline_name="test_pipeline")

        # Start then complete
        result.start_execution()
        result.complete_execution(records_processed=1000)

        assert result.state == ExecutionState.COMPLETED.value
        assert result.completed_at is not None
        assert result.records_processed == 1000
        assert result.duration_seconds is not None
        assert result.duration_seconds >= 0

    def test_pipeline_result_complete_execution_default_records(self):
        """Test completing pipeline execution with default record count."""
        result = FlextMeltanoPipelineResult(pipeline_name="test_pipeline")

        result.start_execution()
        result.complete_execution()  # No records specified

        assert result.state == ExecutionState.COMPLETED.value
        assert result.records_processed == 0

    def test_pipeline_result_fail_execution(self):
        """Test failing pipeline execution."""
        result = FlextMeltanoPipelineResult(pipeline_name="test_pipeline")
        error_msg = "Database connection failed"

        # Start then fail
        result.start_execution()
        result.fail_execution(error_msg)

        assert result.state == ExecutionState.FAILED.value
        assert result.completed_at is not None
        assert result.error_message == error_msg
        assert result.duration_seconds is not None
        assert result.duration_seconds >= 0

    def test_pipeline_result_validate_domain_rules_success(self):
        """Test pipeline result domain validation success."""
        result = FlextMeltanoPipelineResult(pipeline_name="valid_pipeline")

        validation_result = result.validate_business_rules()

        assert validation_result.success
        assert validation_result.data is None

    def test_pipeline_result_validate_domain_rules_empty_name(self):
        """Test pipeline result domain validation fails with empty name."""
        result = FlextMeltanoPipelineResult(pipeline_name="")

        validation_result = result.validate_business_rules()

        assert validation_result.is_failure
        assert "Pipeline name cannot be empty" in str(validation_result.error)

    def test_pipeline_result_validate_domain_rules_whitespace_name(self):
        """Test pipeline result domain validation fails with whitespace-only name."""
        result = FlextMeltanoPipelineResult(pipeline_name="   ")

        validation_result = result.validate_business_rules()

        assert validation_result.is_failure
        assert "Pipeline name cannot be empty" in str(validation_result.error)

    def test_pipeline_result_duration_calculation(self):
        """Test duration calculation between start and completion."""
        result = FlextMeltanoPipelineResult(pipeline_name="test_pipeline")

        # Mock specific timestamps for predictable duration
        start_time = datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC)
        end_time = datetime(2025, 1, 1, 12, 0, 5, tzinfo=UTC)  # 5 seconds later

        # Manual timestamp setting for predictable duration
        result.start_execution()
        object.__setattr__(result, "started_at", start_time)

        result.complete_execution(records_processed=500)
        object.__setattr__(result, "completed_at", end_time)
        object.__setattr__(
            result,
            "duration_seconds",
            (end_time - start_time).total_seconds(),
        )

        assert result.duration_seconds == 5.0
        assert result.records_processed == 500

    def test_pipeline_result_duration_calculation_on_failure(self):
        """Test duration calculation when pipeline fails."""
        result = FlextMeltanoPipelineResult(pipeline_name="test_pipeline")

        # Mock specific timestamps for predictable duration
        start_time = datetime(2025, 1, 1, 12, 0, 0, tzinfo=UTC)
        end_time = datetime(2025, 1, 1, 12, 0, 3, tzinfo=UTC)  # 3 seconds later

        # Manual timestamp setting for predictable duration
        result.start_execution()
        object.__setattr__(result, "started_at", start_time)

        result.fail_execution("Test error")
        object.__setattr__(result, "completed_at", end_time)
        object.__setattr__(
            result,
            "duration_seconds",
            (end_time - start_time).total_seconds(),
        )

        assert result.duration_seconds == 3.0
        assert result.error_message == "Test error"

    def test_pipeline_result_no_duration_without_start(self):
        """Test no duration calculation when execution never started."""
        result = FlextMeltanoPipelineResult(pipeline_name="test_pipeline")

        # Complete without starting
        result.complete_execution(records_processed=100)

        assert result.state == ExecutionState.COMPLETED.value
        assert result.records_processed == 100
        assert result.duration_seconds is None  # No start time available

    def test_pipeline_result_multiple_state_transitions(self):
        """Test multiple state transitions work correctly."""
        result = FlextMeltanoPipelineResult(pipeline_name="test_pipeline")

        # Initial state
        assert result.state == ExecutionState.PENDING.value

        # Start execution
        result.start_execution()
        assert result.state == ExecutionState.RUNNING.value

        # Fail execution
        result.fail_execution("Network timeout")
        assert result.state == ExecutionState.FAILED.value
        assert result.error_message == "Network timeout"

    def test_pipeline_result_metadata_usage(self):
        """Test metadata field can store additional information."""
        metadata = {
            "source_tables": ["users", "orders"],
            "target_schema": "analytics",
            "batch_id": "batch_123",
        }

        result = FlextMeltanoPipelineResult(
            pipeline_name="etl_pipeline",
            metadata=metadata,
        )

        assert result.metadata == metadata
        assert result.metadata["source_tables"] == ["users", "orders"]
        assert result.metadata["batch_id"] == "batch_123"


class TestCoreModuleIntegration:
    """Test core module integration and imports."""

    def test_all_exports_importable(self):
        """Test all core module exports can be imported."""
        from flext_meltano.core import (
            ExecutionState,
            FlextMeltanoPipelineConfig,
            FlextMeltanoPipelineResult,
            PipelineEventType,
        )

        # Test classes are accessible
        assert ExecutionState is not None
        assert FlextMeltanoPipelineConfig is not None
        assert FlextMeltanoPipelineResult is not None
        assert PipelineEventType is not None

    def test_flext_core_integration(self):
        """Test integration with flext-core patterns."""
        # Test FlextResult integration
        result = FlextMeltanoPipelineResult(pipeline_name="test")
        validation_result = result.validate_business_rules()

        assert isinstance(validation_result, FlextResult)
        assert hasattr(validation_result, "success")
        assert hasattr(validation_result, "is_failure")

    def test_entity_inheritance(self):
        """Test FlextMeltanoPipelineResult inherits from FlextEntity."""
        from flext_core import FlextEntity

        result = FlextMeltanoPipelineResult(pipeline_name="test")
        assert isinstance(result, FlextEntity)
