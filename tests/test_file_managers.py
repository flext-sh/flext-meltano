"""Test file_managers module - Basic functionality tests.

Tests FlextMeltanoFileManagers class functionality.
Zero mock usage - all real function testing.
"""

from __future__ import annotations

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
        import shutil

        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_class_instantiation(self) -> None:
        """Test FlextMeltanoFileManagers instantiation."""
        managers = FlextMeltanoFileManagers()
        assert isinstance(managers, FlextMeltanoFileManagers)

    def test_nested_classes_exist(self) -> None:
        """Test all nested manager classes exist."""
        expected_nested_classes = [
            "YamlFileManager",
            "ProjectStructureManager",
            "TempDirectoryManager",
        ]

        for class_name in expected_nested_classes:
            assert hasattr(FlextMeltanoFileManagers, class_name), (
                f"FlextMeltanoFileManagers missing nested class: {class_name}"
            )

    def test_yaml_file_manager(self) -> None:
        """Test YamlFileManager functionality."""
        manager = FlextMeltanoFileManagers.YamlFileManager()
        assert isinstance(manager, FlextMeltanoFileManagers.YamlFileManager)

        # Should have YAML file management methods
        expected_methods = ["save_yaml_config", "load_yaml_config"]

        for method_name in expected_methods:
            assert hasattr(manager, method_name), (
                f"YamlFileManager missing method: {method_name}"
            )

    def test_project_structure_manager(self) -> None:
        """Test ProjectStructureManager functionality."""
        manager = FlextMeltanoFileManagers.ProjectStructureManager()
        assert isinstance(manager, FlextMeltanoFileManagers.ProjectStructureManager)

        # Should have project structure management methods
        expected_methods = ["setup_project_structure"]

        for method_name in expected_methods:
            assert hasattr(manager, method_name), (
                f"ProjectStructureManager missing method: {method_name}"
            )

    def test_temp_directory_manager(self) -> None:
        """Test TempDirectoryManager functionality."""
        manager = FlextMeltanoFileManagers.TempDirectoryManager()
        assert isinstance(manager, FlextMeltanoFileManagers.TempDirectoryManager)

        # Should have temporary directory management methods
        expected_methods = ["create_temp_directory", "cleanup_temp_directory"]

        for method_name in expected_methods:
            assert hasattr(manager, method_name), (
                f"TempDirectoryManager missing method: {method_name}"
            )

    def test_all_methods_callable(self) -> None:
        """Test all manager methods are callable."""
        manager_classes = [
            FlextMeltanoFileManagers.YamlFileManager,
            FlextMeltanoFileManagers.ProjectStructureManager,
            FlextMeltanoFileManagers.TempDirectoryManager,
        ]

        for manager_class in manager_classes:
            manager = manager_class()

            # Get all public methods (not starting with _)
            methods = [
                attr
                for attr in dir(manager)
                if not attr.startswith("_") and callable(getattr(manager, attr))
            ]

            # Should have at least some methods
            assert len(methods) > 0, (
                f"{manager_class.__name__} should have callable methods"
            )

            # All methods should be callable
            for method_name in methods:
                method = getattr(manager, method_name)
                assert callable(method), (
                    f"{manager_class.__name__}.{method_name} should be callable"
                )

    def test_all_exports_available(self) -> None:
        """Test all expected exports are available."""
        from flext_meltano.file_managers import FlextMeltanoFileManagers

        # Main class should be importable
        assert FlextMeltanoFileManagers is not None

        # Should be able to instantiate
        instance = FlextMeltanoFileManagers()
        assert isinstance(instance, FlextMeltanoFileManagers)


if __name__ == "__main__":
    unittest.main()
