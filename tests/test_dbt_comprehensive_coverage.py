"""Comprehensive Coverage Tests for DBT Module.

**Purpose**: Test all classes and methods in dbt.py to achieve 100% coverage
**Scope**: FlextMeltanoDbtManager, FlextMeltanoDbtProject, FlextMeltanoDbtRunner
**Target**: Increase dbt.py coverage from 0% to 100%

This module provides complete functional tests for all DBT classes and methods
to ensure maximum coverage with comprehensive functionality testing.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from flext_meltano.dbt import (
    FlextMeltanoDbtManager,
    FlextMeltanoDbtProject,
    FlextMeltanoDbtRunner,
    __all__ as _dbt_all,
)


class TestFlextMeltanoDbtManagerComplete:
    """Complete tests for FlextMeltanoDbtManager."""

    def test_dbt_manager_initialization_default(self) -> None:
        """Test DBT manager initialization with default parameters."""
        manager = FlextMeltanoDbtManager()

        assert manager is not None
        assert isinstance(manager.project_dir, Path)
        assert manager.project_dir == Path.cwd()

    def test_dbt_manager_initialization_with_path_string(self) -> None:
        """Test DBT manager initialization with string path."""
        with tempfile.TemporaryDirectory() as test_path:
            manager = FlextMeltanoDbtManager(test_path)
            assert manager.project_dir == Path(test_path)

    def test_dbt_manager_initialization_with_path_object(self) -> None:
        """Test DBT manager initialization with Path object."""
        with tempfile.TemporaryDirectory() as temp_str:
            test_path = Path(temp_str)
            manager = FlextMeltanoDbtManager(test_path)
            assert manager.project_dir == test_path

    def test_dbt_manager_initialization_with_none(self) -> None:
        """Test DBT manager initialization with None."""
        manager = FlextMeltanoDbtManager(None)

        assert manager.project_dir == Path.cwd()

    def test_dbt_manager_run_models_no_arguments(self) -> None:
        """Test DBT manager run models without arguments."""
        manager = FlextMeltanoDbtManager()

        result = manager.run_models()

        assert result.success
        assert result.data is not None
        assert result.data["models"] == []
        assert result.data["status"] == "success"

    def test_dbt_manager_run_models_with_models_list(self) -> None:
        """Test DBT manager run models with models list."""
        manager = FlextMeltanoDbtManager()
        test_models = ["model1", "model2", "model3"]

        result = manager.run_models(test_models)

        assert result.success
        assert result.data is not None
        assert result.data["models"] == test_models
        assert result.data["status"] == "success"

    def test_dbt_manager_run_models_with_empty_list(self) -> None:
        """Test DBT manager run models with empty list."""
        manager = FlextMeltanoDbtManager()

        result = manager.run_models([])

        assert result.success
        assert result.data is not None
        assert result.data["models"] == []
        assert result.data["status"] == "success"

    def test_dbt_manager_test_models_no_arguments(self) -> None:
        """Test DBT manager test models without arguments."""
        manager = FlextMeltanoDbtManager()

        result = manager.test_models()

        assert result.success
        assert result.data is not None
        assert result.data["models"] == []
        assert result.data["status"] == "success"

    def test_dbt_manager_test_models_with_models_list(self) -> None:
        """Test DBT manager test models with models list."""
        manager = FlextMeltanoDbtManager()
        test_models = ["test_model1", "test_model2"]

        result = manager.test_models(test_models)

        assert result.success
        assert result.data is not None
        assert result.data["models"] == test_models
        assert result.data["status"] == "success"

    def test_dbt_manager_test_models_with_empty_list(self) -> None:
        """Test DBT manager test models with empty list."""
        manager = FlextMeltanoDbtManager()

        result = manager.test_models([])

        assert result.success
        assert result.data is not None
        assert result.data["models"] == []
        assert result.data["status"] == "success"

    def test_dbt_manager_compile_models_no_arguments(self) -> None:
        """Test DBT manager compile models without arguments."""
        manager = FlextMeltanoDbtManager()

        result = manager.compile_models()

        assert result.success
        assert result.data is not None
        assert result.data["models"] == []
        assert result.data["status"] == "success"

    def test_dbt_manager_compile_models_with_models_list(self) -> None:
        """Test DBT manager compile models with models list."""
        manager = FlextMeltanoDbtManager()
        test_models = ["staging_users", "marts_customers"]

        result = manager.compile_models(test_models)

        assert result.success
        assert result.data is not None
        assert result.data["models"] == test_models
        assert result.data["status"] == "success"

    def test_dbt_manager_compile_models_with_empty_list(self) -> None:
        """Test DBT manager compile models with empty list."""
        manager = FlextMeltanoDbtManager()

        result = manager.compile_models([])

        assert result.success
        assert result.data is not None
        assert result.data["models"] == []
        assert result.data["status"] == "success"


class TestFlextMeltanoDbtProjectComplete:
    """Complete tests for FlextMeltanoDbtProject."""

    def test_dbt_project_initialization_default(self) -> None:
        """Test DBT project initialization with default parameters."""
        project = FlextMeltanoDbtProject()

        assert project is not None
        assert isinstance(project.project_dir, Path)
        assert project.project_dir == Path.cwd()

    def test_dbt_project_initialization_with_path_string(self) -> None:
        """Test DBT project initialization with string path."""
        with tempfile.TemporaryDirectory() as test_path:
            project = FlextMeltanoDbtProject(test_path)
            assert project.project_dir == Path(test_path)

    def test_dbt_project_initialization_with_path_object(self) -> None:
        """Test DBT project initialization with Path object."""
        with tempfile.TemporaryDirectory() as temp_str:
            test_path = Path(temp_str)
            project = FlextMeltanoDbtProject(test_path)
            assert project.project_dir == test_path

    def test_dbt_project_initialization_with_none(self) -> None:
        """Test DBT project initialization with None."""
        project = FlextMeltanoDbtProject(None)

        assert project.project_dir == Path.cwd()

    def test_dbt_project_initialize(self) -> None:
        """Test DBT project initialize method."""
        project = FlextMeltanoDbtProject()

        result = project.initialize()

        assert result.success
        assert result.data is None
        assert result.error is None

    def test_dbt_project_validate(self) -> None:
        """Test DBT project validate method."""
        project = FlextMeltanoDbtProject()

        result = project.validate()

        assert result.success
        assert result.data is None
        assert result.error is None


class TestFlextMeltanoDbtRunnerComplete:
    """Complete tests for FlextMeltanoDbtRunner."""

    def test_dbt_runner_initialization_default(self) -> None:
        """Test DBT runner initialization with default parameters."""
        runner = FlextMeltanoDbtRunner()

        assert runner is not None
        assert isinstance(runner.project_dir, Path)
        assert runner.project_dir == Path.cwd()

    def test_dbt_runner_initialization_with_path_string(self) -> None:
        """Test DBT runner initialization with string path."""
        with tempfile.TemporaryDirectory() as test_path:
            runner = FlextMeltanoDbtRunner(test_path)
            assert runner.project_dir == Path(test_path)

    def test_dbt_runner_initialization_with_path_object(self) -> None:
        """Test DBT runner initialization with Path object."""
        with tempfile.TemporaryDirectory() as temp_str:
            test_path = Path(temp_str)
            runner = FlextMeltanoDbtRunner(test_path)
            assert runner.project_dir == test_path

    def test_dbt_runner_initialization_with_none(self) -> None:
        """Test DBT runner initialization with None."""
        runner = FlextMeltanoDbtRunner(None)

        assert runner.project_dir == Path.cwd()

    def test_dbt_runner_run_basic_command(self) -> None:
        """Test DBT runner run method with basic command."""
        runner = FlextMeltanoDbtRunner()

        result = runner.run("compile")

        assert result.success
        assert result.data is not None
        assert result.data["command"] == "compile"
        assert result.data["args"] == []
        assert result.data["status"] == "success"

    def test_dbt_runner_run_command_with_args(self) -> None:
        """Test DBT runner run method with command and arguments."""
        runner = FlextMeltanoDbtRunner()
        test_args = ["--models", "staging", "--vars", "env:dev"]

        result = runner.run("run", test_args)

        assert result.success
        assert result.data is not None
        assert result.data["command"] == "run"
        assert result.data["args"] == test_args
        assert result.data["status"] == "success"

    def test_dbt_runner_run_command_with_none_args(self) -> None:
        """Test DBT runner run method with None arguments."""
        runner = FlextMeltanoDbtRunner()

        result = runner.run("test", None)

        assert result.success
        assert result.data is not None
        assert result.data["command"] == "test"
        assert result.data["args"] == []
        assert result.data["status"] == "success"

    def test_dbt_runner_run_command_with_empty_args(self) -> None:
        """Test DBT runner run method with empty arguments list."""
        runner = FlextMeltanoDbtRunner()

        result = runner.run("docs", [])

        assert result.success
        assert result.data is not None
        assert result.data["command"] == "docs"
        assert result.data["args"] == []
        assert result.data["status"] == "success"

    def test_dbt_runner_run_models_no_arguments(self) -> None:
        """Test DBT runner run models without arguments."""
        runner = FlextMeltanoDbtRunner()

        result = runner.run_models()

        assert result.success
        assert result.data is not None
        assert result.data["models"] == []
        assert result.data["status"] == "success"

    def test_dbt_runner_run_models_with_models_list(self) -> None:
        """Test DBT runner run models with models list."""
        runner = FlextMeltanoDbtRunner()
        test_models = ["dim_customers", "fact_orders"]

        result = runner.run_models(test_models)

        assert result.success
        assert result.data is not None
        assert result.data["models"] == test_models
        assert result.data["status"] == "success"

    def test_dbt_runner_run_models_with_empty_list(self) -> None:
        """Test DBT runner run models with empty list."""
        runner = FlextMeltanoDbtRunner()

        result = runner.run_models([])

        assert result.success
        assert result.data is not None
        assert result.data["models"] == []
        assert result.data["status"] == "success"

    def test_dbt_runner_test_models_no_arguments(self) -> None:
        """Test DBT runner test models without arguments."""
        runner = FlextMeltanoDbtRunner()

        result = runner.test_models()

        assert result.success
        assert result.data is not None
        assert result.data["models"] == []
        assert result.data["status"] == "success"

    def test_dbt_runner_test_models_with_models_list(self) -> None:
        """Test DBT runner test models with models list."""
        runner = FlextMeltanoDbtRunner()
        test_models = ["test_dim_customers_not_null", "test_fact_orders_unique"]

        result = runner.test_models(test_models)

        assert result.success
        assert result.data is not None
        assert result.data["models"] == test_models
        assert result.data["status"] == "success"

    def test_dbt_runner_test_models_with_empty_list(self) -> None:
        """Test DBT runner test models with empty list."""
        runner = FlextMeltanoDbtRunner()

        result = runner.test_models([])

        assert result.success
        assert result.data is not None
        assert result.data["models"] == []
        assert result.data["status"] == "success"


class TestDbtModuleIntegration:
    """Integration tests for DBT module classes."""

    def test_all_classes_can_be_instantiated(self) -> None:
        """Test that all DBT classes can be instantiated."""
        manager = FlextMeltanoDbtManager()
        project = FlextMeltanoDbtProject()
        runner = FlextMeltanoDbtRunner()

        assert manager is not None
        assert project is not None
        assert runner is not None

    def test_all_classes_with_same_project_dir(self) -> None:
        """Test all classes with the same project directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir)

            manager = FlextMeltanoDbtManager(project_path)
            project = FlextMeltanoDbtProject(project_path)
            runner = FlextMeltanoDbtRunner(project_path)

            assert manager.project_dir == project_path
            assert project.project_dir == project_path
            assert runner.project_dir == project_path

    def test_workflow_integration_simulation(self) -> None:
        """Test simulated workflow integration between classes."""
        # Simulate a complete DBT workflow
        project = FlextMeltanoDbtProject()
        manager = FlextMeltanoDbtManager()
        runner = FlextMeltanoDbtRunner()

        # Initialize project
        init_result = project.initialize()
        assert init_result.success

        # Validate project
        validate_result = project.validate()
        assert validate_result.success

        # Compile models via manager
        compile_result = manager.compile_models(["staging_users"])
        assert compile_result.success

        # Run models via runner
        run_result = runner.run_models(["staging_users"])
        assert run_result.success

        # Test models via manager
        test_result = manager.test_models(["staging_users"])
        assert test_result.success

    def test_module_exports(self) -> None:
        """Test that module exports are correctly defined."""
        expected_exports = [
            "FlextMeltanoDbtManager",
            "FlextMeltanoDbtProject",
            "FlextMeltanoDbtRunner",
        ]

        assert isinstance(_dbt_all, list)
        assert len(_dbt_all) == 3
        for export in expected_exports:
            assert export in _dbt_all

    def test_all_methods_return_flext_result(self) -> None:
        """Test that all methods return FlextResult objects."""
        manager = FlextMeltanoDbtManager()
        project = FlextMeltanoDbtProject()
        runner = FlextMeltanoDbtRunner()

        # Test all manager methods
        assert hasattr(manager.run_models(), "success")
        assert hasattr(manager.test_models(), "success")
        assert hasattr(manager.compile_models(), "success")

        # Test all project methods
        assert hasattr(project.initialize(), "success")
        assert hasattr(project.validate(), "success")

        # Test all runner methods
        assert hasattr(runner.run("compile"), "success")
        assert hasattr(runner.run_models(), "success")
        assert hasattr(runner.test_models(), "success")
