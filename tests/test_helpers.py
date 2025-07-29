"""Tests for simple_helpers module."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import flext_meltano


class TestExecuteJob:
    """Test flext_meltano_execute_job function."""

    @patch("flext_meltano.simple_helpers.subprocess.run")
    def test_execute_job_success(self, mock_run: MagicMock) -> None:
        """Test successful job execution."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Job completed successfully",
            stderr="",
        )

        result = flext_meltano.flext_meltano_execute_job("tap-csv", "target-jsonl")

        assert result.success is True
        assert result.data is not None
        assert result.data["job_completed"] is True
        assert result.data["tap"] == "tap-csv"
        assert result.data["target"] == "target-jsonl"
        assert "Job completed successfully" in result.data["stdout"]

    @patch("flext_meltano.simple_helpers.subprocess.run")
    def test_execute_job_failure(self, mock_run: MagicMock) -> None:
        """Test failed job execution."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Tap not found",
        )

        result = flext_meltano.flext_meltano_execute_job("tap-invalid", "target-jsonl")

        assert result.success is False
        assert result.error is not None
        assert "Job failed: Tap not found" in result.error

    @patch("flext_meltano.simple_helpers.subprocess.run")
    def test_execute_job_exception(self, mock_run: MagicMock) -> None:
        """Test job execution with exception."""
        mock_run.side_effect = FileNotFoundError("meltano command not found")

        result = flext_meltano.flext_meltano_execute_job("tap-csv", "target-jsonl")

        assert result.success is False
        assert result.error is not None
        assert "Execution failed" in result.error


class TestRunCommand:
    """Test flext_meltano_run_command function."""

    @patch("flext_meltano.simple_helpers.subprocess.run")
    def test_run_command_success(self, mock_run: MagicMock) -> None:
        """Test successful command execution."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="meltano version 3.0.0",
            stderr="",
        )

        result = flext_meltano.flext_meltano_run_command(["--version"])

        assert result.success is True
        assert result.data is not None
        assert result.data["command_completed"] is True
        assert result.data["returncode"] == 0
        assert "meltano version 3.0.0" in result.data["stdout"]
        assert result.data["args"] == ["--version"]

    @patch("flext_meltano.simple_helpers.subprocess.run")
    def test_run_command_with_error(self, mock_run: MagicMock) -> None:
        """Test command with non-zero exit code."""
        mock_run.return_value = MagicMock(
            returncode=2,
            stdout="",
            stderr="Invalid command",
        )

        result = flext_meltano.flext_meltano_run_command(["invalid", "command"])

        assert result.success is True  # We still return success for subprocess completion
        assert result.data is not None
        assert result.data["returncode"] == 2
        assert "Invalid command" in result.data["stderr"]

    @patch("flext_meltano.simple_helpers.subprocess.run")
    def test_run_command_exception(self, mock_run: MagicMock) -> None:
        """Test command execution with exception."""
        mock_run.side_effect = OSError("Command execution failed")

        result = flext_meltano.flext_meltano_run_command(["--version"])

        assert result.success is False
        assert result.error is not None
        assert "Command failed" in result.error


class TestValidateProject:
    """Test flext_meltano_validate_project function."""

    @patch("flext_meltano.simple_helpers.Path")
    def test_validate_project_success(self, mock_path_class: MagicMock) -> None:
        """Test successful project validation."""
        mock_path = MagicMock()
        mock_path_class.return_value = mock_path

        mock_meltano_yml = MagicMock()
        mock_meltano_yml.exists.return_value = True
        mock_path.__truediv__.return_value = mock_meltano_yml

        result = flext_meltano.flext_meltano_validate_project("/fake/path")

        assert result.success is True
        assert result.data is True

    @patch("flext_meltano.simple_helpers.Path")
    def test_validate_project_missing_yml(self, mock_path_class: MagicMock) -> None:
        """Test project validation with missing meltano.yml."""
        mock_path = MagicMock()
        mock_path_class.return_value = mock_path

        mock_meltano_yml = MagicMock()
        mock_meltano_yml.exists.return_value = False
        mock_path.__truediv__.return_value = mock_meltano_yml

        result = flext_meltano.flext_meltano_validate_project("/fake/path")

        assert result.success is False
        assert result.error is not None
        assert "meltano.yml not found" in result.error

    @patch("flext_meltano.simple_helpers.Path")
    def test_validate_project_exception(self, mock_path_class: MagicMock) -> None:
        """Test project validation with exception."""
        mock_path_class.side_effect = PermissionError("Access denied")

        result = flext_meltano.flext_meltano_validate_project("/restricted/path")

        assert result.success is False
        assert result.error is not None
        assert "Validation failed" in result.error
