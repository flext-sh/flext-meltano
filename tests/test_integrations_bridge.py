"""Test FLEXT Meltano integrations bridge.

Comprehensive tests for bridge functionality to achieve required coverage.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

# Mock missing dependencies to avoid import errors
sys.modules["flext_observability"] = MagicMock()
sys.modules["flext_observability.logging"] = MagicMock()

# ruff: noqa: E402 - Module mocking must happen before imports
from flext_meltano.integrations.bridge import (
    FlextMeltanoBridge,
    FlextMeltanoResult,
    execute_command_sync,
    flext_add_plugin_sync,
    flext_get_bridge,
    flext_get_project_info_sync,
    flext_init_project_sync,
    flext_run_pipeline_sync,
    is_available,
)


class TestFlextMeltanoResult:
    """Test FlextMeltanoResult class."""

    def test_result_creation_success(self) -> None:
        """Test creating a successful result."""
        result = FlextMeltanoResult(
            success=True,
            message="Operation completed",
            data={"key": "value"},
            metadata={"meta": "data"},
        )

        assert result.success is True
        assert result.message == "Operation completed"
        assert result.data == {"key": "value"}
        assert result.metadata == {"meta": "data"}
        assert result.error is None

    def test_result_creation_failure(self) -> None:
        """Test creating a failure result."""
        result = FlextMeltanoResult(
            success=False,
            message="Operation failed",
            error="Error details",
        )

        assert result.success is False
        assert result.message == "Operation failed"
        assert result.error == "Error details"
        assert result.data is None

    def test_result_to_dict(self) -> None:
        """Test converting result to dictionary."""
        result = FlextMeltanoResult(
            success=True,
            message="Test message",
            data={"test": "data"},
            metadata={"test": "meta"},
            error="Test error",
        )

        result_dict = result.to_dict()

        assert isinstance(result_dict, dict)
        assert result_dict["success"] is True
        assert result_dict["message"] == "Test message"
        assert result_dict["data"] == {"test": "data"}
        assert result_dict["metadata"] == {"test": "meta"}
        assert result_dict["error"] == "Test error"


class TestFlextMeltanoBridge:
    """Test FlextMeltanoBridge class."""

    @pytest.fixture
    def mock_project_manager(self) -> MagicMock:
        """Create mock project manager."""
        manager = MagicMock()
        manager.create_project_bridge = AsyncMock()
        manager.add_plugin_bridge = AsyncMock()
        manager.run_command_bridge = AsyncMock()
        manager.load_project_config = AsyncMock()
        return manager

    @pytest.fixture
    def mock_singer_direct(self) -> MagicMock:
        """Create mock singer direct runner."""
        return MagicMock()

    @pytest.fixture
    def bridge(self, mock_project_manager: MagicMock, mock_singer_direct: MagicMock) -> FlextMeltanoBridge:
        """Create bridge instance with mocked dependencies."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager", return_value=mock_project_manager),
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner", return_value=mock_singer_direct),
            patch("flext_meltano.config.settings.FlextMeltanoSettings"),
            patch("flext_meltano.infrastructure.di_container.get_di_container"),
        ):
            return FlextMeltanoBridge("/test/project")

    def test_bridge_initialization(
        self,
        mock_project_manager: MagicMock,
        mock_singer_direct: MagicMock,
    ) -> None:
        """Test bridge initialization."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager", return_value=mock_project_manager),
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner", return_value=mock_singer_direct),
            patch("flext_meltano.config.settings.FlextMeltanoSettings"),
            patch("flext_meltano.infrastructure.di_container.get_di_container"),
        ):
            bridge = FlextMeltanoBridge("/test/project")

            assert bridge.project_root == Path("/test/project").resolve()
            assert bridge.project_manager == mock_project_manager
            assert bridge.singer_direct == mock_singer_direct
            assert bridge.logger is not None

    def test_is_available(self, bridge: FlextMeltanoBridge) -> None:
        """Test availability check."""
        result = bridge.is_available()
        assert result is True

    async def test_init_project_success(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test successful project initialization."""
        from flext_core import FlextResult

        mock_project_manager.create_project_bridge.return_value = FlextResult.ok(
            {"project_id": "test-project"},
        )

        result_json = await bridge.init_project("test-project", "/test/dir")
        result = json.loads(result_json)

        assert result["success"] is True
        assert result["message"] == "Project initialized successfully"
        assert result["data"]["project_name"] == "test-project"
        assert result["data"]["project_dir"] == "/test/dir"

        mock_project_manager.create_project_bridge.assert_called_once_with(
            project_name="test-project",
            environment="dev",
        )

    async def test_init_project_failure(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test failed project initialization."""
        from flext_core import FlextResult

        mock_project_manager.create_project_bridge.return_value = FlextResult.fail(
            "Project creation failed",
        )

        result_json = await bridge.init_project("test-project")
        result = json.loads(result_json)

        assert result["success"] is False
        assert result["message"] == "Failed to initialize"
        assert result["error"] == "Project creation failed"

    async def test_init_project_exception(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test project initialization with exception."""
        mock_project_manager.create_project_bridge.side_effect = Exception("Test error")

        result_json = await bridge.init_project("test-project")
        result = json.loads(result_json)

        assert result["success"] is False
        assert result["message"] == "Failed to initialize"
        assert result["error"] == "Test error"

    async def test_add_plugin_success(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test successful plugin addition."""
        from flext_core import FlextResult

        mock_project_manager.add_plugin_bridge.return_value = FlextResult.ok(
            {"plugin_id": "tap-csv"},
        )

        result_json = await bridge.add_plugin(
            "test-project",
            "extractors",
            "tap-csv",
            "singer-io",
        )
        result = json.loads(result_json)

        assert result["success"] is True
        assert result["message"] == "Plugin added successfully"
        assert result["data"]["plugin_type"] == "extractors"
        assert result["data"]["plugin_name"] == "tap-csv"
        assert result["data"]["plugin_variant"] == "singer-io"
        assert result["metadata"]["flext_result"] == "success"

        mock_project_manager.add_plugin_bridge.assert_called_once_with(
            project_name="test-project",
            plugin_type="extractors",
            plugin_name="tap-csv",
            variant="singer-io",
        )

    async def test_add_plugin_failure(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test failed plugin addition."""
        from flext_core import FlextResult

        mock_project_manager.add_plugin_bridge.return_value = FlextResult.fail(
            "Plugin not found",
        )

        result_json = await bridge.add_plugin(
            "test-project",
            "extractors",
            "invalid-plugin",
        )
        result = json.loads(result_json)

        assert result["success"] is False
        assert result["message"] == "Failed to add plugin"
        assert result["error"] == "Plugin not found"
        assert result["metadata"]["flext_result"] == "failure"

    async def test_add_plugin_exception(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test plugin addition with exception."""
        mock_project_manager.add_plugin_bridge.side_effect = Exception("Test error")

        result_json = await bridge.add_plugin(
            "test-project",
            "extractors",
            "tap-csv",
        )
        result = json.loads(result_json)

        assert result["success"] is False
        assert result["message"] == "Plugin addition failed"
        assert result["error"] == "Test error"

    async def test_run_pipeline_success_with_transformer(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test successful pipeline run with transformer."""
        from flext_core import FlextResult

        mock_project_manager.run_command_bridge.return_value = FlextResult.ok(
            {"status": "completed", "output": "success"},
        )

        result_json = await bridge.run_pipeline(
            "test-project",
            "tap-csv",
            "target-jsonl",
            "dbt:run",
        )
        result = json.loads(result_json)

        assert result["success"] is True
        assert result["message"] == "Pipeline executed successfully"
        assert result["data"]["extractor"] == "tap-csv"
        assert result["data"]["loader"] == "target-jsonl"
        assert result["data"]["transformer"] == "dbt:run"

        mock_project_manager.run_command_bridge.assert_called_once_with(
            project_name="test-project",
            command_args=["run", "tap-csv", "dbt:run", "target-jsonl"],
            environment="dev",
        )

    async def test_run_pipeline_success_without_transformer(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test successful pipeline run without transformer."""
        from flext_core import FlextResult

        mock_project_manager.run_command_bridge.return_value = FlextResult.ok(
            {"status": "completed"},
        )

        result_json = await bridge.run_pipeline(
            "test-project",
            "tap-csv",
            "target-jsonl",
        )
        result = json.loads(result_json)

        assert result["success"] is True
        assert result["message"] == "Pipeline executed successfully"

        mock_project_manager.run_command_bridge.assert_called_once_with(
            project_name="test-project",
            command_args=["el", "tap-csv", "target-jsonl"],
            environment="dev",
        )

    async def test_run_pipeline_failure(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test failed pipeline run."""
        from flext_core import FlextResult

        mock_project_manager.run_command_bridge.return_value = FlextResult.fail(
            "Pipeline failed",
        )

        result_json = await bridge.run_pipeline(
            "test-project",
            "tap-csv",
            "target-jsonl",
        )
        result = json.loads(result_json)

        assert result["success"] is False
        assert result["message"] == "Pipeline execution failed"
        assert result["error"] == "Pipeline failed"

    async def test_run_pipeline_exception(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test pipeline run with exception."""
        mock_project_manager.run_command_bridge.side_effect = Exception("Test error")

        result_json = await bridge.run_pipeline(
            "test-project",
            "tap-csv",
            "target-jsonl",
        )
        result = json.loads(result_json)

        assert result["success"] is False
        assert result["message"] == "Pipeline execution error"
        assert result["error"] == "Test error"

    async def test_get_project_info_success(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test successful project info retrieval."""
        from flext_core import FlextResult

        project_data = {"name": "test-project", "version": "1.0.0"}
        mock_project_manager.load_project_config.return_value = FlextResult.ok(project_data)

        result_json = await bridge.get_project_info("test-project")
        result = json.loads(result_json)

        assert result["success"] is True
        assert result["message"] == "Project info retrieved successfully"
        assert result["data"]["project_name"] == "test-project"
        assert result["data"]["project_info"] == project_data

        mock_project_manager.load_project_config.assert_called_once_with("test-project")

    async def test_get_project_info_failure(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test failed project info retrieval."""
        from flext_core import FlextResult

        mock_project_manager.load_project_config.return_value = FlextResult.fail(
            "Project not found",
        )

        result_json = await bridge.get_project_info("nonexistent-project")
        result = json.loads(result_json)

        assert result["success"] is False
        assert result["message"] == "Failed to get project info"
        assert result["error"] == "Project not found"

    async def test_get_project_info_exception(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test project info retrieval with exception."""
        mock_project_manager.load_project_config.side_effect = Exception("Test error")

        result_json = await bridge.get_project_info("test-project")
        result = json.loads(result_json)

        assert result["success"] is False
        assert result["message"] == "Project info retrieval error"
        assert result["error"] == "Test error"

    async def test_execute_command_success(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test successful command execution."""
        from flext_core import FlextResult

        command_output = {"stdout": "Command output", "stderr": ""}
        mock_project_manager.run_command_bridge.return_value = FlextResult.ok(command_output)

        command_args = ["config", "list"]
        result_json = await bridge.execute_command("test-project", command_args)
        result = json.loads(result_json)

        assert result["success"] is True
        assert result["message"] == "Command executed successfully"
        assert result["data"]["project_name"] == "test-project"
        assert result["data"]["args"] == command_args
        assert result["data"]["result"] == command_output

        mock_project_manager.run_command_bridge.assert_called_once_with(
            project_name="test-project",
            command_args=command_args,
            environment="dev",
        )

    async def test_execute_command_failure(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test failed command execution."""
        from flext_core import FlextResult

        mock_project_manager.run_command_bridge.return_value = FlextResult.fail(
            "Command failed",
        )

        result_json = await bridge.execute_command("test-project", ["invalid", "command"])
        result = json.loads(result_json)

        assert result["success"] is False
        assert result["message"] == "Command execution failed"
        assert result["error"] == "Command failed"

    async def test_execute_command_exception(
        self,
        bridge: FlextMeltanoBridge,
        mock_project_manager: MagicMock,
    ) -> None:
        """Test command execution with exception."""
        mock_project_manager.run_command_bridge.side_effect = Exception("Test error")

        result_json = await bridge.execute_command("test-project", ["test"])
        result = json.loads(result_json)

        assert result["success"] is False
        assert result["message"] == "Command execution error"
        assert result["error"] == "Test error"


class TestGlobalFunctions:
    """Test global bridge functions."""

    def test_flext_get_bridge(self) -> None:
        """Test getting global bridge instance."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager"),
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner"),
            patch("flext_meltano.config.settings.FlextMeltanoSettings"),
            patch("flext_meltano.infrastructure.di_container.get_di_container"),
        ):
            # Clear global instance first
            import flext_meltano.integrations.bridge
            flext_meltano.integrations.bridge._bridge_instance = None

            bridge1 = flext_get_bridge()
            bridge2 = flext_get_bridge()

            assert bridge1 is not None
            assert bridge1 is bridge2  # Should return the same instance

    def test_is_available(self) -> None:
        """Test availability check through global function."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager"),
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner"),
            patch("flext_meltano.config.settings.FlextMeltanoSettings"),
            patch("flext_meltano.infrastructure.di_container.get_di_container"),
        ):
            result = is_available()
            assert result is True


class TestSyncWrapperFunctions:
    """Test synchronous wrapper functions for Go compatibility."""

    def test_flext_init_project_sync_success(self) -> None:
        """Test synchronous project initialization."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager"),
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner"),
            patch("flext_meltano.config.settings.FlextMeltanoSettings"),
            patch("flext_meltano.infrastructure.di_container.get_di_container"),
            patch("asyncio.new_event_loop") as mock_new_loop,
        ):
            mock_loop = MagicMock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete.return_value = '{"success": true}'

            result = flext_init_project_sync(
                "/test/root",
                project_name="test-project",
                project_dir="/test/dir",
            )

            assert result == '{"success": true}'
            mock_loop.run_until_complete.assert_called_once()
            mock_loop.close.assert_called_once()

    def test_flext_init_project_sync_exception(self) -> None:
        """Test synchronous project initialization with exception."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager"),
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner"),
            patch("flext_meltano.config.settings.FlextMeltanoSettings"),
            patch("flext_meltano.infrastructure.di_container.get_di_container"),
            patch("asyncio.new_event_loop", side_effect=Exception("Test error")),
        ):
            result = flext_init_project_sync("/test/root", project_name="test-project")
            assert "Error: Test error" in result

    def test_flext_add_plugin_sync_success(self) -> None:
        """Test synchronous plugin addition."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager"),
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner"),
            patch("flext_meltano.config.settings.FlextMeltanoSettings"),
            patch("flext_meltano.infrastructure.di_container.get_di_container"),
            patch("asyncio.new_event_loop") as mock_new_loop,
        ):
            mock_loop = MagicMock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete.return_value = '{"success": true}'

            result = flext_add_plugin_sync(
                "extractors",
                "tap-csv",
                project_name="test-project",
                plugin_variant="singer-io",
            )

            assert result == '{"success": true}'

    def test_flext_run_pipeline_sync_success(self) -> None:
        """Test synchronous pipeline execution."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager"),
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner"),
            patch("flext_meltano.config.settings.FlextMeltanoSettings"),
            patch("flext_meltano.infrastructure.di_container.get_di_container"),
            patch("asyncio.new_event_loop") as mock_new_loop,
        ):
            mock_loop = MagicMock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete.return_value = '{"success": true}'

            result = flext_run_pipeline_sync(
                "test-pipeline",
                project_name="test-project",
                extractor="tap-csv",
                loader="target-jsonl",
                transformer="dbt:run",
            )

            assert result == '{"success": true}'

    def test_flext_get_project_info_sync_success(self) -> None:
        """Test synchronous project info retrieval."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager"),
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner"),
            patch("flext_meltano.config.settings.FlextMeltanoSettings"),
            patch("flext_meltano.infrastructure.di_container.get_di_container"),
            patch("asyncio.new_event_loop") as mock_new_loop,
        ):
            mock_loop = MagicMock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete.return_value = '{"success": true}'

            result = flext_get_project_info_sync(project_name="test-project")

            assert result == '{"success": true}'

    def test_execute_command_sync_success(self) -> None:
        """Test synchronous command execution."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager"),
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner"),
            patch("flext_meltano.config.settings.FlextMeltanoSettings"),
            patch("flext_meltano.infrastructure.di_container.get_di_container"),
            patch("asyncio.new_event_loop") as mock_new_loop,
        ):
            mock_loop = MagicMock()
            mock_new_loop.return_value = mock_loop
            mock_loop.run_until_complete.return_value = '{"success": true}'

            result = execute_command_sync(
                '["config", "list"]',
                project_name="test-project",
            )

            assert result == '{"success": true}'

    def test_execute_command_sync_invalid_json(self) -> None:
        """Test synchronous command execution with invalid JSON."""
        with (
            patch("flext_meltano.integrations.bridge.FlextMeltanoProjectManager"),
            patch("flext_meltano.integrations.bridge.FlextMeltanoSingerDirectRunner"),
            patch("flext_meltano.config.settings.FlextMeltanoSettings"),
            patch("flext_meltano.infrastructure.di_container.get_di_container"),
            patch("asyncio.new_event_loop") as mock_new_loop,
        ):
            mock_loop = MagicMock()
            mock_new_loop.return_value = mock_loop
            # Simulate JSON decode error
            mock_loop.run_until_complete.side_effect = json.JSONDecodeError("Invalid JSON", "doc", 0)

            result = execute_command_sync("invalid json", project_name="test-project")
            result_dict = json.loads(result)

            assert result_dict["success"] is False
            assert result_dict["message"] == "Invalid JSON in command arguments"
            assert result_dict["error"] == "Could not parse command arguments as JSON"
