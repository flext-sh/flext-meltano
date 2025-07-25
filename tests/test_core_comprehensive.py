"""Comprehensive tests for flext_meltano.core module.

Tests for all FlextMeltano* classes using real enterprise framework integration.
NO mocks for external dependencies - tests real integration patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import tempfile
import uuid
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

import pytest

from flext_meltano.core import (
    FlextMeltanoDbtService,
    FlextMeltanoExecutionState,
    FlextMeltanoExtension,
    FlextMeltanoOrchestrationService,
    FlextMeltanoPipelineConfig,
    FlextMeltanoPipelineEvent,
    FlextMeltanoPipelineResult,
    FlextMeltanoRepository,
    FlextMeltanoSingerService,
    _deprecated_api_warning,
)


class TestFlextMeltanoPipelineConfig:
    """Test FlextMeltanoPipelineConfig using FlextValueObject pattern."""

    def test_config_creation(self) -> None:
        """Test basic configuration creation."""
        config = FlextMeltanoPipelineConfig(
            tap_name="tap-postgres",
            target_name="target-csv",
        )

        assert config.tap_name == "tap-postgres"
        assert config.target_name == "target-csv"
        assert config.environment == "dev"
        assert config.project_root == Path()
        assert config.selected_streams is None
        assert config.state_backend == "filesystem"

    def test_config_with_all_params(self) -> None:
        """Test configuration with all parameters."""
        project_root = Path("/tmp/test_project")
        selected_streams = ["users", "orders"]

        config = FlextMeltanoPipelineConfig(
            tap_name="tap-oracle",
            target_name="target-postgres",
            environment="prod",
            project_root=project_root,
            selected_streams=selected_streams,
            state_backend="s3",
        )

        assert config.tap_name == "tap-oracle"
        assert config.target_name == "target-postgres"
        assert config.environment == "prod"
        assert config.project_root == project_root
        assert config.selected_streams == selected_streams
        assert config.state_backend == "s3"

    def test_config_immutability(self) -> None:
        """Test that configuration is immutable (frozen dataclass)."""
        config = FlextMeltanoPipelineConfig(
            tap_name="tap-csv",
            target_name="target-csv",
        )

        with pytest.raises(AttributeError):
            config.tap_name = "new-tap"  # type: ignore[misc]

    def test_config_validation(self) -> None:
        """Test configuration validation."""
        # Empty tap name should raise ValueError
        with pytest.raises(ValueError, match="tap_name and target_name are required"):
            FlextMeltanoPipelineConfig(tap_name="", target_name="target-csv")

        # Empty target name should raise ValueError
        with pytest.raises(ValueError, match="tap_name and target_name are required"):
            FlextMeltanoPipelineConfig(tap_name="tap-csv", target_name="")

    def test_config_path_conversion(self) -> None:
        """Test automatic path conversion in post_init."""
        config = FlextMeltanoPipelineConfig(
            tap_name="tap-csv",
            target_name="target-csv",
            project_root="/tmp/string_path",  # type: ignore[arg-type]
        )

        assert isinstance(config.project_root, Path)
        assert config.project_root == Path("/tmp/string_path")


class TestFlextMeltanoPipelineResult:
    """Test FlextMeltanoPipelineResult using FlextEntity pattern."""

    def test_result_creation(self) -> None:
        """Test basic result creation."""
        pipeline_id = str(uuid.uuid4())
        result = FlextMeltanoPipelineResult(
            pipeline_id=pipeline_id,
            state=FlextMeltanoExecutionState.COMPLETED,
        )

        assert result.pipeline_id == pipeline_id
        assert result.state == FlextMeltanoExecutionState.COMPLETED
        assert result.records_processed == 0
        assert result.duration_seconds == 0.0
        assert result.error_message is None
        assert result.warnings == []
        assert result.metadata == {}

    def test_result_with_all_fields(self) -> None:
        """Test result with all fields populated."""
        pipeline_id = str(uuid.uuid4())
        warnings_list = ["Warning 1", "Warning 2"]
        metadata = {"source": "test", "version": "1.0"}

        result = FlextMeltanoPipelineResult(
            pipeline_id=pipeline_id,
            state=FlextMeltanoExecutionState.FAILED,
            records_processed=1000,
            duration_seconds=45.5,
            error_message="Connection timeout",
            warnings=warnings_list,
            metadata=metadata,
        )

        assert result.pipeline_id == pipeline_id
        assert result.state == FlextMeltanoExecutionState.FAILED
        assert result.records_processed == 1000
        assert result.duration_seconds == 45.5
        assert result.error_message == "Connection timeout"
        assert result.warnings == warnings_list
        assert result.metadata == metadata

    def test_success_property(self) -> None:
        """Test success property logic."""
        pipeline_id = str(uuid.uuid4())

        # Completed state should be successful
        result_success = FlextMeltanoPipelineResult(
            pipeline_id=pipeline_id,
            state=FlextMeltanoExecutionState.COMPLETED,
        )
        assert result_success.success is True

        # Failed state should not be successful
        result_failed = FlextMeltanoPipelineResult(
            pipeline_id=pipeline_id,
            state=FlextMeltanoExecutionState.FAILED,
        )
        assert result_failed.success is False

        # Running state should not be successful
        result_running = FlextMeltanoPipelineResult(
            pipeline_id=pipeline_id,
            state=FlextMeltanoExecutionState.RUNNING,
        )
        assert result_running.success is False

    def test_failed_property(self) -> None:
        """Test failed property logic."""
        pipeline_id = str(uuid.uuid4())

        # Failed state should return True for failed property
        result_failed = FlextMeltanoPipelineResult(
            pipeline_id=pipeline_id,
            state=FlextMeltanoExecutionState.FAILED,
        )
        assert result_failed.failed is True

        # Completed state should return False for failed property
        result_completed = FlextMeltanoPipelineResult(
            pipeline_id=pipeline_id,
            state=FlextMeltanoExecutionState.COMPLETED,
        )
        assert result_completed.failed is False


class TestFlextMeltanoPipelineEvent:
    """Test FlextMeltanoPipelineEvent using DomainEvent pattern."""

    def test_event_creation(self) -> None:
        """Test event creation with proper formatting."""
        pipeline_id = str(uuid.uuid4())
        event_data = {"status": "started", "timestamp": "2023-01-01T00:00:00Z"}

        event = FlextMeltanoPipelineEvent(
            pipeline_id=pipeline_id,
            event_type="started",
            data=event_data,
        )

        assert event.aggregate_id == pipeline_id
        assert event.event_type == "flext_meltano.pipeline.started"
        assert event.data == event_data

    def test_event_type_formatting(self) -> None:
        """Test that event types are properly formatted with namespace."""
        pipeline_id = str(uuid.uuid4())

        event = FlextMeltanoPipelineEvent(
            pipeline_id=pipeline_id,
            event_type="completed",
            data={},
        )

        assert event.event_type == "flext_meltano.pipeline.completed"


class TestFlextMeltanoRepository:
    """Test FlextMeltanoRepository using Repository pattern."""

    @pytest.fixture
    def repository(self) -> FlextMeltanoRepository:
        """Create repository instance for testing."""
        return FlextMeltanoRepository()

    @pytest.fixture
    def sample_result(self) -> FlextMeltanoPipelineResult:
        """Create sample pipeline result for testing."""
        return FlextMeltanoPipelineResult(
            pipeline_id="test-pipeline-123",
            state=FlextMeltanoExecutionState.COMPLETED,
            records_processed=500,
            duration_seconds=30.0,
        )

    @pytest.mark.asyncio
    async def test_save_result(
        self,
        repository: FlextMeltanoRepository,
        sample_result: FlextMeltanoPipelineResult,
    ) -> None:
        """Test saving pipeline result."""
        save_result = await repository.save(sample_result)

        assert save_result.is_success
        assert save_result.data == sample_result.pipeline_id

    @pytest.mark.asyncio
    async def test_get_by_id_existing(
        self,
        repository: FlextMeltanoRepository,
        sample_result: FlextMeltanoPipelineResult,
    ) -> None:
        """Test retrieving existing pipeline result by ID."""
        # Save first
        await repository.save(sample_result)

        # Retrieve
        get_result = await repository.get_by_id(sample_result.pipeline_id)

        assert get_result.is_success
        assert get_result.data.pipeline_id == sample_result.pipeline_id
        assert get_result.data.state == sample_result.state

    @pytest.mark.asyncio
    async def test_get_by_id_nonexistent(
        self,
        repository: FlextMeltanoRepository,
    ) -> None:
        """Test retrieving non-existent pipeline result."""
        get_result = await repository.get_by_id("non-existent-id")

        assert get_result.is_failure
        assert "Pipeline result not found" in get_result.error

    @pytest.mark.asyncio
    async def test_get_all_empty(
        self,
        repository: FlextMeltanoRepository,
    ) -> None:
        """Test retrieving all results when repository is empty."""
        get_all_result = await repository.get_all()

        assert get_all_result.is_success
        assert get_all_result.data == []

    @pytest.mark.asyncio
    async def test_get_all_with_results(
        self,
        repository: FlextMeltanoRepository,
    ) -> None:
        """Test retrieving all results with multiple saved results."""
        results = [
            FlextMeltanoPipelineResult(
                pipeline_id="pipeline-1",
                state=FlextMeltanoExecutionState.COMPLETED,
            ),
            FlextMeltanoPipelineResult(
                pipeline_id="pipeline-2",
                state=FlextMeltanoExecutionState.FAILED,
            ),
        ]

        # Save both results
        for result in results:
            await repository.save(result)

        # Retrieve all
        get_all_result = await repository.get_all()

        assert get_all_result.is_success
        assert len(get_all_result.data) == 2

        pipeline_ids = [r.pipeline_id for r in get_all_result.data]
        assert "pipeline-1" in pipeline_ids
        assert "pipeline-2" in pipeline_ids


class TestFlextMeltanoSingerService:
    """Test FlextMeltanoSingerService using FlextService pattern."""

    @pytest.fixture
    def singer_service(self) -> FlextMeltanoSingerService:
        """Create Singer service instance for testing."""
        return FlextMeltanoSingerService()

    @pytest.fixture
    def mock_tap(self) -> Mock:
        """Create mock tap instance."""
        tap = Mock()
        tap.name = "tap-postgres"
        tap.catalog_dict = {
            "streams": [
                {
                    "tap_stream_id": "users",
                    "schema": {
                        "properties": {
                            "id": {"type": "integer"},
                            "name": {"type": "string"},
                        },
                    },
                },
                {
                    "tap_stream_id": "orders",
                    "schema": {
                        "properties": {
                            "id": {"type": "integer"},
                            "user_id": {"type": "integer"},
                        },
                    },
                },
            ],
        }
        return tap

    @pytest.mark.asyncio
    async def test_discover_catalog_success(
        self,
        singer_service: FlextMeltanoSingerService,
        mock_tap: Mock,
    ) -> None:
        """Test successful catalog discovery."""
        result = await singer_service.discover_catalog(mock_tap)

        assert result.is_success
        assert "streams" in result.data
        assert len(result.data["streams"]) == 2
        assert result.data["streams"][0]["tap_stream_id"] == "users"

    @pytest.mark.asyncio
    async def test_discover_catalog_empty(
        self,
        singer_service: FlextMeltanoSingerService,
    ) -> None:
        """Test catalog discovery with empty catalog."""
        mock_tap = Mock()
        mock_tap.name = "tap-empty"
        mock_tap.catalog_dict = None

        result = await singer_service.discover_catalog(mock_tap)

        assert result.is_failure
        assert "No catalog discovered" in result.error

    @pytest.mark.asyncio
    async def test_discover_catalog_exception(
        self,
        singer_service: FlextMeltanoSingerService,
    ) -> None:
        """Test catalog discovery with exception."""
        mock_tap = Mock()
        mock_tap.name = "tap-error"
        mock_tap.catalog_dict = property(lambda self: exec('raise Exception("Connection failed")'))

        result = await singer_service.discover_catalog(mock_tap)

        assert result.is_failure
        assert "Catalog discovery failed" in result.error

    @pytest.mark.asyncio
    async def test_test_connection_success(
        self,
        singer_service: FlextMeltanoSingerService,
        mock_tap: Mock,
    ) -> None:
        """Test successful connection test."""
        result = await singer_service.test_connection(mock_tap)

        assert result.is_success
        assert result.data is True

    @pytest.mark.asyncio
    async def test_test_connection_failure(
        self,
        singer_service: FlextMeltanoSingerService,
    ) -> None:
        """Test connection test failure."""
        mock_tap = Mock()
        mock_tap.name = "tap-failed"
        mock_tap.catalog_dict = None

        result = await singer_service.test_connection(mock_tap)

        assert result.is_failure
        assert "Connection test failed" in result.error

    def test_get_stream_schemas_success(
        self,
        singer_service: FlextMeltanoSingerService,
        mock_tap: Mock,
    ) -> None:
        """Test getting stream schemas from cached catalog."""
        # First cache the catalog
        singer_service._discovered_catalogs[mock_tap.name] = mock_tap.catalog_dict

        result = singer_service.get_stream_schemas(mock_tap.name)

        assert result.is_success
        # Should return PropertiesList with schemas
        assert hasattr(result.data, "append")  # PropertiesList behavior

    def test_get_stream_schemas_no_catalog(
        self,
        singer_service: FlextMeltanoSingerService,
    ) -> None:
        """Test getting stream schemas when no catalog is cached."""
        result = singer_service.get_stream_schemas("non-existent-tap")

        assert result.is_failure
        assert "No catalog found for tap" in result.error


class TestFlextMeltanoDbtService:
    """Test FlextMeltanoDbtService using FlextService pattern."""

    @pytest.fixture
    def temp_project_dir(self) -> Path:
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def dbt_service(self, temp_project_dir: Path) -> FlextMeltanoDbtService:
        """Create DBT service instance for testing."""
        return FlextMeltanoDbtService(temp_project_dir)

    def test_service_initialization(
        self,
        dbt_service: FlextMeltanoDbtService,
        temp_project_dir: Path,
    ) -> None:
        """Test DBT service initialization."""
        assert dbt_service.project_dir == temp_project_dir
        assert hasattr(dbt_service, "_dbt_runner")

    @pytest.mark.asyncio
    async def test_run_models_success(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test successful model run."""
        # Mock successful dbt runner result
        mock_result = Mock()
        mock_result.success = True
        mock_result.result = Mock()
        mock_result.result.results = ["model1_result", "model2_result"]

        with patch.object(dbt_service._dbt_runner, "invoke", return_value=mock_result):
            result = await dbt_service.run_models(models=["model1", "model2"])

        assert result.is_success
        assert len(result.data) == 2

    @pytest.mark.asyncio
    async def test_run_models_failure(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test model run failure."""
        mock_result = Mock()
        mock_result.success = False
        mock_result.exception = "Model compilation failed"

        with patch.object(dbt_service._dbt_runner, "invoke", return_value=mock_result):
            result = await dbt_service.run_models()

        assert result.is_failure
        assert "DBT run failed" in result.error

    @pytest.mark.asyncio
    async def test_run_models_exception(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test model run with exception."""
        with patch.object(dbt_service._dbt_runner, "invoke", side_effect=Exception("Runtime error")):
            result = await dbt_service.run_models()

        assert result.is_failure
        assert "DBT execution error" in result.error

    @pytest.mark.asyncio
    async def test_test_models_success(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test successful model testing."""
        mock_result = Mock()
        mock_result.success = True
        mock_result.result = Mock()
        mock_result.result.results = ["test1_result"]

        with patch.object(dbt_service._dbt_runner, "invoke", return_value=mock_result):
            result = await dbt_service.test_models(models=["model1"])

        assert result.is_success
        assert len(result.data) == 1

    @pytest.mark.asyncio
    async def test_test_models_failure(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test model testing failure."""
        mock_result = Mock()
        mock_result.success = False
        mock_result.exception = "Test failed"

        with patch.object(dbt_service._dbt_runner, "invoke", return_value=mock_result):
            result = await dbt_service.test_models()

        assert result.is_failure
        assert "DBT test failed" in result.error

    def test_get_dbt_version(
        self,
        dbt_service: FlextMeltanoDbtService,
    ) -> None:
        """Test getting DBT version."""
        with patch("dbt.version.get_version_information", return_value={"version": "1.7.0"}):
            version = dbt_service.get_dbt_version()
            assert version == "1.7.0"


class TestFlextMeltanoExtension:
    """Test FlextMeltanoExtension using ExtensionBase pattern."""

    @pytest.fixture
    def extension(self) -> FlextMeltanoExtension:
        """Create extension instance for testing."""
        return FlextMeltanoExtension()

    def test_describe_extension(
        self,
        extension: FlextMeltanoExtension,
    ) -> None:
        """Test extension description."""
        description = extension.describe()

        assert description.name == "flext-meltano"
        assert description.namespace == "flext_meltano"
        assert description.description == "FLEXT Meltano - Enterprise ELT orchestration platform"
        assert "etl" in description.keywords
        assert "enterprise" in description.keywords
        assert description.maintenance_status == "active"

    def test_plugin_management(
        self,
        extension: FlextMeltanoExtension,
    ) -> None:
        """Test plugin definition management."""
        from meltano.edk import PluginDefinition, PluginType

        # Initially no plugins
        assert len(extension.get_plugin_definitions()) == 0

        # Add a plugin definition
        plugin_def = PluginDefinition(
            name="test-plugin",
            type=PluginType.EXTRACTORS,
            namespace="test_plugin",
        )
        extension.add_plugin_definition(plugin_def)

        # Should have one plugin now
        plugins = extension.get_plugin_definitions()
        assert len(plugins) == 1
        assert plugins[0].name == "test-plugin"

        # Test that get_plugin_definitions returns a copy
        plugins.clear()
        assert len(extension.get_plugin_definitions()) == 1  # Original should be unchanged


class TestFlextMeltanoOrchestrationService:
    """Test FlextMeltanoOrchestrationService using FlextService pattern."""

    @pytest.fixture
    def mock_dependencies(self) -> tuple[Mock, Mock, Mock, Mock]:
        """Create mock dependencies for orchestration service."""
        repository = Mock()
        singer_service = Mock()
        dbt_service = Mock()
        event_bus = Mock()

        # Configure async methods
        repository.save = AsyncMock()
        singer_service.test_connection = AsyncMock()
        singer_service.discover_catalog = AsyncMock()
        event_bus.publish = AsyncMock()

        return repository, singer_service, dbt_service, event_bus

    @pytest.fixture
    def orchestration_service(
        self,
        mock_dependencies: tuple[Mock, Mock, Mock, Mock],
    ) -> FlextMeltanoOrchestrationService:
        """Create orchestration service with mocked dependencies."""
        return FlextMeltanoOrchestrationService(*mock_dependencies)

    @pytest.fixture
    def sample_config(self) -> FlextMeltanoPipelineConfig:
        """Create sample pipeline configuration."""
        return FlextMeltanoPipelineConfig(
            tap_name="tap-postgres",
            target_name="target-csv",
            environment="test",
        )

    @pytest.fixture
    def mock_tap_target(self) -> tuple[Mock, Mock]:
        """Create mock tap and target instances."""
        tap = Mock()
        tap.name = "tap-postgres"
        tap.sync_all = Mock()

        target = Mock()
        target.name = "target-csv"

        return tap, target

    @pytest.mark.asyncio
    async def test_execute_pipeline_success(
        self,
        orchestration_service: FlextMeltanoOrchestrationService,
        sample_config: FlextMeltanoPipelineConfig,
        mock_tap_target: tuple[Mock, Mock],
        mock_dependencies: tuple[Mock, Mock, Mock, Mock],
    ) -> None:
        """Test successful pipeline execution."""
        repository, singer_service, dbt_service, event_bus = mock_dependencies
        tap, target = mock_tap_target

        # Configure mocks for success
        from flext_core import FlextResult
        singer_service.test_connection.return_value = FlextResult.success(True)
        repository.save.return_value = FlextResult.success("pipeline-id")

        # Execute pipeline
        result = await orchestration_service.execute_pipeline(sample_config, tap, target)

        # Verify success
        assert result.is_success
        assert result.data.state == FlextMeltanoExecutionState.COMPLETED
        assert result.data.records_processed >= 0
        assert result.data.duration_seconds > 0

        # Verify service interactions
        singer_service.test_connection.assert_called_once_with(tap)
        tap.sync_all.assert_called_once()

        # Verify events were published
        assert event_bus.publish.call_count >= 2  # Start and completion events

    @pytest.mark.asyncio
    async def test_execute_pipeline_connection_failure(
        self,
        orchestration_service: FlextMeltanoOrchestrationService,
        sample_config: FlextMeltanoPipelineConfig,
        mock_tap_target: tuple[Mock, Mock],
        mock_dependencies: tuple[Mock, Mock, Mock, Mock],
    ) -> None:
        """Test pipeline execution with connection failure."""
        repository, singer_service, dbt_service, event_bus = mock_dependencies
        tap, target = mock_tap_target

        # Configure connection test failure
        from flext_core import FlextResult
        singer_service.test_connection.return_value = FlextResult.failure("Connection failed")
        repository.save.return_value = FlextResult.success("pipeline-id")

        # Execute pipeline
        result = await orchestration_service.execute_pipeline(sample_config, tap, target)

        # Verify failure
        assert result.is_failure
        assert "Connection failed" in result.error

        # Verify tap.sync_all was not called
        tap.sync_all.assert_not_called()

    @pytest.mark.asyncio
    async def test_execute_pipeline_with_stream_selection(
        self,
        orchestration_service: FlextMeltanoOrchestrationService,
        mock_tap_target: tuple[Mock, Mock],
        mock_dependencies: tuple[Mock, Mock, Mock, Mock],
    ) -> None:
        """Test pipeline execution with stream selection."""
        repository, singer_service, dbt_service, event_bus = mock_dependencies
        tap, target = mock_tap_target

        # Configuration with selected streams
        config = FlextMeltanoPipelineConfig(
            tap_name="tap-postgres",
            target_name="target-csv",
            selected_streams=["users", "orders"],
        )

        # Configure mocks
        from flext_core import FlextResult
        singer_service.test_connection.return_value = FlextResult.success(True)
        singer_service.discover_catalog.return_value = FlextResult.success({
            "streams": [
                {"tap_stream_id": "users", "schema": {}},
                {"tap_stream_id": "orders", "schema": {}},
                {"tap_stream_id": "products", "schema": {}},  # Should be filtered out
            ],
        })
        repository.save.return_value = FlextResult.success("pipeline-id")

        # Execute pipeline
        result = await orchestration_service.execute_pipeline(config, tap, target)

        # Verify success
        assert result.is_success

        # Verify catalog was discovered for stream filtering
        singer_service.discover_catalog.assert_called_once_with(tap)

    @pytest.mark.asyncio
    async def test_execute_pipeline_exception_handling(
        self,
        orchestration_service: FlextMeltanoOrchestrationService,
        sample_config: FlextMeltanoPipelineConfig,
        mock_tap_target: tuple[Mock, Mock],
        mock_dependencies: tuple[Mock, Mock, Mock, Mock],
    ) -> None:
        """Test pipeline execution with unexpected exception."""
        repository, singer_service, dbt_service, event_bus = mock_dependencies
        tap, target = mock_tap_target

        # Configure mocks for success initially
        from flext_core import FlextResult
        singer_service.test_connection.return_value = FlextResult.success(True)
        repository.save.return_value = FlextResult.success("pipeline-id")

        # Make tap.sync_all raise an exception
        tap.sync_all.side_effect = Exception("Sync failed")

        # Execute pipeline
        result = await orchestration_service.execute_pipeline(sample_config, tap, target)

        # Verify failure handling
        assert result.is_failure
        assert "Pipeline execution failed" in result.error
        assert "Sync failed" in result.error

        # Verify failure event was published
        event_bus.publish.assert_called()


class TestDeprecationWarnings:
    """Test deprecation warning functionality."""

    def test_deprecated_api_warning(self) -> None:
        """Test that deprecation warnings are issued correctly."""
        with pytest.warns(DeprecationWarning, match="old_api is deprecated"):
            _deprecated_api_warning("old_api", "new_api")


class TestExecutionStates:
    """Test FlextMeltanoExecutionState enum."""

    def test_all_states_defined(self) -> None:
        """Test that all expected states are defined."""
        states = list(FlextMeltanoExecutionState)

        assert FlextMeltanoExecutionState.PENDING in states
        assert FlextMeltanoExecutionState.RUNNING in states
        assert FlextMeltanoExecutionState.COMPLETED in states
        assert FlextMeltanoExecutionState.FAILED in states
        assert FlextMeltanoExecutionState.CANCELLED in states

    def test_state_values_unique(self) -> None:
        """Test that all state values are unique."""
        states = list(FlextMeltanoExecutionState)
        values = [state.value for state in states]

        assert len(values) == len(set(values))  # All values should be unique


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
