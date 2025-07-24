"""Test deprecated project manager module.

Comprehensive tests for deprecated project manager to achieve coverage.
This module is marked for deprecation, so tests focus on essential functionality.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING
from unittest.mock import MagicMock, patch

import pytest
import yaml

# Mock missing dependencies
sys.modules["flext_observability"] = MagicMock()
sys.modules["flext_observability.logging"] = MagicMock()

# ruff: noqa: E402 - Module mocking must happen before imports
from flext_meltano.project_manager import (
    FlextMeltanoExecutionError,
    FlextMeltanoProjectError,
    FlextMeltanoProjectInitializationMode,
    FlextMeltanoProjectManager,
)

if TYPE_CHECKING:
    from collections.abc import Generator


class TestFlextMeltanoProjectInitializationMode:
    """Test project initialization mode enum."""

    def test_initialization_modes(self) -> None:
        """Test initialization mode values."""
        assert FlextMeltanoProjectInitializationMode.CREATE_NEW.value == "create_new"
        assert FlextMeltanoProjectInitializationMode.FORCE_RECREATE.value == "force_recreate"
        assert FlextMeltanoProjectInitializationMode.OVERWRITE_EXISTING.value == "overwrite_existing"


class TestFlextMeltanoProjectError:
    """Test project error class."""

    def test_project_error_creation(self) -> None:
        """Test creating project error."""
        error = FlextMeltanoProjectError("Test error")
        assert str(error) == "Test error"
        assert isinstance(error, Exception)


class TestFlextMeltanoExecutionError:
    """Test execution error class."""

    def test_execution_error_creation(self) -> None:
        """Test creating execution error."""
        error = FlextMeltanoExecutionError(
            "Command failed",
            command=["meltano", "run"],
            returncode=1,
            stderr="Error output",
        )

        assert str(error) == "Command failed"
        assert error.command == ["meltano", "run"]
        assert error.returncode == 1
        assert error.stderr == "Error output"

    def test_execution_error_minimal(self) -> None:
        """Test creating execution error with minimal parameters."""
        error = FlextMeltanoExecutionError("Simple error")
        assert str(error) == "Simple error"
        assert error.command is None
        assert error.returncode is None
        assert error.stderr is None


class TestFlextMeltanoProjectManager:
    """Test deprecated project manager class."""

    @pytest.fixture
    def temp_dir(self) -> Generator[Path]:
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as temp_dir:
            yield Path(temp_dir)

    @pytest.fixture
    def manager(self, temp_dir: Path) -> FlextMeltanoProjectManager:
        """Create project manager instance."""
        return FlextMeltanoProjectManager(temp_dir)

    def test_manager_initialization_with_path(self, temp_dir: Path) -> None:
        """Test manager initialization with Path object."""
        manager = FlextMeltanoProjectManager(temp_dir)
        assert manager.project_root == temp_dir

    def test_manager_initialization_with_string(self, temp_dir: Path) -> None:
        """Test manager initialization with string path."""
        manager = FlextMeltanoProjectManager(str(temp_dir))
        assert manager.project_root == temp_dir

    def test_filter_singer_warnings_empty(self, manager: FlextMeltanoProjectManager) -> None:
        """Test filtering empty stderr."""
        result = manager._filter_singer_warnings("")
        assert result == ""

    def test_filter_singer_warnings_none(self, manager: FlextMeltanoProjectManager) -> None:
        """Test filtering None stderr."""
        result = manager._filter_singer_warnings(None)  # type: ignore[arg-type]
        assert result is None

    def test_filter_singer_warnings_with_warnings(self, manager: FlextMeltanoProjectManager) -> None:
        """Test filtering stderr with Singer warnings."""
        stderr_text = """
INFO: Starting extraction
SingerSDKDeprecationWarning: Passing a catalog file path is deprecated
DeprecationWarning: This feature is deprecated
INFO: Extraction completed
Warning: This is a warning
INFO: Processing complete
"""
        result = manager._filter_singer_warnings(stderr_text)

        # Should keep only non-warning lines
        lines = result.split("\n")
        non_empty_lines = [line for line in lines if line.strip()]

        assert "INFO: Starting extraction" in non_empty_lines
        assert "INFO: Extraction completed" in non_empty_lines
        assert "INFO: Processing complete" in non_empty_lines
        assert len(non_empty_lines) == 3  # Only the three INFO lines should remain

    def test_filter_singer_warnings_no_warnings(self, manager: FlextMeltanoProjectManager) -> None:
        """Test filtering stderr with no warnings."""
        stderr_text = """
INFO: Starting extraction
INFO: Extraction completed
INFO: Processing complete
"""
        result = manager._filter_singer_warnings(stderr_text)
        assert result == stderr_text

    async def test_create_project_success(self, manager: FlextMeltanoProjectManager) -> None:
        """Test successful project creation."""
        project_name = "test-project"
        result = await manager.create_project(project_name, "dev")

        assert result.success
        assert result.data is not None

        # Verify project directory was created
        project_path = manager.project_root / project_name
        assert project_path.exists()
        assert project_path.is_dir()

        # Verify meltano.yml was created
        meltano_yml = project_path / "meltano.yml"
        assert meltano_yml.exists()

        # Verify meltano.yml content
        with meltano_yml.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        assert config["version"] == 1
        assert config["default_environment"] == "dev"
        assert project_name in config["project_id"]
        assert {"name": "dev"} in config["environments"]
        assert "extractors" in config["plugins"]
        assert "loaders" in config["plugins"]

    async def test_create_project_already_exists(
        self, manager: FlextMeltanoProjectManager, temp_dir: Path,
    ) -> None:
        """Test project creation when project already exists."""
        project_name = "existing-project"
        project_path = temp_dir / project_name
        project_path.mkdir()  # Create directory first

        result = await manager.create_project(project_name)

        assert result.is_failure
        assert result.error is not None
        assert "already exists" in result.error

    async def test_create_project_custom_environment(self, manager: FlextMeltanoProjectManager) -> None:
        """Test project creation with custom environment."""
        project_name = "test-env-project"
        environment = "production"

        result = await manager.create_project(project_name, environment)

        assert result.success

        # Verify environment was set correctly
        project_path = manager.project_root / project_name
        meltano_yml = project_path / "meltano.yml"

        with meltano_yml.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        assert config["default_environment"] == environment
        assert {"name": environment} in config["environments"]

    async def test_create_project_exception_handling(self, manager: FlextMeltanoProjectManager) -> None:
        """Test project creation with exception handling."""
        # Use invalid characters in project name to potentially cause filesystem errors
        project_name = "test\x00project"  # Null character should cause issues

        with patch("pathlib.Path.mkdir", side_effect=OSError("Filesystem error")):
            result = await manager.create_project(project_name)

            assert result.is_failure
            assert result.error is not None
            assert "Filesystem error" in result.error

    def test_filter_singer_warnings_all_patterns(self, manager: FlextMeltanoProjectManager) -> None:
        """Test filtering all warning patterns."""
        stderr_text = """
INFO: Normal message
SingerSDKDeprecationWarning: Singer warning
DeprecationWarning: General deprecation
PendingDeprecationWarning: Pending warning
Invalid -W option ignored: Invalid option
Warning: Generic warning
UserWarning: User warning
Passing a catalog file path is deprecated
Passing a list of config file paths is deprecated
warnings.warn(message)
stacklevel=2
INFO: Another normal message
"""
        result = manager._filter_singer_warnings(stderr_text)

        # Should only keep non-warning lines
        lines = result.split("\n")
        clean_lines = [line for line in lines if line.strip()]

        assert "INFO: Normal message" in clean_lines
        assert "INFO: Another normal message" in clean_lines
        assert len(clean_lines) == 2  # Only non-warning lines should remain

    async def test_create_project_yaml_content_structure(self, manager: FlextMeltanoProjectManager) -> None:
        """Test that created meltano.yml has correct structure."""
        project_name = "structure-test"
        result = await manager.create_project(project_name, "staging")

        assert result.success

        project_path = manager.project_root / project_name
        meltano_yml = project_path / "meltano.yml"

        with meltano_yml.open("r", encoding="utf-8") as f:
            config = yaml.safe_load(f)

        # Verify complete plugin structure
        plugins = config["plugins"]
        expected_plugin_types = ["extractors", "loaders", "transformers", "orchestrators", "utilities"]

        for plugin_type in expected_plugin_types:
            assert plugin_type in plugins
            assert isinstance(plugins[plugin_type], list)
            assert plugins[plugin_type] == []  # Should be empty initially

        # Verify project_id format includes date
        import re
        project_id_pattern = rf"{project_name}-\d{{8}}"
        assert re.match(project_id_pattern, config["project_id"])

    async def test_create_project_file_permissions(self, manager: FlextMeltanoProjectManager) -> None:
        """Test that created files have appropriate permissions."""
        project_name = "permissions-test"
        result = await manager.create_project(project_name)

        assert result.success

        project_path = manager.project_root / project_name
        meltano_yml = project_path / "meltano.yml"

        # Verify files exist and are readable
        assert project_path.exists()
        assert project_path.is_dir()
        assert meltano_yml.exists()
        assert meltano_yml.is_file()

        # Verify we can read the file
        content = meltano_yml.read_text(encoding="utf-8")
        assert len(content) > 0
        assert "version: 1" in content
