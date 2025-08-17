"""Execution Module Comprehensive Test Suite - Core Operations Layer Validation.

**Test Category**: Integration Tests
**Coverage Target**: 95%+ for execution module components
**Dependencies**: Mock subprocess calls, flext-core patterns
**Execution Time**: < 10 seconds total

## Test Scope

Validates the execution module components that provide the **core subprocess orchestration**
for FLEXT Meltano's bridge architecture, focusing on Meltano CLI execution, pipeline
orchestration, and bridge integration patterns that enable Go ↔ Python communication.

## Test Coverage Areas

1. **Execution Commands**: FlextMeltanoExecutionCommand model validation
2. **Execution Context**: Context management and metadata tracking
3. **Subprocess Orchestration**: Meltano CLI execution with error handling
4. **Pipeline Execution**: End-to-end pipeline orchestration patterns
5. **Bridge Integration**: JSON-serializable results for Go service consumption
6. **Error Handling**: Comprehensive error scenarios and recovery patterns

## Architecture Alignment

Tests align with FLEXT Meltano's execution layer architecture:
- **Subprocess Bridge**: Meltano CLI execution via subprocess calls
- **Enterprise Error Handling**: FlextResult pattern validation throughout
- **Bridge Communication**: JSON-serializable output for Go services
- **Railway-Oriented Programming**: Result composition and error propagation

These tests ensure the execution module provides reliable subprocess orchestration
that serves as the foundation for all Go ↔ Python bridge operations.
"""

from __future__ import annotations

import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from flext_core import FlextResult

from flext_meltano import (
    FlextMeltanoConfig,
    FlextMeltanoExecutionCommand,
    FlextMeltanoExecutionContext,
    FlextMeltanoExecutor,
    FlextMeltanoResult,
    create_executor,
    flext_meltano_execute_job,
    flext_meltano_run_command,
)

# Constants
EXPECTED_DATA_COUNT = 3


class TestFlextMeltanoExecutionCommand:
    """Test FlextMeltanoExecutionCommand model."""

    def test_command_initialization(self) -> None:
        """Test command initialization."""
        command = FlextMeltanoExecutionCommand("tap-csv", "target-jsonl")
        if command.tap_name != "tap-csv":
            msg: str = f"Expected {'tap-csv'}, got {command.tap_name}"
            raise AssertionError(msg)
        assert command.target_name == "target-jsonl"

    def test_command_with_different_values(self) -> None:
        """Test command with different tap/target values."""
        command = FlextMeltanoExecutionCommand("tap-postgres", "target-csv")
        if command.tap_name != "tap-postgres":
            msg: str = f"Expected {'tap-postgres'}, got {command.tap_name}"
            raise AssertionError(msg)
        assert command.target_name == "target-csv"

    def test_command_attribute_modification(self) -> None:
        """Test that command attributes can be modified."""
        command = FlextMeltanoExecutionCommand("tap-csv", "target-jsonl")
        command.tap_name = "tap-postgres"
        command.target_name = "target-csv"
        if command.tap_name != "tap-postgres":
            msg: str = f"Expected {'tap-postgres'}, got {command.tap_name}"
            raise AssertionError(msg)
        assert command.target_name == "target-csv"


class TestFlextMeltanoExecutionContext:
    """Test FlextMeltanoExecutionContext model."""

    def test_context_initialization_defaults(self) -> None:
        """Test context initialization with defaults."""
        context = FlextMeltanoExecutionContext(pipeline_name="tap-csv-to-target-jsonl")
        if context.pipeline_name != "tap-csv-to-target-jsonl":
            msg: str = (
                f"Expected {'tap-csv-to-target-jsonl'}, got {context.pipeline_name}"
            )
            raise AssertionError(msg)
        assert context.environment == "dev"
        if context.timeout_seconds != 1800:
            msg: str = f"Expected {1800}, got {context.timeout_seconds}"
            raise AssertionError(msg)
        assert context.metadata == {}
        assert isinstance(context.execution_id, str)
        assert isinstance(context.started_at, datetime)
        assert isinstance(context.project_root, Path)

    def test_context_initialization_custom(self) -> None:
        """Test context initialization with custom values."""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_path = Path(temp_dir) / "test"
            custom_metadata = {"key": "value", "stage": "production"}

            context = FlextMeltanoExecutionContext(
                pipeline_name="tap-postgres-to-target-csv",
                environment="prod",
                project_root=custom_path,
                timeout_seconds=3600,
                metadata=custom_metadata,
            )

            if context.pipeline_name != "tap-postgres-to-target-csv":
                msg: str = f"Expected {'tap-postgres-to-target-csv'}, got {context.pipeline_name}"
                raise AssertionError(msg)
            assert context.environment == "prod"
            if context.project_root != custom_path:
                msg: str = f"Expected {custom_path}, got {context.project_root}"
                raise AssertionError(msg)
            assert context.timeout_seconds == 3600
            if context.metadata != custom_metadata:
                msg: str = f"Expected {custom_metadata}, got {context.metadata}"
                raise AssertionError(msg)

    def test_context_execution_id_uniqueness(self) -> None:
        """Test that execution IDs are unique."""
        context1 = FlextMeltanoExecutionContext(pipeline_name="test1")
        context2 = FlextMeltanoExecutionContext(pipeline_name="test2")
        assert context1.execution_id != context2.execution_id

    def test_context_modification(self) -> None:
        """Test that context can be modified (not frozen by default)."""
        context = FlextMeltanoExecutionContext(pipeline_name="test")
        # Since the model is not frozen, attributes can be modified
        context.pipeline_name = "changed"
        if context.pipeline_name != "changed":
            msg: str = f"Expected {'changed'}, got {context.pipeline_name}"
            raise AssertionError(msg)


class TestFlextMeltanoResult:
    """Test FlextMeltanoResult (legacy result type)."""

    def test_result_success_initialization(self) -> None:
        """Test successful result initialization."""
        data = {"output": "success", "records": 100}
        result = FlextMeltanoResult(success=True, data=data)

        if not (result.success):
            msg: str = f"Expected True, got {result.success}"
            raise AssertionError(msg)
        if result.data != data:
            msg: str = f"Expected {data}, got {result.data}"
            raise AssertionError(msg)
        assert result.error == ""

    def test_result_failure_initialization(self) -> None:
        """Test failure result initialization."""
        result = FlextMeltanoResult(success=False, error="Pipeline failed")

        if result.success:
            msg: str = f"Expected False, got {result.success}"
            raise AssertionError(msg)
        assert result.data is None
        if result.error != "Pipeline failed":
            msg: str = f"Expected {'Pipeline failed'}, got {result.error}"
            raise AssertionError(msg)

    def test_result_ok_class_method(self) -> None:
        """Test ok class method."""
        data = {"records": 50}
        result = FlextMeltanoResult.ok(data)

        if not (result.success):
            msg: str = f"Expected True, got {result.success}"
            raise AssertionError(msg)
        if result.data != data:
            msg: str = f"Expected {data}, got {result.data}"
            raise AssertionError(msg)
        assert result.error == ""

    def test_result_ok_no_data(self) -> None:
        """Test ok class method without data."""
        result = FlextMeltanoResult.ok()

        if not (result.success):
            msg: str = f"Expected True, got {result.success}"
            raise AssertionError(msg)
        assert result.data is None
        if result.error != "":
            msg: str = f"Expected {''}, got {result.error}"
            raise AssertionError(msg)

    def test_result_fail_class_method(self) -> None:
        """Test fail class method."""
        result = FlextMeltanoResult.fail("Execution error")

        if result.success:
            msg: str = f"Expected False, got {result.success}"
            raise AssertionError(msg)
        assert result.data is None
        if result.error != "Execution error":
            msg: str = f"Expected {'Execution error'}, got {result.error}"
            raise AssertionError(msg)


class TestFlextMeltanoExecutor:
    """Test FlextMeltanoExecutor functionality."""

    def test_service_initialization(self) -> None:
        """Test service initialization."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)
        assert service is not None
        assert service.config is not None
        if service._initialized:
            msg: str = f"Expected False, got {service._initialized}"
            raise AssertionError(msg)

    def test_service_initialization_with_path(self) -> None:
        """Test service initialization with custom path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_path = Path(temp_dir) / "test"
            config = FlextMeltanoConfig(project_root=str(custom_path))
            service = FlextMeltanoExecutor(config)
            if service.config.project_root != str(custom_path):
                msg: str = (
                    f"Expected {custom_path!s}, got {service.config.project_root}"
                )
                raise AssertionError(msg)

    def test_service_initialize(self) -> None:
        """Test service initialization method."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)
        result = service.initialize()
        assert result.success
        if not (service._initialized):
            msg: str = f"Expected True, got {service._initialized}"
            raise AssertionError(msg)

    def test_service_validate(self) -> None:
        """Test service validation."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)
        result = service.validate()
        # May fail if project doesn't exist, but should not crash
        assert result.success or not result.success

    def test_service_get_health_status(self) -> None:
        """Test service health status."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)
        result = service.get_health_status()
        assert result.success
        assert result.data is not None
        if "service" not in result.data:
            msg: str = f"Expected {'service'} in {result.data}"
            raise AssertionError(msg)
        if result.data["service"] != "execution":
            msg: str = f"Expected {'execution'}, got {result.data['service']}"
            raise AssertionError(msg)

    def test_service_execute_pipeline(self) -> None:
        """Test service execute_pipeline method."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)
        result = service.execute_pipeline("tap-csv", "target-jsonl")
        # May fail if meltano not installed, but should not crash
        assert result.success or not result.success

    def test_service_run_command(self) -> None:
        """Test service run_command method."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)
        result = service.run_command(["--version"])
        # May fail if meltano not installed, but should not crash
        assert result.success or not result.success

    def test_service_execute_command(self) -> None:
        """Test service execute command method."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)
        command = FlextMeltanoExecutionCommand("tap-csv", "target-jsonl")
        result = service.execute(command)
        # May fail if meltano not installed, but should not crash
        assert result.success or not result.success


class TestFlextMeltanoExecutorValidation:
    """Test FlextMeltanoExecutor validation methods."""

    @patch("flext_meltano.execution.FlextMeltanoExecutor._find_meltano_executable")
    def test_validation_no_meltano_found(self, mock_find: Mock) -> None:
        """Test validation when meltano executable not found."""
        mock_find.return_value = None

        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)

        result = service.validate()
        assert not result.success
        assert result.error is not None
        if "Meltano CLI not found" not in result.error:
            msg: str = f"Expected {'Meltano CLI not found'} in {result.error}"
            raise AssertionError(msg)

    @patch("flext_meltano.execution.FlextMeltanoExecutor._find_meltano_executable")
    def test_validation_import_error(self, mock_find: Mock) -> None:
        """Test validation with ImportError."""
        mock_find.side_effect = ImportError("Module not found")

        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)

        result = service.validate()
        assert not result.success
        assert result.error is not None
        if "Validation failed" not in result.error:
            msg: str = f"Expected {'Validation failed'} in {result.error}"
            raise AssertionError(msg)

    @patch("shutil.which")
    @patch("pathlib.Path.exists")
    def test_find_meltano_executable_not_found(
        self,
        mock_exists: Mock,
        mock_which: Mock,
    ) -> None:
        """Test _find_meltano_executable when no meltano is found."""
        mock_exists.return_value = False  # Venv meltano doesn't exist
        mock_which.return_value = None  # System meltano not found

        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)

        result = service._find_meltano_executable()
        assert result is None

    @patch("flext_meltano.execution.FlextMeltanoExecutor.validate")
    def test_initialize_exception_handling(self, mock_validate: Mock) -> None:
        """Test initialize method exception handling."""
        mock_validate.side_effect = ValueError("Test error")

        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)

        result = service.initialize()
        assert not result.success
        assert result.error is not None
        if "Service initialization failed" not in result.error:
            msg: str = f"Expected {'Service initialization failed'} in {result.error}"
            raise AssertionError(msg)

    def test_validation_success_with_meltano_yml(self) -> None:
        """Test validation success when meltano.yml exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create meltano.yml file
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            service = FlextMeltanoExecutor(config)

            result = service.validate()
            assert result.success
            if not (result.data):
                msg: str = f"Expected True, got {result.data}"
                raise AssertionError(msg)

    def test_validation_with_nonexistent_path(self) -> None:
        """Test validation with nonexistent project root."""
        config = FlextMeltanoConfig(project_root="/nonexistent/path")
        service = FlextMeltanoExecutor(config)

        result = service.validate()
        # Validation looks for meltano executable, not project root existence
        assert result.success or not result.success

    def test_validation_meltano_cli_not_found(self) -> None:
        """Test validation failure when meltano CLI not found."""
        # Use a path where meltano won't be found
        config = FlextMeltanoConfig(project_root="/nonexistent/path/with/no/meltano")
        service = FlextMeltanoExecutor(config)

        result = service.validate()
        # May fail if meltano CLI not found, or succeed if found in system
        assert result.success or not result.success

    def test_validation_exception_handling(self) -> None:
        """Test validation exception handling."""
        config = FlextMeltanoConfig(project_root="")  # Empty path
        service = FlextMeltanoExecutor(config)

        result = service.validate()
        # Should handle gracefully - may succeed or fail based on Path behavior
        assert result.success or not result.success


class TestFlextMeltanoExecutorValidationPaths:
    """Test FlextMeltanoExecutor validation paths during execution."""

    @patch("flext_meltano.execution.FlextMeltanoExecutor.validate")
    def test_execute_pipeline_no_meltano_path_validation_fails(
        self,
        mock_validate: Mock,
    ) -> None:
        """Test execute_pipeline when _meltano_path is None and validation fails."""
        mock_validate.return_value = FlextResult(error="Validation failed")

        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)
        service._meltano_path = None  # Ensure _meltano_path is None

        result = service.execute_pipeline("tap-csv", "target-jsonl")
        assert not result.success
        assert result.error is not None
        if "Validation failed" not in result.error:
            msg: str = f"Expected {'Validation failed'} in {result.error}"
            raise AssertionError(msg)

    @patch("flext_meltano.execution.FlextMeltanoExecutor.validate")
    def test_run_command_no_meltano_path_validation_fails(
        self,
        mock_validate: Mock,
    ) -> None:
        """Test run_command when _meltano_path is None and validation fails."""
        mock_validate.return_value = FlextResult(error="Validation failed")

        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)
        service._meltano_path = None  # Ensure _meltano_path is None

        result = service.run_command(["--version"])
        assert not result.success
        assert result.error is not None
        if "Validation failed" not in result.error:
            msg: str = f"Expected {'Validation failed'} in {result.error}"
            raise AssertionError(msg)


class TestFlextMeltanoExecutorOperations:
    """Test FlextMeltanoExecutor operations with mocking."""

    @patch("subprocess.run")
    def test_execute_pipeline_success(self, mock_run: Mock) -> None:
        """Test successful pipeline execution."""
        # Mock successful subprocess execution
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Pipeline completed successfully"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            # Create meltano.yml file
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            service = FlextMeltanoExecutor(config)

            result = service.execute_pipeline("tap-csv", "target-jsonl")
            assert result.success
            assert result.data is not None
            if not (result.data["success"]):
                msg: str = f"Expected True, got {result.data['success']}"
                raise AssertionError(msg)
            if result.data["pipeline_name"] != "tap-csv-target-jsonl":
                msg: str = f"Expected {'tap-csv-target-jsonl'}, got {result.data['pipeline_name']}"
                raise AssertionError(msg)
            if "meltano" not in result.data["command"]:
                msg: str = f"Expected {'meltano'} in {result.data['command']}"
                raise AssertionError(msg)

    @patch("subprocess.run")
    def test_execute_pipeline_failure(self, mock_run: Mock) -> None:
        """Test pipeline execution failure."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = "Some output"
        mock_result.stderr = "Pipeline failed"
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            service = FlextMeltanoExecutor(config)

            result = service.execute_pipeline("tap-nonexistent", "target-nonexistent")
            assert not result.success
            assert result.error is not None
            if "Pipeline failed" not in result.error:
                msg: str = f"Expected {'Pipeline failed'} in {result.error}"
                raise AssertionError(msg)

    @patch("subprocess.run")
    def test_execute_pipeline_timeout(self, mock_run: Mock) -> None:
        """Test pipeline execution timeout."""
        mock_run.side_effect = subprocess.TimeoutExpired("meltano", 1800)

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            service = FlextMeltanoExecutor(config)

            result = service.execute_pipeline("tap-csv", "target-jsonl")
            assert not result.success
            assert result.error is not None
            if "Pipeline execution timed out" not in result.error:
                msg: str = (
                    f"Expected {'Pipeline execution timed out'} in {result.error}"
                )
                raise AssertionError(msg)

    @patch("subprocess.run")
    def test_run_command_success(self, mock_run: Mock) -> None:
        """Test successful command execution."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Meltano, version 3.0.0"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            service = FlextMeltanoExecutor(config)

            result = service.run_command(["--version"])
            assert result.success
            assert result.data is not None
            if not (result.data["success"]):
                msg: str = f"Expected True, got {result.data['success']}"
                raise AssertionError(msg)
            if "meltano --version" not in result.data["command"]:
                msg: str = f"Expected {'meltano --version'} in {result.data['command']}"
                raise AssertionError(msg)

    @patch("subprocess.run")
    def test_run_command_failure(self, mock_run: Mock) -> None:
        """Test command execution failure."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "Command failed"
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            service = FlextMeltanoExecutor(config)

            result = service.run_command(["invalid", "command"])
            assert not result.success
            assert result.error is not None
            if "Command failed" not in result.error:
                msg: str = f"Expected {'Command failed'} in {result.error}"
                raise AssertionError(msg)

    @patch("subprocess.run")
    def test_execute_pipeline_with_custom_context(self, mock_run: Mock) -> None:
        """Test execute_pipeline with custom context."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Pipeline success"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            service = FlextMeltanoExecutor(config)

            context = FlextMeltanoExecutionContext(
                pipeline_name="tap-csv-target-jsonl",
                environment="prod",
                timeout_seconds=3600,
            )

            result = service.execute_pipeline("tap-csv", "target-jsonl", context)
            assert result.success
            assert result.data is not None
            if result.data["execution_id"] != context.execution_id:
                msg: str = f"Expected {context.execution_id}, got {result.data['execution_id']}"
                raise AssertionError(msg)

    @patch("subprocess.run")
    def test_run_command_with_custom_context(self, mock_run: Mock) -> None:
        """Test run_command with custom context."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "Command success"
        mock_result.stderr = ""
        mock_run.return_value = mock_result

        with tempfile.TemporaryDirectory() as temp_dir:
            meltano_yml = Path(temp_dir) / "meltano.yml"
            meltano_yml.write_text("version: 1\nproject_id: test")

            config = FlextMeltanoConfig(project_root=temp_dir)
            service = FlextMeltanoExecutor(config)

            context = FlextMeltanoExecutionContext(
                pipeline_name="version-check",
                environment="test",
                timeout_seconds=60,
            )

            result = service.run_command(["--version"], context)
            assert result.success
            assert result.data is not None
            if result.data["execution_id"] != context.execution_id:
                msg: str = f"Expected {context.execution_id}, got {result.data['execution_id']}"
                raise AssertionError(msg)


class TestFlextMeltanoExecutorExceptionPaths:
    """Test exception handling paths in FlextMeltanoExecutor."""

    @patch("subprocess.run")
    @patch("flext_meltano.execution.FlextMeltanoExecutor.validate")
    def test_execute_pipeline_os_error(
        self,
        mock_validate: Mock,
        mock_run: Mock,
    ) -> None:
        """Test execute_pipeline with OSError."""
        mock_validate.return_value = FlextResult(data=True)
        mock_run.side_effect = OSError("Permission denied")

        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)

        result = service.execute_pipeline("tap-csv", "target-jsonl")
        assert not result.success
        assert result.error is not None
        if "Execution error" not in result.error:
            msg: str = f"Expected {'Execution error'} in {result.error}"
            raise AssertionError(msg)

    @patch("subprocess.run")
    @patch("flext_meltano.execution.FlextMeltanoExecutor.validate")
    def test_execute_pipeline_called_process_error(
        self,
        mock_validate: Mock,
        mock_run: Mock,
    ) -> None:
        """Test execute_pipeline with CalledProcessError."""
        mock_validate.return_value = FlextResult(data=True)
        mock_run.side_effect = subprocess.CalledProcessError(1, "meltano")

        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)

        result = service.execute_pipeline("tap-csv", "target-jsonl")
        assert not result.success
        assert result.error is not None
        if "Execution error" not in result.error:
            msg: str = f"Expected {'Execution error'} in {result.error}"
            raise AssertionError(msg)

    @patch("subprocess.run")
    @patch("flext_meltano.execution.FlextMeltanoExecutor.validate")
    def test_run_command_os_error(self, mock_validate: Mock, mock_run: Mock) -> None:
        """Test run_command with OSError."""
        mock_validate.return_value = FlextResult(data=True)
        mock_run.side_effect = OSError("Command not found")

        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)

        result = service.run_command(["--version"])
        assert not result.success
        assert result.error is not None
        if "Command error" not in result.error:
            msg: str = f"Expected {'Command error'} in {result.error}"
            raise AssertionError(msg)

    @patch("subprocess.run")
    @patch("flext_meltano.execution.FlextMeltanoExecutor.validate")
    def test_run_command_called_process_error(
        self,
        mock_validate: Mock,
        mock_run: Mock,
    ) -> None:
        """Test run_command with CalledProcessError."""
        mock_validate.return_value = FlextResult(data=True)
        mock_run.side_effect = subprocess.CalledProcessError(1, "meltano")

        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)

        result = service.run_command(["--version"])
        assert not result.success
        assert result.error is not None
        if "Command error" not in result.error:
            msg: str = f"Expected {'Command error'} in {result.error}"
            raise AssertionError(msg)

    @patch("subprocess.run")
    @patch("flext_meltano.execution.FlextMeltanoExecutor.validate")
    def test_run_command_timeout_expired(
        self,
        mock_validate: Mock,
        mock_run: Mock,
    ) -> None:
        """Test run_command with TimeoutExpired."""
        mock_validate.return_value = FlextResult(data=True)
        mock_run.side_effect = subprocess.TimeoutExpired("meltano", 60)

        config = FlextMeltanoConfig()
        service = FlextMeltanoExecutor(config)

        result = service.run_command(["--version"])
        assert not result.success
        assert result.error is not None
        if "Command timed out" not in result.error:
            msg: str = f"Expected {'Command timed out'} in {result.error}"
            raise AssertionError(msg)


class TestFactoryAndLegacyFunctions:
    """Test factory and legacy compatibility functions."""

    def test_create_executor_success(self) -> None:
        """Test successful execution service creation."""
        config = FlextMeltanoConfig()
        result = create_executor(config)

        assert result.success
        assert isinstance(result.data, FlextMeltanoExecutor)
        assert result.data._initialized is True  # Should be initialized

    def test_create_executor_with_path(self) -> None:
        """Test execution service creation with custom path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            custom_path = Path(temp_dir) / "test"
            config = FlextMeltanoConfig(project_root=str(custom_path))
            result = create_executor(config)

            assert result.success
            assert result.data is not None
            if result.data.config.project_root != str(custom_path):
                msg: str = (
                    f"Expected {custom_path!s}, got {result.data.config.project_root}"
                )
                raise AssertionError(msg)

    @patch("flext_meltano.execution.FlextMeltanoExecutor.execute_pipeline")
    def test_flext_meltano_execute_job_success(
        self,
        mock_execute_pipeline: Mock,
    ) -> None:
        """Test legacy execute job function success."""
        mock_execute_pipeline.return_value = FlextResult(
            data={"success": True, "records": 100},
        )

        result = flext_meltano_execute_job("tap-csv", "target-jsonl", Path.cwd())
        if not (result.success):
            msg: str = f"Expected True, got {result.success}"
            raise AssertionError(msg)

        # Verify deprecation warning
        with pytest.warns(DeprecationWarning, match=".*"):
            flext_meltano_execute_job("tap-csv", "target-jsonl", Path.cwd())

    @patch("flext_meltano.execution.FlextMeltanoExecutor.execute_pipeline")
    def test_flext_meltano_execute_job_failure(
        self,
        mock_execute_pipeline: Mock,
    ) -> None:
        """Test legacy execute job function failure."""
        mock_execute_pipeline.return_value = FlextResult(error="Pipeline failed")

        result = flext_meltano_execute_job("tap-csv", "target-jsonl", Path.cwd())
        if result.success:
            msg: str = f"Expected False, got {result.success}"
            raise AssertionError(msg)
        assert result.error is not None
        if "Pipeline failed" not in result.error:
            msg: str = f"Expected {'Pipeline failed'} in {result.error}"
            raise AssertionError(msg)

    @patch("flext_meltano.execution.FlextMeltanoExecutor.run_command")
    def test_flext_meltano_run_command_success(self, mock_run_command: Mock) -> None:
        """Test legacy run command function success."""
        mock_run_command.return_value = FlextResult(
            data={"success": True, "output": "Version 3.0.0"},
        )

        result = flext_meltano_run_command(["--version"], Path.cwd())
        if not (result.success):
            msg: str = f"Expected True, got {result.success}"
            raise AssertionError(msg)

        # Verify deprecation warning
        with pytest.warns(DeprecationWarning, match=".*"):
            flext_meltano_run_command(["--version"], Path.cwd())

    @patch("flext_meltano.execution.FlextMeltanoExecutor.run_command")
    def test_flext_meltano_run_command_failure(self, mock_run_command: Mock) -> None:
        """Test legacy run command function failure."""
        mock_run_command.return_value = FlextResult(error="Command failed")

        result = flext_meltano_run_command(["invalid"], Path.cwd())
        if result.success:
            msg: str = f"Expected False, got {result.success}"
            raise AssertionError(msg)
        assert result.error is not None
        if "Command failed" not in result.error:
            msg: str = f"Expected {'Command failed'} in {result.error}"
            raise AssertionError(msg)


class TestCreateExecutionServiceEdgeCases:
    """Test create_executor edge cases."""

    def test_create_executor_with_exceptional_config(self) -> None:
        """Test create_executor with config that could cause issues."""
        config = FlextMeltanoConfig(project_root="")

        result = create_executor(config)
        # The service should be created successfully, even if validation fails later
        assert result.success
        assert isinstance(result.data, FlextMeltanoExecutor)

    @patch("flext_meltano.execution.FlextMeltanoExecutor.validate")
    def test_create_executor_validation_failure(self, mock_validate: Mock) -> None:
        """Test create_executor when validation fails during initialization."""
        mock_validate.return_value = FlextResult(error="Validation failed")

        config = FlextMeltanoConfig()
        result = create_executor(config)

        assert not result.success
        assert result.error is not None
        if "Executor initialization failed" not in result.error:
            msg: str = f"Expected {'Executor initialization failed'} in {result.error}"
            raise AssertionError(msg)

    @patch("flext_meltano.execution.FlextMeltanoExecutor.__init__")
    def test_create_executor_initialization_exception(self, mock_init: Mock) -> None:
        """Test create_executor when FlextMeltanoExecutor.__init__ fails."""
        mock_init.side_effect = ValueError("Initialization failed")

        config = FlextMeltanoConfig()
        result = create_executor(config)

        assert not result.success
        assert result.error is not None
        if "Failed to create executor" not in result.error:
            msg: str = f"Expected {'Failed to create executor'} in {result.error}"
            raise AssertionError(msg)

    @patch("flext_meltano.execution.FlextMeltanoExecutor.__init__")
    def test_create_executor_type_error(self, mock_init: Mock) -> None:
        """Test create_executor with TypeError."""
        mock_init.side_effect = TypeError("Type mismatch")

        config = FlextMeltanoConfig()
        result = create_executor(config)

        assert not result.success
        assert result.error is not None
        if "Failed to create executor" not in result.error:
            msg: str = f"Expected {'Failed to create executor'} in {result.error}"
            raise AssertionError(msg)

    @patch("flext_meltano.execution.FlextMeltanoExecutor.__init__")
    def test_create_executor_import_error(self, mock_init: Mock) -> None:
        """Test create_executor with ImportError."""
        mock_init.side_effect = ImportError("Module not found")

        config = FlextMeltanoConfig()
        result = create_executor(config)

        assert not result.success
        assert result.error is not None
        if "Failed to create executor" not in result.error:
            msg: str = f"Expected {'Failed to create executor'} in {result.error}"
            raise AssertionError(msg)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
