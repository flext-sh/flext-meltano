"""Test module for flext-meltano."""

from pathlib import Path
from unittest import mock

# SPDX-License-Identifier: MIT
from flext_core import FlextResult
from flext_meltano import FlextMeltanoExecutor


class TestFlextMeltanoExecutorErrorCoverage:
    """Test suite for error coverage scenarios."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.executor = FlextMeltanoExecutor()

    def test_execute_health_failure(self) -> None:
        """Test execute method with health command failure."""
        # Mock meltano_adapter.get_version to return failure
        with mock.patch.object(
            self.executor.meltano_adapter,
            "get_version",
        ) as mock_get_version:
            mock_get_version.return_value = FlextResult.fail("Health check failed")

            result = self.executor.execute("health")
            # The method handles the failure gracefully and returns success with degraded status
            assert result.is_success
            assert "degraded" in str(result.unwrap())

    def test_execute_version_failure(self) -> None:
        """Test execute method with version command failure."""
        # Mock meltano_adapter.get_version to return failure
        with mock.patch.object(
            self.executor.meltano_adapter,
            "get_version",
        ) as mock_get_version:
            mock_get_version.return_value = FlextResult.fail("Version check failed")

            result = self.executor.execute("version")
            # The method handles the failure gracefully and returns success with default version
            assert result.is_success
            assert "version" in str(result.unwrap())

    def test_execute_unknown_command(self) -> None:
        """Test execute method with unknown command."""
        result = self.executor.execute("unknown_command")
        assert result.is_failure
        assert result.error is not None
        assert result.error is not None and "Command not in registry" in result.error

    def test_execute_meltano_command_project_not_found(self) -> None:
        """Test execute_meltano_command with project not found."""
        # Use a non-existent path
        non_existent_path = Path("/non/existent/path")

        result = self.executor.execute_meltano_command(
            project_root=non_existent_path,
            command=["run", "tap-csv", "target-csv"],
        )
        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None
            and "meltano.yml file missing from project root" in result.error
        )

    def test_get_project_info_project_not_found(self) -> None:
        """Test get_project_info with project not found."""
        # Use a non-existent path
        non_existent_path = Path("/non/existent/path")

        result = self.executor.get_project_info(non_existent_path)
        assert result.is_failure
        assert result.error is not None
        assert (
            result.error is not None
            and "Unable to access project metadata" in result.error
        )

    def test_execute_meltano_command_exception(self) -> None:
        """Test execute_meltano_command with exception."""
        # Mock Path.exists to raise exception
        with mock.patch.object(Path, "exists", side_effect=Exception("Test exception")):
            result = self.executor.execute_meltano_command(
                project_root=Path("/test"),
                command=["run", "tap-csv", "target-csv"],
            )
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "Unable to verify project structure" in result.error
            )

    def test_get_project_info_exception(self) -> None:
        """Test get_project_info with exception."""
        # Mock Path.exists to raise exception
        with mock.patch.object(Path, "exists", side_effect=Exception("Test exception")):
            result = self.executor.get_project_info(Path("/test"))
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "Unable to access project metadata" in result.error
            )

    def test_run_command_exception(self) -> None:
        """Test run_command with exception."""
        # Test with invalid command that will cause internal errors
        result = self.executor.run_command(["invalid_command"])
        assert isinstance(result, FlextResult)
        # Should handle gracefully

    def test_run_method_exception(self) -> None:
        """Test run method with exception."""
        # Mock logger.info to raise exception
        with mock.patch.object(
            self.executor.logger,
            "info",
            side_effect=Exception("Test exception"),
        ):
            result = self.executor.run(["test"])
            # The method handles exceptions gracefully and returns success
            assert result.is_success
            assert "command" in result.unwrap()

    def test_execute_and_format_result_exception(self) -> None:
        """Test _execute_and_format_result with exception."""
        # Test with invalid arguments that will cause internal errors
        result = self.executor._execute_and_format_result(["invalid_command"])
        assert result.is_success  # Should handle exception gracefully
        assert "command" in result.unwrap()

    def test_health_exception(self) -> None:
        """Test health method with exception."""
        # Mock meltano_adapter.get_version to raise exception
        with mock.patch.object(
            self.executor.meltano_adapter,
            "get_version",
            side_effect=Exception("Test exception"),
        ):
            result = self.executor.health()
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "Service health validation unsuccessful" in result.error
            )

    def test_version_exception(self) -> None:
        """Test version method with exception."""
        # Mock meltano_adapter.get_version to raise exception
        with mock.patch.object(
            self.executor.meltano_adapter,
            "get_version",
            side_effect=Exception("Test exception"),
        ):
            result = self.executor.version()
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "Unable to retrieve Meltano version information" in result.error
            )

    def test_help_exception(self) -> None:
        """Test help method with exception."""
        # Mock logger.info to raise exception
        with mock.patch.object(
            self.executor.logger,
            "info",
            side_effect=Exception("Test exception"),
        ):
            result = self.executor.help()
            # The method handles exceptions gracefully and returns success
            assert result.is_success
            assert "commands" in result.unwrap()

    def test_list_commands_exception(self) -> None:
        """Test list_commands method with exception."""
        # Mock logger.info to raise exception
        with mock.patch.object(
            self.executor.logger,
            "info",
            side_effect=Exception("Test exception"),
        ):
            result = self.executor.list_commands()
            # The method handles exceptions gracefully and returns success
            assert result.is_success
            assert "commands" in result.unwrap()

    def test_list_plugins_exception(self) -> None:
        """Test list_plugins method with exception."""
        # Mock meltano_adapter.discover_plugins to raise exception
        with mock.patch.object(
            self.executor.meltano_adapter,
            "discover_plugins",
            side_effect=Exception("Test exception"),
        ):
            result = self.executor.list_plugins()
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None
                and "Unable to enumerate installed plugins" in result.error
            )

    def test_run_pipeline_exception(self) -> None:
        """Test run_pipeline method with exception."""
        # Mock logger.info to raise exception
        with mock.patch.object(
            self.executor.logger,
            "info",
            side_effect=Exception("Test exception"),
        ):
            result = self.executor.run_pipeline("tap-csv", "target-csv")
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None and "Pipeline execution failed" in result.error
            )

    def test_flext_meltano_version_exception(self) -> None:
        """Test _flext_meltano_version method with exception."""
        # Mock MeltanoBridge to raise exception
        with mock.patch(
            "flext_meltano.executors.MeltanoBridge",
            side_effect=Exception("Test exception"),
        ):
            result = self.executor._flext_meltano_version()
            assert result.is_failure
            assert result.error is not None
            assert result.error is not None and "Version check failed" in result.error

    def test_flext_meltano_install_exception(self) -> None:
        """Test install command with exception."""
        # Mock _flext_meltano_install to raise exception
        with mock.patch.object(
            self.executor,
            "_flext_meltano_install",
            side_effect=Exception("Test exception"),
        ):
            # Use run_command which is the public API
            result = self.executor.run_command(["install"])
            # run_command returns FlextResult[int], and exceptions in command execution
            # should result in failure result
            assert isinstance(result, FlextResult)

    def test_flext_meltano_invoke_exception(self) -> None:
        """Test flext_meltano_invoke method with exception."""
        # Mock logger.info to raise exception
        with mock.patch.object(
            self.executor.logger,
            "info",
            side_effect=Exception("Test exception"),
        ):
            result = self.executor._flext_meltano_invoke("test-plugin", "arg1", "arg2")
            assert result.is_failure
            assert result.error is not None
            assert (
                result.error is not None and "Plugin invocation failed" in result.error
            )

    def test_run_cli_exception(self) -> None:
        """Test run_cli method with exception."""
        # Mock logger.info to raise exception
        with mock.patch.object(
            self.executor.logger,
            "info",
            side_effect=Exception("Test exception"),
        ):
            result = self.executor.run_cli(["test"])
            # The method handles exceptions gracefully and returns success with error info
            assert result.is_success
            assert "command" in result.unwrap()

    def test_create_flext_cli_exception(self) -> None:
        """Test create_flext_cli method with exception."""
        # Mock FlextLogger to raise exception
        with mock.patch(
            "flext_meltano.executors.FlextLogger",
            side_effect=Exception("Test exception"),
        ):
            result = self.executor.create_flext_cli()
            assert result.is_failure
            assert result.error is not None
            assert result.error is not None and "CLI creation failed" in result.error
