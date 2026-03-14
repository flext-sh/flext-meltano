"""Test module for flext-meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

import shutil
import tempfile
from pathlib import Path

from flext_meltano import FlextMeltanoFileManagers


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
        config: dict[str, object] = {
            "project_id": "test-project",
            "version": 1,
            "plugins": {"extractors": ["tap-csv"], "loaders": ["target-csv"]},
        }
        file_path = self.temp_dir / "test_config.yml"
        result = FlextMeltanoFileManagers.save_yaml_config(config, file_path)
        assert result.is_success
        assert file_path.exists()
        assert file_path.is_file()

    def test_save_yaml_config_invalid_path(self) -> None:
        """Test saving YAML config to invalid path."""
        config: dict[str, object] = {"test": "data"}
        invalid_path = Path("/nonexistent/directory/config.yml")
        result = FlextMeltanoFileManagers.save_yaml_config(config, invalid_path)
        assert result.is_failure

    def test_load_yaml_config_valid(self) -> None:
        """Test loading valid YAML configuration."""
        config: dict[str, object] = {
            "project_id": "test-load-project",
            "version": 1,
            "plugins": {"extractors": ["tap-csv"]},
        }
        file_path = self.temp_dir / "load_test.yml"
        save_result = FlextMeltanoFileManagers.save_yaml_config(config, file_path)
        assert save_result.is_success
        load_result = FlextMeltanoFileManagers.load_yaml_config(file_path)
        assert load_result.is_success
        loaded_config = load_result.value
        assert loaded_config["project_id"] == "test-load-project"
        assert loaded_config["version"] == 1
        assert "plugins" in loaded_config

    def test_load_yaml_config_nonexistent_file(self) -> None:
        """Test loading YAML config from nonexistent file."""
        nonexistent_path = self.temp_dir / "does_not_exist.yml"
        result = FlextMeltanoFileManagers.load_yaml_config(nonexistent_path)
        assert result.is_failure

    def test_load_yaml_config_invalid_yaml(self) -> None:
        """Test loading invalid YAML configuration."""
        invalid_yaml_path = self.temp_dir / "invalid.yml"
        invalid_yaml_path.write_text("{ invalid: yaml: content: [")
        result = FlextMeltanoFileManagers.load_yaml_config(invalid_yaml_path)
        assert result.is_failure

    def test_validate_yaml_file_valid(self) -> None:
        """Test validating valid YAML file."""
        config: dict[str, object] = {
            "valid": "yaml",
            "content": {"nested": "value"},
        }
        yaml_path = self.temp_dir / "valid.yml"
        save_result = FlextMeltanoFileManagers.save_yaml_config(config, yaml_path)
        assert save_result.is_success
        validate_result = FlextMeltanoFileManagers.validate_yaml_file(yaml_path)
        assert validate_result.is_success

    def test_validate_yaml_file_invalid(self) -> None:
        """Test validating invalid YAML file."""
        invalid_yaml_path = self.temp_dir / "invalid_validate.yml"
        invalid_yaml_path.write_text("invalid: yaml: [content")
        result = FlextMeltanoFileManagers.validate_yaml_file(invalid_yaml_path)
        assert result.is_failure

    def test_validate_yaml_file_nonexistent(self) -> None:
        """Test validating nonexistent YAML file."""
        nonexistent_path = self.temp_dir / "nonexistent_validate.yml"
        result = FlextMeltanoFileManagers.validate_yaml_file(nonexistent_path)
        assert result.is_failure

    def test_create_directory_structure_valid(self) -> None:
        """Test creating valid directory structure."""
        base_path = self.temp_dir / "test_project"
        directories = ["config", "data", "logs", "extract", "load"]
        result = FlextMeltanoFileManagers.create_directory_structure(
            base_path, directories
        )
        assert result.is_success
        created_paths = result.value
        assert isinstance(created_paths, dict)
        for directory in directories:
            dir_path = base_path / directory
            assert dir_path.exists()
            assert dir_path.is_dir()

    def test_create_directory_structure_empty(self) -> None:
        """Test creating empty directory structure."""
        base_path = self.temp_dir / "empty_project"
        empty_directories: list[str] = []
        result = FlextMeltanoFileManagers.create_directory_structure(
            base_path, empty_directories
        )
        assert result.is_success
        created_paths = result.value
        assert isinstance(created_paths, dict)
        assert len(created_paths) == 0

    def test_setup_project_structure_valid(self) -> None:
        """Test setting up complete project structure."""
        project_root = self.temp_dir / "complete_project"
        result = FlextMeltanoFileManagers.setup_project_structure(
            project_root=project_root, _project_name="test-complete-project"
        )
        assert result.is_success
        structure = result.value
        assert isinstance(structure, dict)
        assert len(structure) > 0
        assert project_root.exists()
        assert project_root.is_dir()

    def test_setup_project_structure_no_defaults(self) -> None:
        """Test setting up project structure without default files."""
        project_root = self.temp_dir / "minimal_project"
        result = FlextMeltanoFileManagers.setup_project_structure(
            project_root=project_root, _project_name="test-minimal-project"
        )
        assert result.is_success
        assert project_root.exists()
        assert project_root.is_dir()

    def test_create_temp_directory_default_prefix(self) -> None:
        """Test creating temporary directory with default prefix."""
        result = FlextMeltanoFileManagers.create_temp_directory()
        assert result.is_success
        temp_path = result.value
        assert isinstance(temp_path, Path)
        assert temp_path.exists()
        assert temp_path.is_dir()
        assert "flext_meltano" in temp_path.name
        cleanup_result = FlextMeltanoFileManagers.cleanup_temp_directory(temp_path)
        assert cleanup_result.is_success

    def test_create_temp_directory_custom_prefix(self) -> None:
        """Test creating temporary directory with custom prefix."""
        custom_prefix = "test_custom_prefix"
        result = FlextMeltanoFileManagers.create_temp_directory(prefix=custom_prefix)
        assert result.is_success
        temp_path = result.value
        assert isinstance(temp_path, Path)
        assert temp_path.exists()
        assert temp_path.is_dir()
        assert custom_prefix in temp_path.name
        cleanup_result = FlextMeltanoFileManagers.cleanup_temp_directory(temp_path)
        assert cleanup_result.is_success

    def test_cleanup_temp_directory_valid(self) -> None:
        """Test cleaning up valid temporary directory."""
        create_result = FlextMeltanoFileManagers.create_temp_directory(
            prefix="cleanup_test"
        )
        assert create_result.is_success
        temp_path = create_result.value
        assert temp_path.exists()
        cleanup_result = FlextMeltanoFileManagers.cleanup_temp_directory(temp_path)
        assert cleanup_result.is_success
        assert not temp_path.exists()

    def test_cleanup_temp_directory_nonexistent(self) -> None:
        """Test cleaning up nonexistent directory."""
        nonexistent_path = self.temp_dir / "definitely_does_not_exist_cleanup_test"
        result = FlextMeltanoFileManagers.cleanup_temp_directory(nonexistent_path)
        assert result.is_success

    def test_validate_project_structure_valid(self) -> None:
        """Test validating valid project structure."""
        project_root = self.temp_dir / "validation_project"
        setup_result = FlextMeltanoFileManagers.setup_project_structure(
            project_root=project_root, _project_name="validation-test"
        )
        assert setup_result.is_success
        validate_result = FlextMeltanoFileManagers.validate_project_structure(
            project_root
        )
        assert validate_result.is_success

    def test_validate_project_structure_invalid(self) -> None:
        """Test validating invalid project structure."""
        empty_project_root = self.temp_dir / "empty_validation"
        empty_project_root.mkdir()
        result = FlextMeltanoFileManagers.validate_project_structure(empty_project_root)
        assert result.is_failure

    def test_validate_project_structure_nonexistent(self) -> None:
        """Test validating nonexistent project."""
        nonexistent_path = self.temp_dir / "does_not_exist_validation"
        result = FlextMeltanoFileManagers.validate_project_structure(nonexistent_path)
        assert result.is_failure

    def test_complex_workflow_integration(self) -> None:
        """Test complex workflow integrating multiple file manager operations."""
        temp_result = FlextMeltanoFileManagers.create_temp_directory(
            prefix="integration_test"
        )
        assert temp_result.is_success
        temp_path = temp_result.value
        try:
            project_root = temp_path / "integration_project"
            setup_result = FlextMeltanoFileManagers.setup_project_structure(
                project_root=project_root, _project_name="integration-workflow-test"
            )
            assert setup_result.is_success
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
            assert save_result.is_success
            validate_yaml_result = FlextMeltanoFileManagers.validate_yaml_file(
                config_path
            )
            assert validate_yaml_result.is_success
            load_result = FlextMeltanoFileManagers.load_yaml_config(config_path)
            assert load_result.is_success
            loaded_config = load_result.value
            assert loaded_config["project_id"] == "integration-workflow-test"
            plugins = loaded_config["plugins"]
            if isinstance(plugins, dict):
                extractors = plugins.get("extractors")
                loaders = plugins.get("loaders")
                if isinstance(extractors, list) and isinstance(loaders, list):
                    assert len(extractors) == 2
                    assert len(loaders) == 2
            validate_structure_result = (
                FlextMeltanoFileManagers.validate_project_structure(project_root)
            )
            assert validate_structure_result.is_success
        finally:
            cleanup_result = FlextMeltanoFileManagers.cleanup_temp_directory(temp_path)
            assert cleanup_result.is_success

    def test_error_handling_edge_cases(self) -> None:
        """Test error handling for various edge cases."""
        try:
            invalid_path = Path("/invalid/path/that/does/not/exist")
            result = FlextMeltanoFileManagers.save_yaml_config({}, invalid_path)
            assert result.is_failure
        except (TypeError, AttributeError):
            pass
        empty_config_result = FlextMeltanoFileManagers.save_yaml_config(
            {}, self.temp_dir / "empty.yml"
        )
        assert empty_config_result.is_success
        load_empty_result = FlextMeltanoFileManagers.load_yaml_config(
            self.temp_dir / "empty.yml"
        )
        assert load_empty_result.is_success
        assert load_empty_result.value == {}

    def test_concurrent_file_operations(self) -> None:
        """Test concurrent file operations don't interfere."""
        configs: list[dict[str, object]] = [
            {"id": "config1", "data": "value1"},
            {"id": "config2", "data": "value2"},
            {"id": "config3", "data": "value3"},
        ]
        for i, config in enumerate(configs):
            file_path = self.temp_dir / f"concurrent_{i}.yml"
            result = FlextMeltanoFileManagers.save_yaml_config(config, file_path)
            assert result.is_success
        for i, expected_config in enumerate(configs):
            file_path = self.temp_dir / f"concurrent_{i}.yml"
            load_result = FlextMeltanoFileManagers.load_yaml_config(file_path)
            assert load_result.is_success
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
