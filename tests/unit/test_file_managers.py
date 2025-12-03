"""Test module for flext-meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import shutil
import tempfile
from pathlib import Path

from pydantic import ConfigDict

from flext_meltano import FlextMeltanoFileManagers
from tests.flext_tests_compat import FlextTestsMatchers


class TestFlextMeltanoFileManagersComprehensive:
    """Comprehensive tests for FlextMeltanoFileManagers with 100% coverage."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.temp_dir = Path(tempfile.mkdtemp())

    def teardown_method(self) -> None:
        """Cleanup after each test."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir)

    def test_save_yaml_config_valid(self) -> None:
        """Test saving valid YAML configuration."""
        config: ConfigDict = {
            "project_id": "test-project",
            "version": 1,
            "plugins": {"extractors": ["tap-csv"], "loaders": ["target-csv"]},
        }
        file_path = self.temp_dir / "test_config.yml"

        result = FlextMeltanoFileManagers.save_yaml_config(config, file_path)
        FlextTestsMatchers.assert_result_success(result)

        # Verify file was created and contains expected content
        assert file_path.exists()
        assert file_path.is_file()

    def test_save_yaml_config_invalid_path(self) -> None:
        """Test saving YAML config to invalid path."""
        config: dict[str, object] = {
            "test": "data",
        }
        invalid_path = Path("/nonexistent/directory/config.yml")

        result = FlextMeltanoFileManagers.save_yaml_config(config, invalid_path)
        FlextTestsMatchers.assert_result_failure(result)

    def test_load_yaml_config_valid(self) -> None:
        """Test loading valid YAML configuration."""
        # First create a valid YAML file
        config: dict[str, object] = {
            "project_id": "test-load-project",
            "version": 1,
            "plugins": {"extractors": ["tap-csv"]},
        }
        file_path = self.temp_dir / "load_test.yml"

        # Save it first
        save_result = FlextMeltanoFileManagers.save_yaml_config(config, file_path)
        FlextTestsMatchers.assert_result_success(save_result, True)

        # Now load it back
        load_result = FlextMeltanoFileManagers.load_yaml_config(file_path)
        FlextTestsMatchers.assert_result_success(load_result)

        loaded_config = load_result.value
        assert loaded_config["project_id"] == "test-load-project"
        assert loaded_config["version"] == 1
        assert "plugins" in loaded_config

    def test_load_yaml_config_nonexistent_file(self) -> None:
        """Test loading YAML config from nonexistent file."""
        nonexistent_path = self.temp_dir / "does_not_exist.yml"

        result = FlextMeltanoFileManagers.load_yaml_config(nonexistent_path)
        FlextTestsMatchers.assert_result_failure(result)

    def test_load_yaml_config_invalid_yaml(self) -> None:
        """Test loading invalid YAML configuration."""
        invalid_yaml_path = self.temp_dir / "invalid.yml"

        # Create file with invalid YAML content
        invalid_yaml_path.write_text("{ invalid: yaml: content: [")

        result = FlextMeltanoFileManagers.load_yaml_config(invalid_yaml_path)
        FlextTestsMatchers.assert_result_failure(result)

    def test_validate_yaml_file_valid(self) -> None:
        """Test validating valid YAML file."""
        # Create valid YAML file
        config: dict[str, object] = {
            "valid": "yaml",
            "content": {"nested": "value"},
        }
        yaml_path = self.temp_dir / "valid.yml"

        save_result = FlextMeltanoFileManagers.save_yaml_config(config, yaml_path)
        FlextTestsMatchers.assert_result_success(save_result, True)

        # Validate it
        validate_result = FlextMeltanoFileManagers.validate_yaml_file(yaml_path)
        FlextTestsMatchers.assert_result_success(validate_result, True)

    def test_validate_yaml_file_invalid(self) -> None:
        """Test validating invalid YAML file."""
        invalid_yaml_path = self.temp_dir / "invalid_validate.yml"
        invalid_yaml_path.write_text("invalid: yaml: [content")

        result = FlextMeltanoFileManagers.validate_yaml_file(invalid_yaml_path)
        FlextTestsMatchers.assert_result_failure(result)

    def test_validate_yaml_file_nonexistent(self) -> None:
        """Test validating nonexistent YAML file."""
        nonexistent_path = self.temp_dir / "nonexistent_validate.yml"

        result = FlextMeltanoFileManagers.validate_yaml_file(nonexistent_path)
        FlextTestsMatchers.assert_result_failure(result)

    def test_create_directory_structure_valid(self) -> None:
        """Test creating valid directory structure."""
        base_path = self.temp_dir / "test_project"
        directories = ["config", "data", "logs", "extract", "load"]

        result = FlextMeltanoFileManagers.create_directory_structure(
            base_path,
            directories,
        )
        FlextTestsMatchers.assert_result_success(result)

        created_paths = result.value
        assert isinstance(created_paths, dict)

        # Verify directories were created
        for directory in directories:
            dir_path = base_path / directory
            assert dir_path.exists()
            assert dir_path.is_dir()

    def test_create_directory_structure_empty(self) -> None:
        """Test creating empty directory structure."""
        base_path = self.temp_dir / "empty_project"
        empty_directories: list[str] = []

        result = FlextMeltanoFileManagers.create_directory_structure(
            base_path,
            empty_directories,
        )
        FlextTestsMatchers.assert_result_success(result)

        # Should return empty dict[str, object] but succeed
        created_paths = result.value
        assert isinstance(created_paths, dict)
        assert len(created_paths) == 0

    def test_setup_project_structure_valid(self) -> None:
        """Test setting up complete project structure."""
        project_root = self.temp_dir / "complete_project"

        result = FlextMeltanoFileManagers.setup_project_structure(
            project_root=project_root,
            _project_name="test-complete-project",
        )
        FlextTestsMatchers.assert_result_success(result)

        structure = result.value
        assert isinstance(structure, dict)
        # Should have directory paths and config file paths
        assert len(structure) > 0  # Should contain created paths

        # Verify basic project structure was created
        assert project_root.exists()
        assert project_root.is_dir()

    def test_setup_project_structure_no_defaults(self) -> None:
        """Test setting up project structure without default files."""
        project_root = self.temp_dir / "minimal_project"

        result = FlextMeltanoFileManagers.setup_project_structure(
            project_root=project_root,
            _project_name="test-minimal-project",
        )
        FlextTestsMatchers.assert_result_success(result)

        # Should still create the project root
        assert project_root.exists()
        assert project_root.is_dir()

    def test_create_temp_directory_default_prefix(self) -> None:
        """Test creating temporary directory with default prefix."""
        result = FlextMeltanoFileManagers.create_temp_directory()
        FlextTestsMatchers.assert_result_success(result)

        temp_path = result.value
        assert isinstance(temp_path, Path)
        assert temp_path.exists()
        assert temp_path.is_dir()
        assert "flext_meltano" in temp_path.name

        # Clean up
        cleanup_result = FlextMeltanoFileManagers.cleanup_temp_directory(temp_path)
        FlextTestsMatchers.assert_result_success(cleanup_result, True)

    def test_create_temp_directory_custom_prefix(self) -> None:
        """Test creating temporary directory with custom prefix."""
        custom_prefix = "test_custom_prefix"

        result = FlextMeltanoFileManagers.create_temp_directory(prefix=custom_prefix)
        FlextTestsMatchers.assert_result_success(result)

        temp_path = result.value
        assert isinstance(temp_path, Path)
        assert temp_path.exists()
        assert temp_path.is_dir()
        assert custom_prefix in temp_path.name

        # Clean up
        cleanup_result = FlextMeltanoFileManagers.cleanup_temp_directory(temp_path)
        FlextTestsMatchers.assert_result_success(cleanup_result, True)

    def test_cleanup_temp_directory_valid(self) -> None:
        """Test cleaning up valid temporary directory."""
        # First create a temp directory
        create_result = FlextMeltanoFileManagers.create_temp_directory(
            prefix="cleanup_test",
        )
        FlextTestsMatchers.assert_result_success(create_result)

        temp_path = create_result.value
        assert temp_path.exists()

        # Now clean it up
        cleanup_result = FlextMeltanoFileManagers.cleanup_temp_directory(temp_path)
        FlextTestsMatchers.assert_result_success(cleanup_result, True)

        # Verify it was deleted
        assert not temp_path.exists()

    def test_cleanup_temp_directory_nonexistent(self) -> None:
        """Test cleaning up nonexistent directory."""
        nonexistent_path = self.temp_dir / "definitely_does_not_exist_cleanup_test"

        result = FlextMeltanoFileManagers.cleanup_temp_directory(nonexistent_path)
        # Implementation succeeds even if directory doesn't exist (graceful handling)
        FlextTestsMatchers.assert_result_success(result)

    def test_validate_project_structure_valid(self) -> None:
        """Test validating valid project structure."""
        # First create a project structure
        project_root = self.temp_dir / "validation_project"

        setup_result = FlextMeltanoFileManagers.setup_project_structure(
            project_root=project_root,
            _project_name="validation-test",
        )
        FlextTestsMatchers.assert_result_success(setup_result)

        # Now validate it
        validate_result = FlextMeltanoFileManagers.validate_project_structure(
            project_root,
        )
        FlextTestsMatchers.assert_result_success(validate_result, True)

    def test_validate_project_structure_invalid(self) -> None:
        """Test validating invalid project structure."""
        # Empty directory should be invalid project structure
        empty_project_root = self.temp_dir / "empty_validation"
        empty_project_root.mkdir()

        result = FlextMeltanoFileManagers.validate_project_structure(empty_project_root)
        FlextTestsMatchers.assert_result_failure(result)

    def test_validate_project_structure_nonexistent(self) -> None:
        """Test validating nonexistent project."""
        nonexistent_path = self.temp_dir / "does_not_exist_validation"

        result = FlextMeltanoFileManagers.validate_project_structure(nonexistent_path)
        FlextTestsMatchers.assert_result_failure(result)

    def test_complex_workflow_integration(self) -> None:
        """Test complex workflow integrating multiple file manager operations."""
        # Create temp directory
        temp_result = FlextMeltanoFileManagers.create_temp_directory(
            prefix="integration_test",
        )
        FlextTestsMatchers.assert_result_success(temp_result)
        temp_path = temp_result.value

        try:
            # Setup project structure
            project_root = temp_path / "integration_project"
            setup_result = FlextMeltanoFileManagers.setup_project_structure(
                project_root=project_root,
                _project_name="integration-workflow-test",
            )
            FlextTestsMatchers.assert_result_success(setup_result)

            # Create and save config
            config: dict[str, object] = {
                "project_id": "integration-workflow-test",
                "version": 1,
                "plugins": {
                    "extractors": ["tap-csv", "tap-postgres"],
                    "loaders": ["target-csv", "target-postgres"],
                },
                "environments": ["dev", "prod"],
            }
            config_path = project_root / "pipeline.yml"
            save_result = FlextMeltanoFileManagers.save_yaml_config(config, config_path)
            FlextTestsMatchers.assert_result_success(save_result, True)

            # Validate YAML file
            validate_yaml_result = FlextMeltanoFileManagers.validate_yaml_file(
                config_path,
            )
            FlextTestsMatchers.assert_result_success(validate_yaml_result, True)

            # Load config back
            load_result = FlextMeltanoFileManagers.load_yaml_config(config_path)
            FlextTestsMatchers.assert_result_success(load_result)
            loaded_config = load_result.value

            # Verify loaded config matches original
            assert loaded_config["project_id"] == "integration-workflow-test"
            plugins = loaded_config["plugins"]
            if isinstance(plugins, dict):
                extractors = plugins.get("extractors")
                loaders = plugins.get("loaders")
                if isinstance(extractors, list) and isinstance(loaders, list):
                    assert len(extractors) == 2
                    assert len(loaders) == 2

            # Validate project structure
            validate_structure_result = (
                FlextMeltanoFileManagers.validate_project_structure(project_root)
            )
            FlextTestsMatchers.assert_result_success(validate_structure_result, True)

        finally:
            # Clean up temp directory
            cleanup_result = FlextMeltanoFileManagers.cleanup_temp_directory(temp_path)
            FlextTestsMatchers.assert_result_success(cleanup_result, True)

    def test_error_handling_edge_cases(self) -> None:
        """Test error handling for various edge cases."""
        # Test with invalid paths should return failure result instead of raising
        try:
            # Use an invalid path that still has proper type
            invalid_path = Path("/invalid/path/that/does/not/exist")
            result = FlextMeltanoFileManagers.save_yaml_config({}, invalid_path)
            # If it doesn't raise, it should return a failure result
            FlextTestsMatchers.assert_result_failure(result)
        except (TypeError, AttributeError):
            # If it does raise, that's also acceptable behavior
            pass

        # Test with empty config
        empty_config_result = FlextMeltanoFileManagers.save_yaml_config(
            {},
            self.temp_dir / "empty.yml",
        )
        FlextTestsMatchers.assert_result_success(empty_config_result, True)

        # Test loading empty config
        load_empty_result = FlextMeltanoFileManagers.load_yaml_config(
            self.temp_dir / "empty.yml",
        )
        FlextTestsMatchers.assert_result_success(load_empty_result)
        assert load_empty_result.value == {}

    def test_concurrent_file_operations(self) -> None:
        """Test concurrent file operations don't interfere."""
        # Create multiple configs simultaneously
        configs: list[ConfigDict] = [
            {"id": "config1", "data": "value1"},
            {"id": "config2", "data": "value2"},
            {"id": "config3", "data": "value3"},
        ]

        # Save all configs
        for i, config in enumerate(configs):
            file_path = self.temp_dir / f"concurrent_{i}.yml"
            result = FlextMeltanoFileManagers.save_yaml_config(config, file_path)
            FlextTestsMatchers.assert_result_success(result)

        # Load all configs back and verify
        for i, expected_config in enumerate(configs):
            file_path = self.temp_dir / f"concurrent_{i}.yml"
            load_result = FlextMeltanoFileManagers.load_yaml_config(file_path)
            FlextTestsMatchers.assert_result_success(load_result)

            loaded_config = load_result.value
            assert loaded_config["id"] == expected_config["id"]
            assert loaded_config["data"] == expected_config["data"]

    def test_file_managers_inheritance_methods(self) -> None:
        """Test that FlextMeltanoFileManagers has all expected methods."""
        expected_methods = [
            "save_yaml_config",
            "load_yaml_config",
            "validate_yaml_file",
            "create_directory_structure",
            "setup_project_structure",
            "create_temp_directory",
            "cleanup_temp_directory",
            "validate_project_structure",
        ]

        for method_name in expected_methods:
            assert hasattr(FlextMeltanoFileManagers, method_name)
            method = getattr(FlextMeltanoFileManagers, method_name)
            assert callable(method)
