"""Tests for advanced helpers - comprehensive validation."""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from flext_meltano.helpers.advanced import (
    BatchProcessor,
    MeltanoProject,
    PipelineSpec,
    PluginSpec,
    batch_process_tables,
    setup_project,
)
from flext_meltano.helpers.execution import FlextMeltanoResult


class TestPluginSpec:
    """Test PluginSpec dataclass."""

    def test_plugin_spec_creation(self) -> None:
        """Test basic plugin spec creation."""
        spec = PluginSpec("tap-csv", "extractor")

        assert spec.name == "tap-csv"
        assert spec.type == "extractor"
        assert spec.variant is None
        assert spec.config == {}
        assert spec.install is True

    def test_plugin_spec_with_config(self) -> None:
        """Test plugin spec with configuration."""
        config = {"host": "localhost", "port": 5432}
        spec = PluginSpec(
            "tap-postgres",
            "extractor",
            variant="meltanolabs",
            config=config,
            install=False,
        )

        assert spec.name == "tap-postgres"
        assert spec.type == "extractor"
        assert spec.variant == "meltanolabs"
        assert spec.config == config
        assert spec.install is False


class TestPipelineSpec:
    """Test PipelineSpec dataclass."""

    def test_pipeline_spec_creation(self) -> None:
        """Test basic pipeline spec creation."""
        spec = PipelineSpec("test_pipeline", "tap-csv", "target-csv")

        assert spec.name == "test_pipeline"
        assert spec.tap == "tap-csv"
        assert spec.target == "target-csv"
        assert spec.transform is None
        assert spec.schedule is None
        assert spec.select is None
        assert spec.config == {}

    def test_pipeline_spec_with_all_options(self) -> None:
        """Test pipeline spec with all options."""
        spec = PipelineSpec(
            "complex_pipeline",
            "tap-postgres",
            "target-csv",
            transform="dbt:run",
            schedule="@daily",
            select=["users", "orders"],
            config={"batch_size": 1000},
        )

        assert spec.name == "complex_pipeline"
        assert spec.tap == "tap-postgres"
        assert spec.target == "target-csv"
        assert spec.transform == "dbt:run"
        assert spec.schedule == "@daily"
        assert spec.select == ["users", "orders"]
        assert spec.config == {"batch_size": 1000}


class TestMeltanoProject:
    """Test MeltanoProject advanced manager."""

    @pytest.fixture
    def temp_project(self) -> Path:
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def mock_commands(self) -> tuple[Mock, ...]:
        """Mock all Meltano command executions."""
        with patch(
            "flext_meltano.helpers.advanced.flext_meltano_run_command",
        ) as mock_cmd:
            # Default successful response
            mock_cmd.return_value = FlextMeltanoResult.ok(
                {
                    "stdout": "Success",
                    "stderr": "",
                    "returncode": 0,
                },
            )
            yield (mock_cmd,)

    def test_project_initialization(self, temp_project: Path) -> None:
        """Test project manager initialization."""
        project = MeltanoProject(temp_project)

        assert project.project_root == temp_project
        assert temp_project.exists()  # Should create directory

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_setup_complete_basic(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test complete project setup."""
        mock_cmd.return_value = FlextMeltanoResult.ok({})

        project = MeltanoProject(temp_project)
        result = project.setup_complete()

        assert result.success is True
        assert result.data["environments_created"] == ["dev", "staging", "prod"]

        # Should call meltano init if meltano.yml doesn't exist
        mock_cmd.assert_called()

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_setup_complete_custom_environments(
        self,
        mock_cmd: Mock,
        temp_project: Path,
    ) -> None:
        """Test setup with custom environments."""
        mock_cmd.return_value = FlextMeltanoResult.ok({})

        project = MeltanoProject(temp_project)
        result = project.setup_complete(environments=["dev", "test", "prod"])

        assert result.success is True
        assert result.data["environments_created"] == ["dev", "test", "prod"]

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_install_plugins_success(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test successful bulk plugin installation."""
        mock_cmd.return_value = FlextMeltanoResult.ok({})

        plugins = [
            PluginSpec("tap-csv", "extractor"),
            PluginSpec("target-csv", "loader"),
            PluginSpec("tap-postgres", "extractor", config={"host": "localhost"}),
        ]

        project = MeltanoProject(temp_project)
        result = project.install_plugins(plugins)

        assert result.success is True
        assert result.data["count",] == 3
        assert result.data["installed"] == ["tap-csv", "target-csv", "tap-postgres"]

        # Should be called for each plugin + config calls
        assert mock_cmd.call_count >= 3

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_install_plugins_partial_failure(
        self,
        mock_cmd: Mock,
        temp_project: Path,
    ) -> None:
        """Test plugin installation with partial failures."""
        # First plugin succeeds, second fails
        mock_cmd.side_effect = [
            FlextMeltanoResult.ok({}),  # tap-csv success
            FlextMeltanoResult.fail("Plugin not found"),  # tap-invalid failure
        ]

        plugins = [
            PluginSpec("tap-csv", "extractor"),
            PluginSpec("tap-invalid", "extractor"),
        ]

        project = MeltanoProject(temp_project)
        result = project.install_plugins(plugins)

        assert result.success is False
        assert "Plugin installation errors" in result.error
        assert "tap-invalid" in result.error

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_create_pipelines_success(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test successful pipeline creation."""
        mock_cmd.return_value = FlextMeltanoResult.ok({})

        pipelines = [
            PipelineSpec(
                "daily_users",
                "tap-postgres",
                "target-csv",
                schedule="@daily",
            ),
            PipelineSpec("hourly_orders", "tap-postgres", "target-postgres"),
        ]

        project = MeltanoProject(temp_project)
        result = project.create_pipelines(pipelines)

        assert result.success is True
        assert result.data["count",] == 2
        assert result.data["created"] == ["daily_users", "hourly_orders"]

        # Should call job add for each pipeline + schedule for first one
        assert mock_cmd.call_count >= 2

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_run_all_pipelines(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test running all configured pipelines."""
        # Mock job list response
        mock_cmd.side_effect = [
            FlextMeltanoResult.ok(
                {
                    "stdout": "pipeline1\npipeline2\npipeline3",
                    "stderr": "",
                    "returncode": 0,
                },
            ),
            # Mock individual pipeline runs
            FlextMeltanoResult.ok({}),  # pipeline1
            FlextMeltanoResult.ok({}),  # pipeline2
            FlextMeltanoResult.fail("Pipeline failed"),  # pipeline3
        ]

        project = MeltanoProject(temp_project)
        results = project.run_all_pipelines()

        assert len(results) == 3
        assert results["pipeline1",].success is True
        assert results["pipeline2",].success is True
        assert results["pipeline3",].success is False

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_health_check(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test comprehensive health check."""
        # Mock various health check commands
        mock_cmd.side_effect = [
            FlextMeltanoResult.ok(
                {"stdout": "meltano, version 3.8.0"},
            ),  # version check
            FlextMeltanoResult.ok(
                {"stdout": "extractors.tap-csv\nloaders.target-csv"},
            ),  # config list
            FlextMeltanoResult.ok({"stdout": "dev\nstaging\nprod"}),  # environment list
            FlextMeltanoResult.ok({}),  # database check
        ]

        project = MeltanoProject(temp_project)
        health = project.health_check()

        assert health["healthy",] is True
        assert len(health["issues",]) == 0
        assert health["plugins"]["extractors",] == 1
        assert health["plugins"]["loaders",] == 1
        assert health["environments"] == ["dev", "staging", "prod"]
        assert health["database"]["configured",] is True

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_health_check_with_issues(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test health check with various issues."""
        mock_cmd.side_effect = [
            FlextMeltanoResult.fail("Meltano not found"),  # version check fails
            FlextMeltanoResult.fail("Cannot list config"),  # config list fails
            FlextMeltanoResult.ok({"stdout": "dev"}),  # environment list succeeds
            FlextMeltanoResult.fail("Database not configured"),  # database check fails
        ]

        project = MeltanoProject(temp_project)
        health = project.health_check()

        assert health["healthy",] is False
        assert len(health["issues",]) >= 2
        assert "Meltano CLI not accessible" in health["issues",]
        assert "Database not configured" in health["issues",]

    def test_environment_context_manager(self, temp_project: Path) -> None:
        """Test environment context manager."""
        project = MeltanoProject(temp_project)

        # Default environment should be 'dev'
        original_env = getattr(project, "_current_env", "dev")

        with project.environment_context("prod") as prod_project:
            assert prod_project is project
            assert project._current_env == "prod"

        # Should restore original environment
        assert getattr(project, "_current_env", "dev") == original_env

    @patch("shutil.copytree")
    def test_backup_project(self, mock_copytree: Mock, temp_project: Path) -> None:
        """Test project backup functionality."""
        mock_copytree.return_value = None

        project = MeltanoProject(temp_project)
        backup_path = temp_project.parent / "backup"

        with patch.object(project, "health_check", return_value={"healthy": True}):
            result = project.backup_project(backup_path)

        assert result.success is True
        assert result.data["backup_path",] == str(backup_path)
        mock_copytree.assert_called_once()


class TestBatchProcessor:
    """Test BatchProcessor for bulk operations."""

    @pytest.fixture
    def temp_project(self) -> Path:
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_batch_processor_initialization(self, temp_project: Path) -> None:
        """Test batch processor initialization."""
        processor = BatchProcessor(temp_project, environment="staging")

        assert processor.project_root == temp_project
        assert processor.environment == "staging"

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_process_tables_sequential(
        self,
        mock_cmd: Mock,
        temp_project: Path,
    ) -> None:
        """Test sequential table processing."""
        # Mock successful responses for config and run commands
        mock_cmd.return_value = FlextMeltanoResult.ok({})

        processor = BatchProcessor(temp_project)
        tables = ["users", "orders", "products"]

        results = processor.process_tables("tap-postgres", "target-csv", tables)

        assert len(results) == 3
        assert all(result.success for result in results.values())
        assert all(table in results for table in tables)

        # Should call config + run for each table
        assert mock_cmd.call_count == len(tables) * 2

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_process_tables_with_failures(
        self,
        mock_cmd: Mock,
        temp_project: Path,
    ) -> None:
        """Test table processing with some failures."""
        # Mock mixed success/failure responses
        mock_cmd.side_effect = [
            FlextMeltanoResult.ok({}),  # users config
            FlextMeltanoResult.ok({}),  # users run
            FlextMeltanoResult.fail("Config failed"),  # orders config failure
            FlextMeltanoResult.ok({}),  # products config
            FlextMeltanoResult.fail("Run failed"),  # products run failure
        ]

        processor = BatchProcessor(temp_project)
        tables = ["users", "orders", "products"]

        results = processor.process_tables("tap-postgres", "target-csv", tables)

        assert len(results) == 3
        assert results["users",].success is True
        assert results["orders",].success is False  # Config failed
        assert results["products",].success is False  # Run failed

    @patch("concurrent.futures.ThreadPoolExecutor")
    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_process_tables_parallel(
        self,
        mock_cmd: Mock,
        mock_executor: Mock,
        temp_project: Path,
    ) -> None:
        """Test parallel table processing."""
        mock_cmd.return_value = FlextMeltanoResult.ok({})

        # Mock executor behavior
        mock_future = Mock()
        mock_executor.return_value.__enter__.return_value.submit.return_value = (
            mock_future
        )
        mock_executor.return_value.__enter__.return_value.wait.return_value = None

        processor = BatchProcessor(temp_project)
        tables = ["users", "orders"]

        # This will use the mocked parallel path
        processor.process_tables(
            "tap-postgres",
            "target-csv",
            tables,
            parallel=True,
            max_workers=2,
        )

        # Should have attempted to create executor
        mock_executor.assert_called_once_with(max_workers=2)

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_reset_all_states(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test bulk state reset."""
        mock_cmd.return_value = FlextMeltanoResult.ok({})

        processor = BatchProcessor(temp_project)
        result = processor.reset_all_states("tap-postgres")

        assert result.success is True
        mock_cmd.assert_called_once_with(
            ["state", "clear", "--pattern", "tap-postgres-*"],
            project_root=temp_project,
        )


class TestFactoryFunctions:
    """Test ultra-simplified factory functions."""

    @pytest.fixture
    def temp_project(self) -> Path:
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @patch("flext_meltano.helpers.advanced.MeltanoProject")
    def test_setup_project_factory(
        self,
        mock_project_class: Mock,
        temp_project: Path,
    ) -> None:
        """Test one-liner project setup."""
        # Mock project instance and its methods
        mock_project = Mock()
        mock_project.setup_complete.return_value = FlextMeltanoResult.ok({})
        mock_project.install_plugins.return_value = FlextMeltanoResult.ok({})
        mock_project.create_pipelines.return_value = FlextMeltanoResult.ok({})
        mock_project_class.return_value = mock_project

        plugins = [PluginSpec("tap-csv", "extractor")]
        pipelines = [PipelineSpec("test", "tap-csv", "target-csv")]

        result = setup_project(temp_project, plugins=plugins, pipelines=pipelines)

        assert result.success is True
        assert result.data["project_ready",] is True

        # Should call all setup methods
        mock_project.setup_complete.assert_called_once()
        mock_project.install_plugins.assert_called_once_with(plugins)
        mock_project.create_pipelines.assert_called_once_with(pipelines)

    @patch("flext_meltano.helpers.advanced.MeltanoProject")
    def test_setup_project_plugin_failure(
        self,
        mock_project_class: Mock,
        temp_project: Path,
    ) -> None:
        """Test project setup with plugin installation failure."""
        mock_project = Mock()
        mock_project.setup_complete.return_value = FlextMeltanoResult.ok({})
        mock_project.install_plugins.return_value = FlextMeltanoResult.fail(
            "Plugin installation failed",
        )
        mock_project_class.return_value = mock_project

        plugins = [PluginSpec("tap-invalid", "extractor")]

        result = setup_project(temp_project, plugins=plugins)

        assert result.success is False
        assert "Plugin installation failed" in result.error

    @patch("flext_meltano.helpers.advanced.BatchProcessor")
    def test_batch_process_tables_factory(
        self,
        mock_processor_class: Mock,
        temp_project: Path,
    ) -> None:
        """Test one-liner batch table processing."""
        # Mock processor instance
        mock_processor = Mock()
        mock_processor.process_tables.return_value = {
            "users": FlextMeltanoResult.ok({}),
            "orders": FlextMeltanoResult.fail("Failed"),
            "products": FlextMeltanoResult.ok({}),
        }
        mock_processor_class.return_value = mock_processor

        tables = ["users", "orders", "products"]
        results = batch_process_tables(
            temp_project,
            "tap-postgres",
            "target-csv",
            tables,
        )

        assert len(results) == 3
        assert results["users",] is True
        assert results["orders",] is False
        assert results["products",] is True

        mock_processor.process_tables.assert_called_once_with(
            "tap-postgres",
            "target-csv",
            tables,
        )


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""

    @pytest.fixture
    def temp_project(self) -> Path:
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_complete_data_pipeline_setup(
        self,
        mock_cmd: Mock,
        temp_project: Path,
    ) -> None:
        """Test complete data pipeline setup scenario."""
        mock_cmd.return_value = FlextMeltanoResult.ok({})

        # Step 1: Setup project
        project = MeltanoProject(temp_project)
        setup_result = project.setup_complete(environments=["dev", "prod"])
        assert setup_result.success is True

        # Step 2: Install plugins
        plugins = [
            PluginSpec(
                "tap-postgres",
                "extractor",
                config={
                    "host": "localhost",
                    "port": 5432,
                    "database": "source_db",
                },
            ),
            PluginSpec(
                "target-postgres",
                "loader",
                config={
                    "host": "warehouse",
                    "port": 5432,
                    "database": "warehouse_db",
                },
            ),
            PluginSpec("dbt-postgres", "transformer"),
        ]
        plugin_result = project.install_plugins(plugins)
        assert plugin_result.success is True

        # Step 3: Create pipelines
        pipelines = [
            PipelineSpec(
                "daily_etl",
                "tap-postgres",
                "target-postgres",
                transform="dbt-postgres:run",
                schedule="@daily",
                select=["users", "orders", "products"],
            ),
            PipelineSpec(
                "hourly_incremental",
                "tap-postgres",
                "target-postgres",
                schedule="0 * * * *",
                select=["events", "logs"],
            ),
        ]
        pipeline_result = project.create_pipelines(pipelines)
        assert pipeline_result.success is True

        # Step 4: Health check
        with patch.object(
            project,
            "health_check",
            return_value={"healthy": True, "issues": []},
        ):
            health = project.health_check()
            assert health["healthy",] is True

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_batch_processing_workflow(
        self,
        mock_cmd: Mock,
        temp_project: Path,
    ) -> None:
        """Test realistic batch processing workflow."""
        # Mock successful responses
        mock_cmd.return_value = FlextMeltanoResult.ok({})

        # Setup batch processor
        processor = BatchProcessor(temp_project, environment="prod")

        # Process large table set
        large_table_set = [
            "customers",
            "orders",
            "order_items",
            "products",
            "categories",
            "suppliers",
            "inventory",
            "transactions",
            "user_sessions",
            "event_logs",
        ]

        # Process tables sequentially first
        results = processor.process_tables(
            "tap-postgres",
            "target-warehouse",
            large_table_set,
        )

        assert len(results) == len(large_table_set)
        assert all(result.success for result in results.values())

        # Reset states for reprocessing
        reset_result = processor.reset_all_states("tap-postgres")
        assert reset_result.success is True

    @patch("flext_meltano.helpers.advanced.flext_meltano_run_command")
    def test_error_recovery_scenario(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test error recovery and retry scenarios."""
        project = MeltanoProject(temp_project)

        # Simulate initial setup failure
        mock_cmd.side_effect = [FlextMeltanoResult.fail("Network error")]
        setup_result = project.setup_complete()
        assert setup_result.success is False

        # Simulate recovery with successful retry
        mock_cmd.side_effect = [
            FlextMeltanoResult.ok({}),
        ] * 10  # Multiple successful calls
        setup_result_retry = project.setup_complete()
        assert setup_result_retry.success is True

        # Test partial plugin installation failure and recovery
        mock_cmd.side_effect = [
            FlextMeltanoResult.ok({}),  # First plugin succeeds
            FlextMeltanoResult.fail("Plugin not found"),  # Second fails
            FlextMeltanoResult.ok({}),  # Third succeeds
        ]

        plugins = [
            PluginSpec("tap-csv", "extractor"),
            PluginSpec("tap-invalid", "extractor"),
            PluginSpec("target-csv", "loader"),
        ]

        plugin_result = project.install_plugins(plugins)
        assert plugin_result.success is False
        assert "tap-invalid" in plugin_result.error


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
