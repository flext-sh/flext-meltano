"""Test module for flext-meltano."""

import asyncio
from pathlib import Path
from unittest import mock

from flext_core import FlextResult
from flext_meltano.executors_bridge import FlextMeltanoBridge


class TestFlextMeltanoBridgeErrorCoverage:
    """Test suite for error coverage scenarios."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.bridge = FlextMeltanoBridge()

    def test_get_version_adapter_failure(self) -> None:
        """Test get_version with adapter failure."""
        # Mock adapter.get_version to return failure
        with mock.patch.object(self.bridge.adapter, "get_version") as mock_get_version:
            mock_get_version.return_value = FlextResult.fail("Version check failed")

            result = self.bridge.get_version()
            assert result.is_failure
            assert "Version check failed" in (result.error or "")

    def test_get_version_adapter_exception(self) -> None:
        """Test get_version with adapter exception."""
        # Mock adapter.get_version to raise exception
        with mock.patch.object(
            self.bridge.adapter,
            "get_version",
            side_effect=Exception("Test exception"),
        ):
            result = self.bridge.get_version()
            assert result.is_failure
            assert "Test exception" in (result.error or "")

    def test_get_version_json_failure(self) -> None:
        """Test get_version_json with failure."""
        # Mock get_version to return failure
        with mock.patch.object(self.bridge, "get_version") as mock_get_version:
            mock_get_version.return_value = FlextResult.fail("Version check failed")

            result = self.bridge.get_version_json()
            assert "error" in result
            assert "Version check failed" in result

    def test_run_pipeline_adapter_failure(self) -> None:
        """Test run_pipeline with adapter failure."""
        # Mock adapter.create_temporary_meltano_project to return failure
        with mock.patch.object(
            self.bridge.adapter,
            "create_temporary_meltano_project",
        ) as mock_create_project:
            mock_create_project.return_value = FlextResult.fail(
                "Project creation failed",
            )

            result = self.bridge.run_pipeline("tap-csv", "target-csv")
            assert result["success"] is False
            assert "Attempted to access value on failed result" in str(result["error"])

    def test_run_pipeline_adapter_exception(self) -> None:
        """Test run_pipeline with adapter exception."""
        # Mock adapter.create_temporary_meltano_project to raise exception
        with mock.patch.object(
            self.bridge.adapter,
            "create_temporary_meltano_project",
            side_effect=Exception("Test exception"),
        ):
            result = self.bridge.run_pipeline("tap-csv", "target-csv")
            assert result["success"] is False
            assert "Test exception" in str(result["error"])

    def test_execute_meltano_command_adapter_failure(self) -> None:
        """Test execute_meltano_command with adapter failure."""
        # Mock adapter.execute_bridge_service to return failure
        with mock.patch.object(
            self.bridge.adapter,
            "execute_bridge_service",
        ) as mock_execute:
            mock_execute.return_value = FlextResult.fail("Command failed")

            result = self.bridge.execute_meltano_command(["test"])
            assert result["success"] is False
            assert "Attempted to access value on failed result" in str(result["error"])

    def test_execute_meltano_command_adapter_exception(self) -> None:
        """Test execute_meltano_command with adapter exception."""
        # Mock adapter.execute_bridge_service to raise exception
        with mock.patch.object(
            self.bridge.adapter,
            "execute_bridge_service",
            side_effect=Exception("Test exception"),
        ):
            result = self.bridge.execute_meltano_command(["test"])
            assert result["success"] is False
            assert "Test exception" in str(result["error"])

    def test_execute_dbt_command_adapter_failure(self) -> None:
        """Test execute_dbt_command with adapter failure."""
        # Mock adapter.execute_dbt_operation to return failure
        with mock.patch.object(
            self.bridge.adapter,
            "execute_dbt_operation",
        ) as mock_execute:
            mock_execute.return_value = FlextResult.fail("DBT command failed")

            result = self.bridge.execute_dbt_command(["test"])
            assert result["success"] is False
            assert "Attempted to access value on failed result" in str(result["error"])

    def test_execute_dbt_command_adapter_exception(self) -> None:
        """Test execute_dbt_command with adapter exception."""
        # Mock adapter.execute_dbt_operation to raise exception
        with mock.patch.object(
            self.bridge.adapter,
            "execute_dbt_operation",
            side_effect=Exception("Test exception"),
        ):
            result = self.bridge.execute_dbt_command(["test"])
            assert result["success"] is False
            assert "Test exception" in str(result["error"])

    def test_install_plugin_project_not_found(self) -> None:
        """Test install_plugin with project not found."""
        # Mock Path.exists to return False
        with mock.patch.object(Path, "exists", return_value=False):
            result = self.bridge.install_plugin("tap-csv", "csv", ".")
            assert isinstance(result, FlextResult)
            assert result.is_failure
            assert "meltano.yml not found" in (result.error or "")

    def test_install_plugin_adapter_failure(self) -> None:
        """Test install_plugin with adapter failure."""
        # Mock Path.exists to return True and adapter.add_plugin to return failure
        with (
            mock.patch.object(Path, "exists", return_value=True),
            mock.patch.object(self.bridge.adapter, "add_plugin") as mock_add_plugin,
        ):
            mock_add_plugin.return_value = FlextResult.fail(
                "Plugin installation failed",
            )

            result = self.bridge.install_plugin("tap-csv", "csv", ".")
            assert isinstance(result, FlextResult)
            assert result.is_failure
            assert "Plugin installation failed" in (result.error or "")

    def test_install_plugin_exception(self) -> None:
        """Test install_plugin with exception."""
        # Mock Path.exists to raise exception
        with mock.patch.object(Path, "exists", side_effect=Exception("Test exception")):
            result = self.bridge.install_plugin("tap-csv", "csv", ".")
            assert isinstance(result, FlextResult)
            assert result.is_failure
            assert "Test exception" in (result.error or "")

    def test_get_project_info_adapter_failure(self) -> None:
        """Test get_project_info with adapter failure."""
        # Mock adapter.create_project to return failure
        with mock.patch.object(
            self.bridge.adapter,
            "create_project",
        ) as mock_create_project:
            mock_create_project.return_value = FlextResult.fail(
                "Project creation failed",
            )

            result = self.bridge.get_project_info(".")
            assert result["success"] is False
            assert "Project creation failed" in str(result["error"])

    def test_get_project_info_exception(self) -> None:
        """Test get_project_info with exception."""
        # Mock adapter.create_project to raise exception
        with mock.patch.object(
            self.bridge.adapter,
            "create_project",
            side_effect=Exception("Test exception"),
        ):
            result = self.bridge.get_project_info(".")
            assert result["success"] is False
            assert "Test exception" in str(result["error"])

    def test_discover_plugins_adapter_failure(self) -> None:
        """Test discover_plugins with adapter failure."""
        # Mock adapter.discover_plugins to return failure
        with mock.patch.object(
            self.bridge.adapter,
            "discover_plugins",
        ) as mock_discover:
            mock_discover.return_value = FlextResult.fail("Discovery failed")

            result = self.bridge.discover_plugins()
            assert result.is_failure
            assert "Discovery failed" in (result.error or "")

    def test_discover_plugins_exception(self) -> None:
        """Test discover_plugins with exception."""
        # Mock adapter.discover_plugins to raise exception
        with mock.patch.object(
            self.bridge.adapter,
            "discover_plugins",
            side_effect=Exception("Test exception"),
        ):
            result = self.bridge.discover_plugins()
            assert result.is_failure
            assert "Test exception" in (result.error or "")

    def test_run_plugin_async_exception(self) -> None:
        """Test run_plugin_async with exception."""
        # Mock _run_plugin_sync to raise exception
        with mock.patch.object(
            self.bridge,
            "_run_plugin_sync",
            side_effect=Exception("Test exception"),
        ):

            async def test_async() -> None:
                result = await self.bridge.run_plugin_async(
                    None,
                    "test-plugin",
                    "test",
                    [],
                )
                assert isinstance(result, dict)
                assert result["success"] is False
                assert "Test exception" in str(result["error"])

            asyncio.run(test_async())

    def test_run_plugin_sync_adapter_failure(self) -> None:
        """Test _run_plugin_sync with adapter failure."""
        # Mock adapter.execute_bridge_service to return failure
        with mock.patch.object(
            self.bridge.adapter,
            "execute_bridge_service",
        ) as mock_execute:
            mock_execute.return_value = FlextResult.fail("Plugin execution failed")

            result = self.bridge._run_plugin_sync(None, "test-plugin", "test", [])
            assert isinstance(result, dict)
            assert result["success"] is False
            assert "Plugin execution failed" in str(result["error"])

    def test_run_plugin_sync_exception(self) -> None:
        """Test _run_plugin_sync with exception."""
        # Mock adapter.execute_bridge_service to raise exception
        with mock.patch.object(
            self.bridge.adapter,
            "execute_bridge_service",
            side_effect=Exception("Test exception"),
        ):
            result = self.bridge._run_plugin_sync(None, "test-plugin", "test", [])
            assert isinstance(result, dict)
            assert result["success"] is False
            assert "Test exception" in str(result["error"])

    def test_list_plugins_adapter_failure(self) -> None:
        """Test list_plugins with adapter failure."""
        # Mock adapter.discover_plugins to return failure
        with mock.patch.object(
            self.bridge.adapter,
            "discover_plugins",
        ) as mock_discover:
            mock_discover.return_value = FlextResult.fail("Plugin listing failed")

            result = self.bridge.list_plugins()
            assert result.is_failure
            assert "Plugin listing failed" in (result.error or "")

    def test_list_plugins_exception(self) -> None:
        """Test list_plugins with exception."""
        # Mock adapter.discover_plugins to raise exception
        with mock.patch.object(
            self.bridge.adapter,
            "discover_plugins",
            side_effect=Exception("Test exception"),
        ):
            result = self.bridge.list_plugins()
            assert result.is_failure
            assert "Test exception" in (result.error or "")

    def test_initialize_project_adapter_failure(self) -> None:
        """Test initialize_project with adapter failure."""
        # Mock adapter.initialize_project to return failure
        with mock.patch.object(self.bridge.adapter, "initialize_project") as mock_init:
            mock_init.return_value = FlextResult.fail("Project initialization failed")

            result = self.bridge.initialize_project(".")
            assert result.is_failure
            assert "Project initialization failed" in (result.error or "")

    def test_initialize_project_exception(self) -> None:
        """Test initialize_project with exception."""
        # Mock adapter.initialize_project to raise exception
        with mock.patch.object(
            self.bridge.adapter,
            "initialize_project",
            side_effect=Exception("Test exception"),
        ):
            result = self.bridge.initialize_project(".")
            assert result.is_failure
            assert "Test exception" in (result.error or "")
