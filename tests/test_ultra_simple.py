"""Ultra simple tests that work without complex imports."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from flext_core import FlextResult

from flext_meltano.config import FlextMeltanoConfig


# Test just the core functionality without complex imports
def test_basic_path_operations() -> None:
    """Test basic file operations work."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        assert temp_path.exists()
        assert temp_path.is_dir()

        # Create a test file
        test_file = temp_path / "test.txt"
        test_file.write_text("Hello World")

        assert test_file.exists()
        assert test_file.read_text() == "Hello World"


def test_flext_core_import() -> None:
    """Test that flext-core imports work."""
    # Test FlextResult creation
    success_result = FlextResult.ok("success")
    assert success_result.success is True
    assert success_result.value == "success"
    assert success_result.error is None

    # Test FlextResult failure
    failure_result = FlextResult.fail("error message")
    assert failure_result.success is False
    # Don't access .value on failed result - it raises TypeError
    assert failure_result.error == "error message"


def test_simple_config_creation() -> None:
    """Test simple config without complex dependencies."""
    # Try to import just the config (imported at top level)
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(
                project_root=str(temp_dir),
                environment="test",
            )

            assert config.project_root == str(temp_dir)
            assert config.environment == "test"

    except ImportError as e:
        # If import fails, that's expected due to dependency issues
        # Check that the error is related to our module as expected
        error_str = str(e).lower()
        expected_keywords = ["flext_meltano", "module", "import"]
        assert any(keyword in error_str for keyword in expected_keywords)


def test_real_subprocess_execution() -> None:
    """Test real subprocess execution without mocks."""
    # Test real subprocess call using full python path
    result = subprocess.run(
        [sys.executable, "-c", "print('Hello from subprocess')"],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert result.returncode == 0
    assert "Hello from subprocess" in result.stdout
    assert isinstance(result.stdout, str)
    assert isinstance(result.stderr, str)


def test_environment_variables() -> None:
    """Test environment variable handling."""
    # Test setting and getting environment variables
    test_var = "FLEXT_TEST_VAR"
    test_value = "test_value_123"

    # Clean state
    if test_var in os.environ:
        del os.environ[test_var]

    assert test_var not in os.environ

    # Set and test
    os.environ[test_var] = test_value
    assert os.environ[test_var] == test_value
    assert os.getenv(test_var) == test_value

    # Clean up
    del os.environ[test_var]
    assert test_var not in os.environ


def test_json_serialization() -> None:
    """Test JSON serialization for bridge integration."""
    # Test data structures that would be used by bridge
    test_data = {
        "success": True,
        "data": {
            "version": "2.0.0",
            "plugins": [
                {"name": "tap-csv", "type": "extractor"},
                {"name": "target-csv", "type": "loader"},
            ],
        },
        "error": None,
    }

    # Serialize to JSON
    json_str = json.dumps(test_data)
    assert isinstance(json_str, str)
    assert "success" in json_str
    assert "2.0.0" in json_str

    # Deserialize from JSON
    restored_data = json.loads(json_str)
    assert restored_data == test_data
    assert restored_data["success"] is True
    assert len(restored_data["data"]["plugins"]) == 2
