"""Comprehensive tests for the new FLEXT Meltano API.

Tests para validar todas as funcionalidades da nova API ultra-simplificada
com foco em redução massiva de código e usabilidade extrema.
"""

from __future__ import annotations

import asyncio
import json
import tempfile
import time
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from flext_meltano.api import (
    FlextMeltano,
    PipelineConfig,
    PipelineResult,
    async_run_pipeline,
    discover_catalog,
    run_pipeline,
    test_tap_connection,
)
from flext_meltano.helpers.execution import FlextMeltanoResult


class TestPipelineConfig:
    """Test PipelineConfig dataclass."""

    def test_pipeline_config_creation(self) -> None:
        """Test basic pipeline config creation."""
        config = PipelineConfig(tap="tap-csv", target="target-csv")

        assert config.tap == "tap-csv"
        assert config.target == "target-csv"
        assert config.environment == "dev"
        assert config.select is None
        assert config.state_backend == "filesystem"

    def test_pipeline_config_to_dict(self) -> None:
        """Test config serialization."""
        config = PipelineConfig(
            tap="tap-postgres",
            target="target-csv",
            environment="prod",
            project_root="/custom/path",
            select=["users", "orders"],
            state_backend="s3",
        )

        result = config.to_dict()

        assert result["tap"] == "tap-postgres"
        assert result["target"] == "target-csv"
        assert result["environment"] == "prod"
        assert result["project_root"] == "/custom/path"
        assert result["select"] == ["users", "orders"]
        assert result["state_backend"] == "s3"


class TestPipelineResult:
    """Test PipelineResult dataclass."""

    def test_pipeline_result_success(self) -> None:
        """Test successful pipeline result."""
        result = PipelineResult(
            success=True,
            duration=10.5,
            records_processed=100,
            errors=[],
            warnings=["minor warning"],
            state={"bookmarks": {"users": "2025-01-25"}},
            metadata={"command": "meltano run tap-csv target-csv"},
        )

        assert result.success is True
        assert result.failed is False
        assert result.has_errors is False
        assert result.has_warnings is True
        assert result.duration == 10.5
        assert result.records_processed == 100

    def test_pipeline_result_failure(self) -> None:
        """Test failed pipeline result."""
        result = PipelineResult(
            success=False,
            duration=5.0,
            records_processed=0,
            errors=["Connection failed", "Invalid config"],
            warnings=[],
            state={},
            metadata={},
        )

        assert result.success is False
        assert result.failed is True
        assert result.has_errors is True
        assert result.has_warnings is False
        assert len(result.errors) == 2


class TestFlextMeltano:
    """Test FlextMeltano main class."""

    @pytest.fixture
    def temp_project(self) -> Path:
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def mock_meltano(self) -> None:
        """Mock Meltano command execution."""
        with patch("flext_meltano.api.flext_meltano_run_command") as mock_cmd, \
             patch("flext_meltano.api.flext_meltano_execute_job") as mock_job:

            # Default successful responses
            mock_cmd.return_value = FlextMeltanoResult.ok({
                "stdout": "meltano, version 3.8.0",
                "stderr": "",
                "returncode": 0,
            })

            mock_job.return_value = FlextMeltanoResult.ok({
                "stdout": "Run completed. 5 records extracted.",
                "stderr": "",
                "returncode": 0,
            })

            yield mock_cmd, mock_job

    def test_flext_meltano_initialization(self, temp_project: Path) -> None:
        """Test FlextMeltano initialization."""
        fm = FlextMeltano(
            project_root=temp_project,
            environment="staging",
            auto_install=False,
            state_backend="s3",
        )

        assert fm.project_root == temp_project
        assert fm.environment == "staging"
        assert fm.auto_install is False
        assert fm.state_backend == "s3"
        assert fm._initialized is False

    @patch("flext_meltano.api.flext_meltano_execute_job")
    def test_run_pipeline_basic(self, mock_job: Mock, temp_project: Path) -> None:
        """Test basic pipeline execution."""
        mock_job.return_value = FlextMeltanoResult.ok({
            "stdout": "Run completed. 5 records extracted.",
            "stderr": "",
            "returncode": 0,
        })

        fm = FlextMeltano(project_root=temp_project, auto_install=False)

        # Mock project initialization
        with patch.object(fm, "_ensure_project_setup"):
            result = fm.run("tap-csv", "target-csv")

        assert isinstance(result, PipelineResult)
        assert result.success is True
        assert result.records_processed == 5  # Extracted from stdout
        assert result.duration > 0

        mock_job.assert_called_once()

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_add_tap_chainable(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test chainable tap addition."""
        mock_cmd.return_value = FlextMeltanoResult.ok({})

        fm = FlextMeltano(project_root=temp_project)

        result = fm.add_tap("tap-csv", variant="meltanolabs", config={"path": "/data"})

        assert result is fm  # Chainable
        mock_cmd.assert_called()

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_add_target_chainable(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test chainable target addition."""
        mock_cmd.return_value = FlextMeltanoResult.ok({})

        fm = FlextMeltano(project_root=temp_project)

        result = fm.add_target("target-csv", config={"destination_path": "/output"})

        assert result is fm  # Chainable
        mock_cmd.assert_called()

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_discover_catalog(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test catalog discovery."""
        catalog_data = {
            "streams": [
                {"tap_stream_id": "users", "schema": {"properties": {"id": {"type": "integer"}}}},
                {"tap_stream_id": "orders", "schema": {"properties": {"id": {"type": "integer"}}}},
            ],
        }

        mock_cmd.return_value = FlextMeltanoResult.ok({
            "stdout": json.dumps(catalog_data),
            "stderr": "",
            "returncode": 0,
        })

        fm = FlextMeltano(project_root=temp_project)
        catalog = fm.discover("tap-postgres")

        assert catalog == catalog_data
        assert len(catalog["streams"]) == 2
        assert catalog["streams"][0]["tap_stream_id"] == "users"

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_discover_catalog_failure(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test catalog discovery failure."""
        mock_cmd.return_value = FlextMeltanoResult.fail("Connection failed")

        fm = FlextMeltano(project_root=temp_project)

        with pytest.raises(RuntimeError, match="Failed to discover tap-postgres"):
            fm.discover("tap-postgres")

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_test_connection_success(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test successful connection test."""
        mock_cmd.return_value = FlextMeltanoResult.ok({
            "stdout": json.dumps({"streams": []}),
            "stderr": "",
            "returncode": 0,
        })

        fm = FlextMeltano(project_root=temp_project)
        result = fm.test_connection("tap-postgres")

        assert result is True

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_test_connection_failure(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test connection test failure."""
        mock_cmd.return_value = FlextMeltanoResult.fail("Connection failed")

        fm = FlextMeltano(project_root=temp_project)
        result = fm.test_connection("tap-postgres")

        assert result is False

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_get_state(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test state retrieval."""
        state_data = {"bookmarks": {"users": {"version": 1, "datetime": "2025-01-25T10:00:00Z"}}}

        mock_cmd.return_value = FlextMeltanoResult.ok({
            "stdout": json.dumps(state_data),
            "stderr": "",
            "returncode": 0,
        })

        fm = FlextMeltano(project_root=temp_project)
        state = fm.get_state("tap-postgres", "target-csv")

        assert state == state_data
        assert "bookmarks" in state

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_reset_state(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test state reset."""
        mock_cmd.return_value = FlextMeltanoResult.ok({})

        fm = FlextMeltano(project_root=temp_project)
        result = fm.reset_state("tap-postgres", "target-csv")

        assert result is True
        mock_cmd.assert_called_with(
            ["state", "clear", "tap-postgres-to-target-csv"],
            project_root=temp_project,
        )

    @pytest.mark.asyncio
    async def test_async_context_manager(self, temp_project: Path) -> None:
        """Test async context manager."""
        fm = FlextMeltano(project_root=temp_project)

        async with fm.async_context() as async_fm:
            assert async_fm is fm

    @pytest.mark.asyncio
    @patch("flext_meltano.api.flext_meltano_execute_job")
    async def test_async_run(self, mock_job: Mock, temp_project: Path) -> None:
        """Test async pipeline execution."""
        mock_job.return_value = FlextMeltanoResult.ok({
            "stdout": "Run completed. 10 records extracted.",
            "stderr": "",
            "returncode": 0,
        })

        fm = FlextMeltano(project_root=temp_project, auto_install=False)

        with patch.object(fm, "_ensure_project_setup"):
            result = await fm.async_run("tap-csv", "target-csv")

        assert isinstance(result, PipelineResult)
        assert result.success is True
        assert result.records_processed == 10

    def test_method_chaining(self, temp_project: Path) -> None:
        """Test fluent method chaining."""
        fm = FlextMeltano(project_root=temp_project)

        with patch("flext_meltano.api.flext_meltano_run_command") as mock_cmd, \
             patch("flext_meltano.api.flext_meltano_execute_job") as mock_job, \
             patch.object(fm, "_ensure_project_setup"):

            mock_cmd.return_value = FlextMeltanoResult.ok({})
            mock_job.return_value = FlextMeltanoResult.ok({
                "stdout": "Run completed. 3 records extracted.",
                "stderr": "",
                "returncode": 0,
            })

            # Test method chaining
            result = (fm
                     .add_tap("tap-csv")
                     .add_target("target-csv")
                     .run("tap-csv", "target-csv"))

            assert isinstance(result, PipelineResult)
            assert result.success is True
            assert mock_cmd.call_count == 2  # add_tap + add_target


class TestFactoryFunctions:
    """Test ultra-simplified factory functions."""

    @pytest.fixture
    def temp_project(self) -> Path:
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @patch("flext_meltano.api.flext_meltano_execute_job")
    def test_run_pipeline_factory(self, mock_job: Mock, temp_project: Path) -> None:
        """Test one-liner pipeline execution."""
        mock_job.return_value = FlextMeltanoResult.ok({
            "stdout": "Run completed. 7 records extracted.",
            "stderr": "",
            "returncode": 0,
        })

        with patch("flext_meltano.api.FlextMeltano._ensure_project_setup"):
            result = run_pipeline("tap-csv", "target-csv", project_root=temp_project)

        assert isinstance(result, PipelineResult)
        assert result.success is True
        assert result.records_processed == 7

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_discover_catalog_factory(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test one-liner catalog discovery."""
        catalog_data = {"streams": [{"tap_stream_id": "test_table"}]}
        mock_cmd.return_value = FlextMeltanoResult.ok({
            "stdout": json.dumps(catalog_data),
            "stderr": "",
            "returncode": 0,
        })

        catalog = discover_catalog("tap-postgres", project_root=temp_project)

        assert catalog == catalog_data

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_test_tap_connection_factory(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test one-liner connection test."""
        mock_cmd.return_value = FlextMeltanoResult.ok({
            "stdout": json.dumps({"streams": []}),
            "stderr": "",
            "returncode": 0,
        })

        result = test_tap_connection("tap-postgres", project_root=temp_project)

        assert result is True

    @pytest.mark.asyncio
    @patch("flext_meltano.api.flext_meltano_execute_job")
    async def test_async_run_pipeline_factory(self, mock_job: Mock, temp_project: Path) -> None:
        """Test async one-liner pipeline execution."""
        mock_job.return_value = FlextMeltanoResult.ok({
            "stdout": "Run completed. 12 records extracted.",
            "stderr": "",
            "returncode": 0,
        })

        with patch("flext_meltano.api.FlextMeltano._ensure_project_setup"):
            result = await async_run_pipeline("tap-csv", "target-csv", project_root=temp_project)

        assert isinstance(result, PipelineResult)
        assert result.success is True
        assert result.records_processed == 12


class TestErrorHandling:
    """Test comprehensive error handling."""

    @pytest.fixture
    def temp_project(self) -> Path:
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_add_tap_failure(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test tap addition failure."""
        mock_cmd.return_value = FlextMeltanoResult.fail("Plugin not found")

        fm = FlextMeltano(project_root=temp_project)

        with pytest.raises(RuntimeError, match="Failed to add tap tap-invalid"):
            fm.add_tap("tap-invalid")

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_discover_invalid_json(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test discovery with invalid JSON."""
        mock_cmd.return_value = FlextMeltanoResult.ok({
            "stdout": "invalid json response",
            "stderr": "",
            "returncode": 0,
        })

        fm = FlextMeltano(project_root=temp_project)

        with pytest.raises(RuntimeError, match="Invalid catalog JSON"):
            fm.discover("tap-postgres")

    @patch("flext_meltano.api.flext_meltano_execute_job")
    def test_run_pipeline_failure(self, mock_job: Mock, temp_project: Path) -> None:
        """Test pipeline execution failure."""
        mock_job.return_value = FlextMeltanoResult.fail("Connection timeout")

        fm = FlextMeltano(project_root=temp_project, auto_install=False)

        with patch.object(fm, "_ensure_project_setup"):
            result = fm.run("tap-postgres", "target-csv")

        assert result.success is False
        assert "Connection timeout" in result.errors
        assert result.records_processed == 0

    @patch("flext_meltano.api.flext_meltano_run_command")
    def test_configure_plugin_failure(self, mock_cmd: Mock, temp_project: Path) -> None:
        """Test plugin configuration failure."""
        # First call succeeds (add plugin), second fails (configure)
        mock_cmd.side_effect = [
            FlextMeltanoResult.ok({}),  # add plugin success
            FlextMeltanoResult.fail("Invalid config key"),  # configure failure
        ]

        fm = FlextMeltano(project_root=temp_project)

        with pytest.raises(RuntimeError, match="Failed to configure"):
            fm.add_tap("tap-csv", config={"invalid_key": "value"})


class TestPerformanceAndMetrics:
    """Test performance characteristics and metrics extraction."""

    @pytest.fixture
    def temp_project(self) -> Path:
        """Create temporary project directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @patch("flext_meltano.api.flext_meltano_execute_job")
    def test_metrics_extraction(self, mock_job: Mock, temp_project: Path) -> None:
        """Test metrics extraction from output."""
        mock_job.return_value = FlextMeltanoResult.ok({
            "stdout": """
            INFO Starting extraction
            INFO 150 records extracted from users table
            INFO 75 records extracted from orders table
            INFO Run completed successfully
            """,
            "stderr": "",
            "returncode": 0,
        })

        fm = FlextMeltano(project_root=temp_project, auto_install=False)

        with patch.object(fm, "_ensure_project_setup"):
            result = fm.run("tap-postgres", "target-csv")

        assert result.success is True
        # Should extract first occurrence of record count
        assert result.records_processed == 150
        assert result.duration > 0

    @patch("flext_meltano.api.flext_meltano_execute_job")
    def test_duration_measurement(self, mock_job: Mock, temp_project: Path) -> None:
        """Test duration measurement accuracy."""
        # Mock a slow execution
        def slow_execution(*args, **kwargs):
            time.sleep(0.1)  # 100ms delay
            return FlextMeltanoResult.ok({
                "stdout": "Run completed. 1 records extracted.",
                "stderr": "",
                "returncode": 0,
            })

        mock_job.side_effect = slow_execution

        fm = FlextMeltano(project_root=temp_project, auto_install=False)

        with patch.object(fm, "_ensure_project_setup"):
            result = fm.run("tap-csv", "target-csv")

        assert result.success is True
        assert result.duration >= 0.1  # At least 100ms
        assert result.duration < 1.0   # But reasonable

    @pytest.mark.asyncio
    @patch("flext_meltano.api.flext_meltano_execute_job")
    async def test_concurrent_execution(self, mock_job: Mock, temp_project: Path) -> None:
        """Test concurrent pipeline execution."""
        call_count = 0

        def counting_execution(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return FlextMeltanoResult.ok({
                "stdout": f"Run completed. {call_count} records extracted.",
                "stderr": "",
                "returncode": 0,
            })

        mock_job.side_effect = counting_execution

        # Run 3 pipelines concurrently
        tasks = []
        for _i in range(3):
            task = async_run_pipeline("tap-csv", "target-csv", project_root=temp_project)
            tasks.append(task)

        with patch("flext_meltano.api.FlextMeltano._ensure_project_setup"):
            results = await asyncio.gather(*tasks)

        assert len(results) == 3
        assert all(result.success for result in results)
        assert call_count == 3  # All 3 pipelines executed


class TestRegressionPrevention:
    """Regression tests to prevent breaking changes."""

    def test_api_stability(self) -> None:
        """Test that public API remains stable."""
        # Test that all expected classes and functions exist
        from flext_meltano.api import (
            FlextMeltano,
        )

        # Test that classes have expected methods
        fm = FlextMeltano()
        assert hasattr(fm, "run")
        assert hasattr(fm, "add_tap")
        assert hasattr(fm, "add_target")
        assert hasattr(fm, "discover")
        assert hasattr(fm, "test_connection")
        assert hasattr(fm, "get_state")
        assert hasattr(fm, "reset_state")
        assert hasattr(fm, "async_context")
        assert hasattr(fm, "async_run")

    def test_backward_compatibility(self) -> None:
        """Test backward compatibility with original interfaces."""
        # Test that original execution functions still work
        from flext_meltano.helpers.execution import (
            FlextMeltanoResult,
            flext_meltano_execute_job,
            flext_meltano_run_command,
        )

        # These should remain available for legacy code
        assert callable(flext_meltano_execute_job)
        assert callable(flext_meltano_run_command)
        assert FlextMeltanoResult is not None

    def test_import_compatibility(self) -> None:
        """Test that imports work as expected."""
        # Test main API imports
        from flext_meltano.api import FlextMeltano
        from flext_meltano.helpers.advanced import BatchProcessor, MeltanoProject

        # Test that classes can be instantiated
        fm = FlextMeltano()
        project = MeltanoProject("/tmp")
        processor = BatchProcessor("/tmp")

        assert fm is not None
        assert project is not None
        assert processor is not None


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
