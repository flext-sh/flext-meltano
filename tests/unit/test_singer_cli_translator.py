"""Comprehensive tests for FlextMeltanoSingerCliTranslator module.

Tests the complete Singer SDK CLI command translation layer including:
- Pydantic model to CLI command conversion
- Command validation and error handling
- File path validation
- Command execution (mocked)

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

from flext_meltano.models import FlextMeltanoModels
from flext_meltano.singer_cli_translator import FlextMeltanoSingerCliTranslator


class TestFlextMeltanoSingerCliTranslatorTapRun:
    """Test translate_tap_run method."""

    def test_translate_tap_run_minimal(self) -> None:
        """Test tap run translation with minimal parameters."""
        params = FlextMeltanoModels.TapRunParams(
            tap_name="tap-postgres",
            discover=False,
        )

        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == ["tap-postgres"]

    def test_translate_tap_run_discover_mode(self) -> None:
        """Test tap run translation in discover mode."""
        params = FlextMeltanoModels.TapRunParams(
            tap_name="tap-postgres",
            discover=True,
        )

        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == ["tap-postgres", "--discover"]

    def test_translate_tap_run_with_config(self) -> None:
        """Test tap run translation with config file."""
        params = FlextMeltanoModels.TapRunParams(
            tap_name="tap-postgres",
            config_file="/path/to/config.json",
            discover=False,
        )

        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == ["tap-postgres", "--config", "/path/to/config.json"]

    def test_translate_tap_run_with_catalog(self) -> None:
        """Test tap run translation with catalog file."""
        params = FlextMeltanoModels.TapRunParams(
            tap_name="tap-postgres",
            catalog_file="/path/to/catalog.json",
            discover=False,
        )

        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == ["tap-postgres", "--catalog", "/path/to/catalog.json"]

    def test_translate_tap_run_with_state(self) -> None:
        """Test tap run translation with state file."""
        params = FlextMeltanoModels.TapRunParams(
            tap_name="tap-postgres",
            state_file="/path/to/state.json",
            discover=False,
        )

        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == ["tap-postgres", "--state", "/path/to/state.json"]

    def test_translate_tap_run_with_properties(self) -> None:
        """Test tap run translation with properties file."""
        params = FlextMeltanoModels.TapRunParams(
            tap_name="tap-postgres",
            properties_file="/path/to/properties.json",
            discover=False,
        )

        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == ["tap-postgres", "--properties", "/path/to/properties.json"]

    def test_translate_tap_run_with_all_parameters(self) -> None:
        """Test tap run translation with all parameters."""
        params = FlextMeltanoModels.TapRunParams(
            tap_name="tap-postgres",
            config_file="/path/to/config.json",
            catalog_file="/path/to/catalog.json",
            state_file="/path/to/state.json",
            properties_file="/path/to/properties.json",
            discover=False,
        )

        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == [
            "tap-postgres",
            "--config",
            "/path/to/config.json",
            "--catalog",
            "/path/to/catalog.json",
            "--state",
            "/path/to/state.json",
            "--properties",
            "/path/to/properties.json",
        ]

    def test_translate_tap_run_discover_ignores_other_params(self) -> None:
        """Test that discover mode returns early, ignoring other parameters."""
        params = FlextMeltanoModels.TapRunParams(
            tap_name="tap-postgres",
            config_file="/path/to/config.json",
            catalog_file="/path/to/catalog.json",
            discover=True,
        )

        result = FlextMeltanoSingerCliTranslator.translate_tap_run(params)

        assert result.is_success
        command = result.unwrap()
        # Should only include tap name and --discover flag
        assert command == ["tap-postgres", "--discover"]


class TestFlextMeltanoSingerCliTranslatorTargetRun:
    """Test translate_target_run method."""

    def test_translate_target_run_minimal(self) -> None:
        """Test target run translation with minimal parameters."""
        params = FlextMeltanoModels.TargetRunParams(
            target_name="target-postgres",
        )

        result = FlextMeltanoSingerCliTranslator.translate_target_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == ["target-postgres"]

    def test_translate_target_run_with_config(self) -> None:
        """Test target run translation with config file."""
        params = FlextMeltanoModels.TargetRunParams(
            target_name="target-postgres",
            config_file="/path/to/config.json",
        )

        result = FlextMeltanoSingerCliTranslator.translate_target_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == ["target-postgres", "--config", "/path/to/config.json"]

    def test_translate_target_run_with_input(self) -> None:
        """Test target run translation with input file."""
        params = FlextMeltanoModels.TargetRunParams(
            target_name="target-postgres",
            input_file="/path/to/input.jsonl",
        )

        result = FlextMeltanoSingerCliTranslator.translate_target_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == ["target-postgres", "--input", "/path/to/input.jsonl"]

    def test_translate_target_run_with_all_parameters(self) -> None:
        """Test target run translation with all parameters."""
        params = FlextMeltanoModels.TargetRunParams(
            target_name="target-postgres",
            config_file="/path/to/config.json",
            input_file="/path/to/input.jsonl",
        )

        result = FlextMeltanoSingerCliTranslator.translate_target_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == [
            "target-postgres",
            "--config",
            "/path/to/config.json",
            "--input",
            "/path/to/input.jsonl",
        ]


class TestFlextMeltanoSingerCliTranslatorPipelineRun:
    """Test translate_pipeline_run method."""

    def test_translate_pipeline_run_minimal(self) -> None:
        """Test pipeline run translation with minimal parameters."""
        params = FlextMeltanoModels.PipelineRunParams(
            tap_name="tap-postgres",
            target_name="target-postgres",
        )

        result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(params)

        assert result.is_success
        tap_command, target_command = result.unwrap()
        assert tap_command == ["tap-postgres"]
        assert target_command == ["target-postgres"]

    def test_translate_pipeline_run_with_tap_config(self) -> None:
        """Test pipeline run translation with tap config."""
        params = FlextMeltanoModels.PipelineRunParams(
            tap_name="tap-postgres",
            target_name="target-postgres",
            tap_config="/path/to/tap-config.json",
        )

        result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(params)

        assert result.is_success
        tap_command, target_command = result.unwrap()
        assert tap_command == ["tap-postgres", "--config", "/path/to/tap-config.json"]
        assert target_command == ["target-postgres"]

    def test_translate_pipeline_run_with_target_config(self) -> None:
        """Test pipeline run translation with target config."""
        params = FlextMeltanoModels.PipelineRunParams(
            tap_name="tap-postgres",
            target_name="target-postgres",
            target_config="/path/to/target-config.json",
        )

        result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(params)

        assert result.is_success
        tap_command, target_command = result.unwrap()
        assert tap_command == ["tap-postgres"]
        assert target_command == [
            "target-postgres",
            "--config",
            "/path/to/target-config.json",
        ]

    def test_translate_pipeline_run_with_catalog(self) -> None:
        """Test pipeline run translation with catalog file."""
        params = FlextMeltanoModels.PipelineRunParams(
            tap_name="tap-postgres",
            target_name="target-postgres",
            catalog_file="/path/to/catalog.json",
        )

        result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(params)

        assert result.is_success
        tap_command, target_command = result.unwrap()
        assert tap_command == ["tap-postgres", "--catalog", "/path/to/catalog.json"]
        assert target_command == ["target-postgres"]

    def test_translate_pipeline_run_with_state(self) -> None:
        """Test pipeline run translation with state file."""
        params = FlextMeltanoModels.PipelineRunParams(
            tap_name="tap-postgres",
            target_name="target-postgres",
            state_file="/path/to/state.json",
        )

        result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(params)

        assert result.is_success
        tap_command, target_command = result.unwrap()
        assert tap_command == ["tap-postgres", "--state", "/path/to/state.json"]
        assert target_command == ["target-postgres"]

    def test_translate_pipeline_run_with_all_parameters(self) -> None:
        """Test pipeline run translation with all parameters."""
        params = FlextMeltanoModels.PipelineRunParams(
            tap_name="tap-postgres",
            target_name="target-postgres",
            tap_config="/path/to/tap-config.json",
            target_config="/path/to/target-config.json",
            catalog_file="/path/to/catalog.json",
            state_file="/path/to/state.json",
        )

        result = FlextMeltanoSingerCliTranslator.translate_pipeline_run(params)

        assert result.is_success
        tap_command, target_command = result.unwrap()
        assert tap_command == [
            "tap-postgres",
            "--config",
            "/path/to/tap-config.json",
            "--catalog",
            "/path/to/catalog.json",
            "--state",
            "/path/to/state.json",
        ]
        assert target_command == [
            "target-postgres",
            "--config",
            "/path/to/target-config.json",
        ]


class TestFlextMeltanoSingerCliTranslatorDbtRun:
    """Test translate_dbt_run method."""

    def test_translate_dbt_run_minimal(self) -> None:
        """Test DBT run translation with minimal parameters."""
        params = FlextMeltanoModels.DbtRunParams(
            project_dir="/path/to/dbt/project",
        )

        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == ["dbt", "run", "--project-dir", "/path/to/dbt/project"]

    def test_translate_dbt_run_with_models(self) -> None:
        """Test DBT run translation with models parameter."""
        params = FlextMeltanoModels.DbtRunParams(
            project_dir="/path/to/dbt/project",
            models="users orders",
        )

        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == [
            "dbt",
            "run",
            "--project-dir",
            "/path/to/dbt/project",
            "--models",
            "users orders",
        ]

    def test_translate_dbt_run_with_select(self) -> None:
        """Test DBT run translation with select parameter."""
        params = FlextMeltanoModels.DbtRunParams(
            project_dir="/path/to/dbt/project",
            select="tag:daily",
        )

        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == [
            "dbt",
            "run",
            "--project-dir",
            "/path/to/dbt/project",
            "--select",
            "tag:daily",
        ]

    def test_translate_dbt_run_with_exclude(self) -> None:
        """Test DBT run translation with exclude parameter."""
        params = FlextMeltanoModels.DbtRunParams(
            project_dir="/path/to/dbt/project",
            exclude="tag:deprecated",
        )

        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == [
            "dbt",
            "run",
            "--project-dir",
            "/path/to/dbt/project",
            "--exclude",
            "tag:deprecated",
        ]

    def test_translate_dbt_run_with_full_refresh(self) -> None:
        """Test DBT run translation with full refresh flag."""
        params = FlextMeltanoModels.DbtRunParams(
            project_dir="/path/to/dbt/project",
            full_refresh=True,
        )

        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == [
            "dbt",
            "run",
            "--project-dir",
            "/path/to/dbt/project",
            "--full-refresh",
        ]

    def test_translate_dbt_run_with_vars(self) -> None:
        """Test DBT run translation with vars parameter."""
        params = FlextMeltanoModels.DbtRunParams(
            project_dir="/path/to/dbt/project",
            vars='{"key": "value"}',
        )

        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == [
            "dbt",
            "run",
            "--project-dir",
            "/path/to/dbt/project",
            "--vars",
            '{"key": "value"}',
        ]

    def test_translate_dbt_run_with_all_parameters(self) -> None:
        """Test DBT run translation with all parameters."""
        params = FlextMeltanoModels.DbtRunParams(
            project_dir="/path/to/dbt/project",
            models="users orders",
            select="tag:daily",
            exclude="tag:deprecated",
            full_refresh=True,
            vars='{"environment": "production"}',
        )

        result = FlextMeltanoSingerCliTranslator.translate_dbt_run(params)

        assert result.is_success
        command = result.unwrap()
        assert command == [
            "dbt",
            "run",
            "--project-dir",
            "/path/to/dbt/project",
            "--models",
            "users orders",
            "--select",
            "tag:daily",
            "--exclude",
            "tag:deprecated",
            "--full-refresh",
            "--vars",
            '{"environment": "production"}',
        ]


class TestFlextMeltanoSingerCliTranslatorExecuteCommand:
    """Test execute_singer_command method."""

    @patch("flext_core.utilities.FlextCore.Utilities.run_external_command")
    def test_execute_singer_command_success(self, mock_run: MagicMock) -> None:
        """Test successful command execution."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Success output",
            stderr="",
        )

        result = FlextMeltanoSingerCliTranslator.execute_singer_command([
            "tap-postgres",
            "--config",
            "config.json",
        ])

        assert result.is_success
        output = result.unwrap()
        assert output["stdout"] == "Success output"
        assert not output["stderr"]
        assert output["returncode"] == 0
        assert output["command"] == "tap-postgres --config config.json"

        mock_run.assert_called_once()

    @patch("flext_core.utilities.FlextCore.Utilities.run_external_command")
    def test_execute_singer_command_with_input(self, mock_run: MagicMock) -> None:
        """Test command execution with input data."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="Success",
            stderr="",
        )

        input_data = '{"type": "RECORD", "stream": "users"}'
        result = FlextMeltanoSingerCliTranslator.execute_singer_command(
            ["target-postgres"], input_data=input_data
        )

        assert result.is_success

        # Verify FlextCore.Utilities.run_external_command was called with encoded input
        call_args = mock_run.call_args
        assert call_args.kwargs["input"] == input_data.encode()

    @patch("flext_core.utilities.FlextCore.Utilities.run_external_command")
    def test_execute_singer_command_failure(self, mock_run: MagicMock) -> None:
        """Test command execution failure."""
        mock_run.return_value = MagicMock(
            returncode=1,
            stdout="",
            stderr="Error: Connection failed",
        )

        result = FlextMeltanoSingerCliTranslator.execute_singer_command([
            "tap-postgres"
        ])

        assert result.is_failure
        assert "Command failed with code 1" in result.error
        assert "Connection failed" in result.error

    @patch("flext_core.utilities.FlextCore.Utilities.run_external_command")
    def test_execute_singer_command_timeout(self, mock_run: MagicMock) -> None:
        """Test command execution timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("tap-postgres", 10)

        result = FlextMeltanoSingerCliTranslator.execute_singer_command(
            ["tap-postgres"], timeout=10
        )

        assert result.is_failure
        assert "Command timed out after 10 seconds" in result.error

    @patch("flext_core.utilities.FlextCore.Utilities.run_external_command")
    def test_execute_singer_command_not_found(self, mock_run: MagicMock) -> None:
        """Test command not found error."""
        mock_run.side_effect = FileNotFoundError("tap-nonexistent not found")

        result = FlextMeltanoSingerCliTranslator.execute_singer_command([
            "tap-nonexistent"
        ])

        assert result.is_failure
        assert "Command not found: tap-nonexistent" in result.error

    @patch("flext_core.utilities.FlextCore.Utilities.run_external_command")
    def test_execute_singer_command_generic_exception(
        self, mock_run: MagicMock
    ) -> None:
        """Test generic exception handling."""
        mock_run.side_effect = RuntimeError("Unexpected error")

        result = FlextMeltanoSingerCliTranslator.execute_singer_command([
            "tap-postgres"
        ])

        assert result.is_failure
        assert "Unexpected error running command" in result.error


class TestFlextMeltanoSingerCliTranslatorFileValidation:
    """Test validate_file_path method."""

    def test_validate_file_path_none(self) -> None:
        """Test file path validation with None input."""
        result = FlextMeltanoSingerCliTranslator.validate_file_path(None)

        assert result.is_success
        assert result.unwrap() is None

    def test_validate_file_path_empty_string(self) -> None:
        """Test file path validation with empty string."""
        result = FlextMeltanoSingerCliTranslator.validate_file_path("")

        assert result.is_success
        assert result.unwrap() is None

    def test_validate_file_path_valid(self, tmp_path: Path) -> None:
        """Test file path validation with valid file."""
        test_file = tmp_path / "config.json"
        test_file.write_text('{"key": "value"}')

        result = FlextMeltanoSingerCliTranslator.validate_file_path(str(test_file))

        assert result.is_success
        validated_path = result.unwrap()
        assert validated_path == test_file
        assert validated_path.exists()

    def test_validate_file_path_not_found(self) -> None:
        """Test file path validation with non-existent file."""
        result = FlextMeltanoSingerCliTranslator.validate_file_path(
            "/path/to/nonexistent.json"
        )

        assert result.is_failure
        assert "File not found" in result.error

    def test_validate_file_path_directory(self, tmp_path: Path) -> None:
        """Test file path validation with directory instead of file."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        result = FlextMeltanoSingerCliTranslator.validate_file_path(str(test_dir))

        assert result.is_failure
        assert "Not a file" in result.error
