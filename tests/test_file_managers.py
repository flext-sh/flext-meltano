"""Test module for flext-meltano."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import TestCase

from flext_meltano.file_managers import FlextMeltanoFileManagers


class TestFlextMeltanoFileManagersBasic(TestCase):
    """Basic functionality tests for FlextMeltanoFileManagers."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.file_managers = FlextMeltanoFileManagers()
        self.temp_dir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_class_instantiation(self) -> None:
        """Test FlextMeltanoFileManagers instantiation."""
        managers = FlextMeltanoFileManagers()
        assert isinstance(managers, FlextMeltanoFileManagers)

    def test_class_methods_exist(self) -> None:
        """Test all required file manager methods exist."""
        expected_methods = [
            "save_yaml_config",
            "load_yaml_config",
            "validate_yaml_file",
            "create_directory_structure",
            "create_temp_directory",
            "cleanup_temp_directory",
        ]

        for method_name in expected_methods:
            assert hasattr(FlextMeltanoFileManagers, method_name), (
                f"FlextMeltanoFileManagers missing method: {method_name}"
            )
            # Verify the method is callable
            method = getattr(FlextMeltanoFileManagers, method_name)
            assert callable(method), f"Method {method_name} is not callable"

    def test_yaml_file_manager(self) -> None:
        """Test YAML file manager functionality with class methods."""
        # Test class methods directly since FlextMeltanoFileManagers uses class methods
        expected_methods = [
            "save_yaml_config",
            "load_yaml_config",
            "validate_yaml_file",
        ]

        for method_name in expected_methods:
            assert hasattr(FlextMeltanoFileManagers, method_name), (
                f"FlextMeltanoFileManagers missing method: {method_name}"
            )
            # Verify the method is callable
            method = getattr(FlextMeltanoFileManagers, method_name)
            assert callable(method), f"Method {method_name} is not callable"

    def test_project_structure_manager(self) -> None:
        """Test project structure management functionality."""
        # Test directory structure creation method
        assert hasattr(FlextMeltanoFileManagers, "create_directory_structure"), (
            "FlextMeltanoFileManagers missing create_directory_structure method"
        )

        method = FlextMeltanoFileManagers.create_directory_structure
        assert callable(method), "create_directory_structure is not callable"

    def test_temp_directory_manager(self) -> None:
        """Test temporary directory management functionality."""
        # Test temp directory methods
        temp_methods = ["create_temp_directory", "cleanup_temp_directory"]

        for method_name in temp_methods:
            assert hasattr(FlextMeltanoFileManagers, method_name), (
                f"FlextMeltanoFileManagers missing method: {method_name}"
            )

    def test_all_methods_callable(self) -> None:
        """Test all manager class methods are callable."""
        # FlextMeltanoFileManagers uses class methods, not nested classes
        all_methods = [
            "save_yaml_config",
            "load_yaml_config",
            "validate_yaml_file",
            "create_directory_structure",
            "create_temp_directory",
            "cleanup_temp_directory",
        ]

        for method_name in all_methods:
            # Verify method exists and is callable
            assert hasattr(FlextMeltanoFileManagers, method_name), (
                f"FlextMeltanoFileManagers missing method: {method_name}"
            )
            method = getattr(FlextMeltanoFileManagers, method_name)
            assert callable(method), f"Method {method_name} is not callable"

    def test_all_exports_available(self) -> None:
        """Test all expected exports are available."""
        # Main class should be importable
        assert FlextMeltanoFileManagers is not None

        # Should be able to instantiate
        instance = FlextMeltanoFileManagers()
        assert isinstance(instance, FlextMeltanoFileManagers)


if __name__ == "__main__":
    unittest.main()
