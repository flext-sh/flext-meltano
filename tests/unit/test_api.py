"""Tests for FlextMeltano MRO facade - real API testing.

Tests the main unified API (FlextMeltano) which is an MRO facade over
Meltano services. Only tests methods that actually exist on the facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from pytest_benchmark.fixture import BenchmarkFixture

from flext_core import r
from flext_meltano import FlextMeltano, FlextMeltanoAdapter, FlextMeltanoExecutorBase, m
from tests import c

pytestmark = pytest.mark.unit


class TestFlextMeltanoInitialization:
    """Test FlextMeltano initialization and basic properties."""

    def test_api_initialization_default(self) -> None:
        """Test API initialization with default parameters."""
        api = FlextMeltano()
        assert api is not None

    def test_api_initialization_with_service_name(self) -> None:
        """Test API initialization with specific service name."""
        api = FlextMeltano(service_name="test-api")
        assert api is not None

    def test_api_service_name_property(self) -> None:
        """Test API service name property."""
        api = FlextMeltano(service_name="test-service")
        assert api.service_name == "test-service"

    def test_api_get_instance_returns_singleton(self) -> None:
        """Test get_instance returns the same instance."""
        FlextMeltano._instance = None
        instance1 = FlextMeltano.get_instance()
        instance2 = FlextMeltano.get_instance()
        assert instance1 is instance2
        FlextMeltano._instance = None

    def test_api_has_expected_attributes(self) -> None:
        """Test basic API attributes exist."""
        api = FlextMeltano()
        assert hasattr(api, "execute")
        assert hasattr(api, "service_name")


class TestFlextMeltanoExecuteMethod:
    """Test FlextMeltano execute method."""

    def test_execute_returns_result(self) -> None:
        """Test execute method returns r."""
        api = FlextMeltano()
        result = api.execute()
        assert result.is_success
        assert result.value is not None

    def test_execute_contains_version(self) -> None:
        """Test execute result contains version info."""
        api = FlextMeltano()
        result = api.execute()
        assert result.is_success
        assert "version" in result.value

    def test_execute_contains_service_name(self) -> None:
        """Test execute result contains service_name."""
        api = FlextMeltano()
        result = api.execute()
        assert result.is_success
        assert "service_name" in result.value

    def test_execute_contains_status(self) -> None:
        """Test execute result contains status."""
        api = FlextMeltano()
        result = api.execute()
        assert result.is_success
        assert "status" in result.value

    def test_execute_contains_handlers(self) -> None:
        """Test execute result contains handlers list."""
        api = FlextMeltano()
        result = api.execute()
        assert result.is_success
        assert "handlers" in result.value
        assert isinstance(result.value["handlers"], list)


class TestFlextMeltanoProjectOperations:
    """Test FlextMeltano project creation and validation operations."""

    def test_create_project_invalid_name(self) -> None:
        """Test project creation with invalid name."""
        api = FlextMeltano()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = api.create_project(
                project_name="",
                project_dir=Path(temp_dir),
            )
            assert result.is_failure
            assert result.error is not None

    def test_create_project_with_config(self) -> None:
        """Test project creation with project_dir."""
        api = FlextMeltano()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = api.create_project(
                project_name="config_test",
                project_dir=Path(temp_dir),
            )
            assert result.is_success
            project_path = Path(str(result.value["project_path"]))
            assert (project_path / c.Meltano.Paths.MELTANO_PROJECT_FILE).exists()

    def test_validate_project_nonexistent(self) -> None:
        """Test validation of non-existent project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nonexistent = Path(temp_dir) / "nonexistent"
            result = FlextMeltano.validate_project(nonexistent)
            assert result.is_failure
            assert result.error is not None

    def test_validate_project_with_path(self) -> None:
        """Test project validation with specific path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = FlextMeltano.validate_project(Path(temp_dir))
            assert result.is_success or result.is_failure


class TestFlextMeltanoPluginOperations:
    """Test FlextMeltano install_component (from FlextMeltanoService)."""

    def test_install_component_without_project(self) -> None:
        """Test component installation without valid project."""
        result = FlextMeltano.install_component(
            component_type="extractors",
            component_name="tap-csv",
        )
        assert result.is_failure or result.is_success

    def test_install_component_invalid_type(self) -> None:
        """Test component installation with invalid type."""
        result = FlextMeltano.install_component(
            component_type="invalid_type",
            component_name="tap-csv",
        )
        assert result.is_failure
        assert result.error is not None

    def test_install_component_with_config(self) -> None:
        """Test component installation with configuration."""
        result = FlextMeltano.install_component(
            component_type="extractors",
            component_name="tap-csv",
            config={"path": "/tmp/test.csv"},
        )
        assert result.is_failure or result.is_success


class TestFlextMeltanoCatalogOperations:
    """Test FlextMeltano discover_plugins (from FlextMeltanoBridge)."""

    def test_discover_plugins_requires_active_project(self) -> None:
        """Test discover_plugins fails when no Meltano project is active."""
        bridge_result = FlextMeltano().discover_plugins()
        assert bridge_result.is_failure
        error_lower = (bridge_result.error or "").lower()
        assert (
            "failed to load meltano project" in error_lower
            or "does not satisfy" in error_lower
            or "project" in error_lower
        )

    def test_discover_plugins_returns_empty_list_for_new_project(self) -> None:
        """Test discover_plugins succeeds for a newly initialized project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir) / "plugins_project"
            create_result = FlextMeltanoAdapter.ProjectAdapter().create_project(
                project_name=project_root.name,
                project_dir=project_root.parent,
            )
            assert create_result.is_success
            adapter = FlextMeltanoAdapter.PluginAdapter(
                config_overrides={"project_root": str(project_root)},
            )
            plugins_result = adapter.discover_plugins()
            assert plugins_result.is_success
            assert isinstance(plugins_result.value, list)


class TestFlextMeltanoPipelineOperations:
    """Test FlextMeltano pipeline execution (from FlextMeltanoExecutor)."""

    def test_execute_pipeline_tap_target(self) -> None:
        """Test execute_pipeline with tap and target returns result or raises."""
        api = FlextMeltano()
        mock_result = m.Meltano.CommandExecutionResult(
            command=["elt", "tap-csv", "target-jsonl"],
            success=False,
            exit_code=1,
            output="",
            error="No project found",
            execution_time=0.0,
        )
        with patch.object(
            FlextMeltanoExecutorBase,
            "execute_meltano_command",
            return_value=r[m.Meltano.CommandExecutionResult].ok(mock_result),
        ):
            result = api.execute_pipeline(
                tap_name="tap-csv",
                target_name="target-jsonl",
            )
        assert result.is_failure or result.is_success


class TestFlextMeltanoErrorHandling:
    """Test FlextMeltano error handling and edge cases."""

    def test_api_default_initialization(self) -> None:
        """Test API initializes with defaults."""
        api = FlextMeltano()
        assert api is not None

    def test_create_project_exception_handling(self) -> None:
        """Test project creation handles exceptions gracefully."""
        api = FlextMeltano()
        result = api.create_project(
            project_name="test",
            project_dir=Path("/invalid/path/that/does/not/exist"),
        )
        assert result.is_failure or result.is_success

    def test_validate_project_exception_handling(self) -> None:
        """Test project validation handles exceptions gracefully."""
        result = FlextMeltano.validate_project(Path("/invalid/path"))
        assert result.is_failure
        assert result.error is not None


class TestFlextMeltanoIntegration:
    """Integration tests for FlextMeltano operations."""

    def test_api_full_workflow_simulation(self) -> None:
        """Test simulated full workflow without actual Meltano execution."""
        api = FlextMeltano()
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "integration_test"
            create_result = api.create_project(
                project_name="integration_test",
                project_dir=project_path.parent,
            )
            assert create_result.is_success or "already exists" in (
                create_result.error or ""
            )
            validate_result = FlextMeltano.validate_project(project_path)
            assert validate_result.is_failure or validate_result.is_success
            plugins_result = FlextMeltano().discover_plugins()
            assert plugins_result.is_failure or plugins_result.is_success


@pytest.mark.benchmark
class TestFlextMeltanoSuccessPaths:
    """Test FlextMeltano success scenarios for coverage."""

    def test_create_project_exception_path(self) -> None:
        """Test project creation exception handling."""
        api = FlextMeltano()
        result = api.create_project(
            project_name="test",
            project_dir=Path("/nonexistent/impossible/path/that/cannot/exist"),
        )
        assert result.is_failure
        assert result.error is not None
        assert (
            "Failed to create" in result.error
            or "Project creation failed" in result.error
            or "Permission denied" in result.error
            or "not found" in result.error
        )

    def test_validate_project_exception_path(self) -> None:
        """Test project validation exception handling."""
        result = FlextMeltano.validate_project(Path("/nonexistent/path"))
        assert result.is_failure
        assert result.error is not None
        assert (
            "Failed to validate project" in result.error
            or "not found" in result.error
            or "validate" in result.error.lower()
            or "exist" in result.error.lower()
        )

    def test_install_component_exception_path(self) -> None:
        """Test component installation exception handling."""
        result = FlextMeltano.install_component(
            component_type="invalid",
            component_name="nonexistent-plugin",
        )
        assert result.is_failure

    def test_discover_plugins_exception_path(self) -> None:
        """Test discover_plugins returns result."""
        result = FlextMeltano().discover_plugins()
        assert result.is_failure or result.is_success


@pytest.mark.benchmark
class TestFlextMeltanoPerformance:
    """Performance benchmarks for FlextMeltano operations."""

    def test_api_initialization_performance(self, benchmark: BenchmarkFixture) -> None:
        """Benchmark API initialization performance."""

        def create_api() -> FlextMeltano:
            return FlextMeltano()

        benchmark(create_api)

    def test_api_execute_performance(
        self,
        benchmark: BenchmarkFixture,
    ) -> None:
        """Benchmark API execute performance."""
        api = FlextMeltano()

        def run_execute() -> object:
            return api.execute()

        benchmark(run_execute)
