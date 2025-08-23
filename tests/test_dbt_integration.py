"""DBT Integration Comprehensive Test Suite - Data Transformation Layer Validation.

**Test Category**: Integration Tests
**Coverage Target**: 95%+ for DBT integration components
**Dependencies**: DBT Core, flext-core patterns, temporary project directories
**Execution Time**: < 15 seconds total

## Test Scope

Validates the DBT integration components that provide **data transformation capabilities**
for FLEXT Meltano's bridge architecture, focusing on DBT project management, model
execution, and enterprise patterns for data transformation workflows.

## Test Coverage Areas

1. **DBT Project Management**: DBT project lifecycle and configuration
2. **Model Execution**: DBT run, test, and compile operations
3. **Integration Patterns**: DBT service creation and configuration management
4. **Enterprise Patterns**: FlextResult integration and error handling
5. **Bridge Integration**: DBT operations accessible via Go service bridge

## Architecture Alignment

Tests align with FLEXT Meltano's DBT integration architecture:
- **Data Transformation**: DBT-based data transformation with enterprise patterns
- **Project Management**: DBT project lifecycle with proper configuration
- **Service Integration**: DBT services integrated with FLEXT service patterns
- **Bridge Communication**: DBT operations designed for Go service consumption
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from flext_meltano import (
    FlextMeltanoConfig,
    FlextMeltanoDbtManager,
    FlextMeltanoDbtRunner,
    FlextMeltanoDbtService,
)

# Use the real service class, not the stub
FlextMeltanoDbtProject = FlextMeltanoDbtService


class TestFlextMeltanoDbtManager:
    """Test DBT Manager functionality."""

    def test_manager_initialization(self) -> None:
        """Test DBT manager initialization."""
        manager = FlextMeltanoDbtManager()
        if manager.project_dir != Path.cwd():
            msg: str = f"Expected {Path.cwd()}, got {manager.project_dir}"
            raise AssertionError(msg)

    def test_manager_initialization_with_path(self) -> None:
        """Test DBT manager initialization with specific path."""
        project_dir = Path("/test/project")
        manager = FlextMeltanoDbtManager(project_dir=project_dir)
        if manager.project_dir != project_dir:
            msg: str = f"Expected {project_dir}, got {manager.project_dir}"
            raise AssertionError(msg)

    def test_manager_initialization_with_string_path(self) -> None:
        """Test DBT manager initialization with string path."""
        project_dir_str = "/test/project"
        manager = FlextMeltanoDbtManager(project_dir=project_dir_str)
        if manager.project_dir != Path(project_dir_str):
            msg: str = f"Expected {Path(project_dir_str)}, got {manager.project_dir}"
            raise AssertionError(msg)

    def test_run_models_default(self) -> None:
        """Test run models with default parameters."""
        manager = FlextMeltanoDbtManager()

        result = manager.run_models()
        assert result.success
        assert result.value is not None
        if result.value["models"] != []:
            msg: str = f"Expected {[]}, got {result.value['models']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["status"] != "success":
            msg: str = f"Expected {'success'}, got {result.value['status']}"
            raise AssertionError(msg)

    def test_run_models_with_specific_models(self) -> None:
        """Test run models with specific model list."""
        manager = FlextMeltanoDbtManager()
        models = ["model1", "model2", "model3"]

        result = manager.run_models(models=models)
        assert result.success
        assert result.value is not None
        if result.value["models"] != models:
            msg: str = f"Expected {models}, got {result.value['models']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["status"] != "success":
            msg: str = f"Expected {'success'}, got {result.value['status']}"
            raise AssertionError(msg)

    def test_test_models_default(self) -> None:
        """Test test models with default parameters."""
        manager = FlextMeltanoDbtManager()

        result = manager.test_models()
        assert result.success
        assert result.value is not None
        if result.value["models"] != []:
            msg: str = f"Expected {[]}, got {result.value['models']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["status"] != "success":
            msg: str = f"Expected {'success'}, got {result.value['status']}"
            raise AssertionError(msg)

    def test_test_models_with_specific_models(self) -> None:
        """Test test models with specific model list."""
        manager = FlextMeltanoDbtManager()
        models = ["test1", "test2"]

        result = manager.test_models(models=models)
        assert result.success
        assert result.value is not None
        if result.value["models"] != models:
            msg: str = f"Expected {models}, got {result.value['models']}"
            raise AssertionError(msg)

    def test_compile_models_default(self) -> None:
        """Test compile models with default parameters."""
        manager = FlextMeltanoDbtManager()

        result = manager.compile_models()
        assert result.success
        assert result.value is not None
        if result.value["models"] != []:
            msg: str = f"Expected {[]}, got {result.value['models']}"
            raise AssertionError(msg)

    def test_compile_models_with_specific_models(self) -> None:
        """Test compile models with specific model list."""
        manager = FlextMeltanoDbtManager()
        models = ["compile_model1", "compile_model2"]

        result = manager.compile_models(models=models)
        assert result.success
        assert result.value is not None
        if result.value["models"] != models:
            msg: str = f"Expected {models}, got {result.value['models']}"
            raise AssertionError(msg)


class TestFlextMeltanoDbtProject:
    """Test DBT Project functionality."""

    def test_project_initialization(self) -> None:
        """Test DBT project initialization."""
        config = FlextMeltanoConfig()  # Uses default project root
        project = FlextMeltanoDbtProject(config)
        # Since dbt_project_dir is None by default, project_dir will be None
        assert project.project_dir is None

    def test_project_initialization_with_path(self) -> None:
        """Test DBT project initialization with specific path."""
        project_dir_str = "/test/dbt/project"
        config = FlextMeltanoConfig(dbt_project_dir=project_dir_str)
        project = FlextMeltanoDbtProject(config)
        if project.project_dir != Path(project_dir_str):
            msg: str = f"Expected {Path(project_dir_str)}, got {project.project_dir}"
            raise AssertionError(msg)

    def test_project_initialization_with_string_path(self) -> None:
        """Test DBT project initialization with string path."""
        project_dir_str = "/test/dbt/project"
        config = FlextMeltanoConfig(dbt_project_dir=project_dir_str)
        project = FlextMeltanoDbtProject(config)
        if project.project_dir != Path(project_dir_str):
            msg: str = f"Expected {Path(project_dir_str)}, got {project.project_dir}"
            raise AssertionError(msg)

    def test_project_initialize(self) -> None:
        """Test project initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(dbt_project_dir=temp_dir)
            project = FlextMeltanoDbtProject(config)

            result = project.initialize()
            assert result.success
            assert (
                result.value is True
            )  # Changed from None to True based on implementation

    def test_project_validate(self) -> None:
        """Test project validation."""
        config = FlextMeltanoConfig(dbt_project_dir="/nonexistent/test_dbt")
        project = FlextMeltanoDbtProject(config)

        result = project.validate_service()
        # Should fail because directory doesn't exist
        assert not result.success
        assert result.error is not None
        assert result.error is not None
        assert result.error is not None
        if "DBT project directory not found" not in result.error:
            msg: str = f"Expected {'DBT project directory not found'} in {result.error}"
            raise AssertionError(msg)


class TestFlextMeltanoDbtRunner:
    """Test DBT Runner functionality."""

    def test_runner_initialization(self) -> None:
        """Test DBT runner initialization."""
        runner = FlextMeltanoDbtRunner()
        if runner.project_dir != Path.cwd():
            msg: str = f"Expected {Path.cwd()}, got {runner.project_dir}"
            raise AssertionError(msg)

    def test_runner_initialization_with_path(self) -> None:
        """Test DBT runner initialization with specific path."""
        project_dir = Path("/test/dbt/runner")
        runner = FlextMeltanoDbtRunner(project_dir=project_dir)
        if runner.project_dir != project_dir:
            msg: str = f"Expected {project_dir}, got {runner.project_dir}"
            raise AssertionError(msg)

    def test_runner_run_command(self) -> None:
        """Test runner run command."""
        runner = FlextMeltanoDbtRunner()

        result = runner.run("run", args=["--models", "test_model"])
        assert result.success
        assert result.value is not None
        if result.value["command"] != "run":
            msg: str = f"Expected {'run'}, got {result.value['command']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["args"] != ["--models", "test_model"]:
            msg: str = (
                f"Expected {['--models', 'test_model']}, got {result.value['args']}"
            )
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["status"] != "success":
            msg: str = f"Expected {'success'}, got {result.value['status']}"
            raise AssertionError(msg)

    def test_runner_run_command_no_args(self) -> None:
        """Test runner run command without arguments."""
        runner = FlextMeltanoDbtRunner()

        result = runner.run("test")
        assert result.success
        assert result.value is not None
        if result.value["command"] != "test":
            msg: str = f"Expected {'test'}, got {result.value['command']}"
            raise AssertionError(msg)
        assert result.value is not None
        if result.value["args"] != []:
            msg: str = f"Expected {[]}, got {result.value['args']}"
            raise AssertionError(msg)

    def test_runner_run_models(self) -> None:
        """Test runner run models."""
        runner = FlextMeltanoDbtRunner()
        models = ["model_a", "model_b"]

        result = runner.run_models(models=models)
        assert result.success
        assert result.value is not None
        if result.value["models"] != models:
            msg: str = f"Expected {models}, got {result.value['models']}"
            raise AssertionError(msg)

    def test_runner_run_models_default(self) -> None:
        """Test runner run models with default parameters."""
        runner = FlextMeltanoDbtRunner()

        result = runner.run_models()
        assert result.success
        assert result.value is not None
        if result.value["models"] != []:
            msg: str = f"Expected {[]}, got {result.value['models']}"
            raise AssertionError(msg)

    def test_runner_test_models(self) -> None:
        """Test runner test models."""
        runner = FlextMeltanoDbtRunner()
        models = ["test_a", "test_b"]

        result = runner.test_models(models=models)
        assert result.success
        assert result.value is not None
        if result.value["models"] != models:
            msg: str = f"Expected {models}, got {result.value['models']}"
            raise AssertionError(msg)

    def test_runner_test_models_default(self) -> None:
        """Test runner test models with default parameters."""
        runner = FlextMeltanoDbtRunner()

        result = runner.test_models()
        assert result.success
        assert result.value is not None
        if result.value["models"] != []:
            msg: str = f"Expected {[]}, got {result.value['models']}"
            raise AssertionError(msg)


class TestDBTIntegrationPatterns:
    """Test DBT integration patterns and common usage."""

    def test_manager_workflow(self) -> None:
        """Test typical manager workflow."""
        manager = FlextMeltanoDbtManager(project_dir="/dbt/project")

        # Typical workflow: compile -> run -> test
        compile_result = manager.compile_models(["staging.*"])
        assert compile_result.success

        run_result = manager.run_models(["staging.*"])
        assert run_result.success

        test_result = manager.test_models(["staging.*"])
        assert test_result.success

    def test_project_workflow(self) -> None:
        """Test typical project workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(dbt_project_dir=temp_dir)
            project = FlextMeltanoDbtProject(config)

            # Initialize and validate project
            init_result = project.initialize()
            assert init_result.success

            validate_result = project.validate_service()
            assert validate_result.success

    def test_runner_workflow(self) -> None:
        """Test typical runner workflow."""
        runner = FlextMeltanoDbtRunner("/dbt/project")

        # Run various DBT commands
        deps_result = runner.run("deps")
        assert deps_result.success

        seed_result = runner.run("seed")
        assert seed_result.success

        run_result = runner.run_models()
        assert run_result.success

        test_result = runner.test_models()
        assert test_result.success

    def test_integration_with_different_project_types(self) -> None:
        """Test integration with different project directory types."""
        # Test with None project dir
        manager1 = FlextMeltanoDbtManager(project_dir=None)
        if manager1.project_dir != Path.cwd():
            msg: str = f"Expected {Path.cwd()}, got {manager1.project_dir}"
            raise AssertionError(msg)

        # Test with Path object
        project_path = Path("/some/dbt/project")
        manager2 = FlextMeltanoDbtManager(project_dir=project_path)
        if manager2.project_dir != project_path:
            msg: str = f"Expected {project_path}, got {manager2.project_dir}"
            raise AssertionError(msg)

        # Test with string path
        project_str = "/another/dbt/project"
        manager3 = FlextMeltanoDbtManager(project_dir=project_str)
        if manager3.project_dir != Path(project_str):
            msg: str = f"Expected {Path(project_str)}, got {manager3.project_dir}"
            raise AssertionError(msg)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
