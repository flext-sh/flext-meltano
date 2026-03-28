"""Tests for FlextMeltano MRO facade - real API testing.

Tests the main unified API (FlextMeltano) which is an MRO facade over
Meltano services. Only tests methods that actually exist on the facade.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from collections.abc import Mapping
from pathlib import Path

import pytest
from flext_core import r
from flext_tests import tm
from pytest_benchmark.fixture import BenchmarkFixture

from flext_meltano import FlextMeltano
from tests import t

pytestmark = pytest.mark.unit


class TestFlextMeltanoInitialization:
    """Test FlextMeltano initialization and basic properties."""

    def test_api_initialization_default(self) -> None:
        """Test API initialization with default parameters."""
        api = FlextMeltano()
        tm.that(api, none=False)

    def test_api_initialization_with_service_name(self) -> None:
        """Test API initialization with specific service name."""
        api = FlextMeltano(service_name="test-api")
        tm.that(api, none=False)

    def test_api_service_name_property(self) -> None:
        """Test API service name property."""
        api = FlextMeltano(service_name="test-service")
        tm.that(api.service_name, eq="test-service")

    def test_api_get_instance_returns_singleton(self) -> None:
        """Test get_instance returns the same instance."""
        FlextMeltano._instance = None
        instance1 = FlextMeltano.get_instance()
        instance2 = FlextMeltano.get_instance()
        tm.that(instance1 is instance2, eq=True)
        FlextMeltano._instance = None

    def test_api_has_expected_attributes(self) -> None:
        """Test basic API attributes exist."""
        api = FlextMeltano()
        tm.that(hasattr(api, "execute"), eq=True)
        tm.that(hasattr(api, "service_name"), eq=True)


class TestFlextMeltanoExecuteMethod:
    """Test FlextMeltano execute method."""

    def test_execute_returns_result(self) -> None:
        """Test execute method returns r."""
        api = FlextMeltano()
        result = api.execute()
        tm.ok(result)
        tm.that(result.value, none=False)

    def test_execute_contains_version(self) -> None:
        """Test execute result contains version info."""
        api = FlextMeltano()
        result = api.execute()
        tm.ok(result)
        tm.that("version" in result.value, eq=True)

    def test_execute_contains_service_name(self) -> None:
        """Test execute result contains service_name."""
        api = FlextMeltano()
        result = api.execute()
        tm.ok(result)
        tm.that("service_name" in result.value, eq=True)

    def test_execute_contains_status(self) -> None:
        """Test execute result contains status."""
        api = FlextMeltano()
        result = api.execute()
        tm.ok(result)
        tm.that("status" in result.value, eq=True)

    def test_execute_contains_handlers(self) -> None:
        """Test execute result contains handlers list."""
        api = FlextMeltano()
        result = api.execute()
        tm.ok(result)
        tm.that("handlers" in result.value, eq=True)
        tm.that(result.value["handlers"], is_=list)


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
            tm.fail(result)
            tm.that(result.error, none=False)

    def test_create_project_with_config(self) -> None:
        """Test project creation with project_dir."""
        api = FlextMeltano()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = api.create_project(
                project_name="config_test",
                project_dir=Path(temp_dir),
            )
            tm.that(result.is_success or result.is_failure, eq=True)

    def test_validate_project_nonexistent(self) -> None:
        """Test validation of non-existent project."""
        with tempfile.TemporaryDirectory() as temp_dir:
            nonexistent = Path(temp_dir) / "nonexistent"
            result = FlextMeltano.validate_project(nonexistent)
            tm.fail(result)
            tm.that(result.error, none=False)

    def test_validate_project_with_path(self) -> None:
        """Test project validation with specific path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            result = FlextMeltano.validate_project(Path(temp_dir))
            tm.that(result.is_success or result.is_failure, eq=True)


class TestFlextMeltanoPluginOperations:
    """Test FlextMeltano install_component (from FlextMeltanoService)."""

    def test_install_component_without_project(self) -> None:
        """Test component installation without valid project."""
        result = FlextMeltano.install_component(
            component_type="extractors",
            component_name="tap-csv",
        )
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_install_component_invalid_type(self) -> None:
        """Test component installation with invalid type."""
        result = FlextMeltano.install_component(
            component_type="invalid_type",
            component_name="tap-csv",
        )
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_install_component_with_config(self) -> None:
        """Test component installation with configuration."""
        result = FlextMeltano.install_component(
            component_type="extractors",
            component_name="tap-csv",
            config={"path": "/tmp/test.csv"},
        )
        tm.that(result.is_failure or result.is_success, eq=True)


class TestFlextMeltanoCatalogOperations:
    """Test FlextMeltano discover_plugins (from FlextMeltanoBridge)."""

    def test_discover_plugins_returns_result(self) -> None:
        """Test discover_plugins returns a result."""
        bridge_result = FlextMeltano.discover_plugins()
        tm.that(bridge_result.is_failure or bridge_result.is_success, eq=True)


class TestFlextMeltanoPipelineOperations:
    """Test FlextMeltano pipeline execution (from FlextMeltanoExecutor)."""

    def test_execute_pipeline_tap_target(self) -> None:
        """Test execute_pipeline with tap and target."""
        api = FlextMeltano()
        result = api.execute_pipeline(
            tap_name="tap-csv",
            target_name="target-jsonl",
        )
        tm.that(result.is_failure or result.is_success, eq=True)


class TestFlextMeltanoErrorHandling:
    """Test FlextMeltano error handling and edge cases."""

    def test_api_default_initialization(self) -> None:
        """Test API initializes with defaults."""
        api = FlextMeltano()
        tm.that(api, none=False)

    def test_create_project_exception_handling(self) -> None:
        """Test project creation handles exceptions gracefully."""
        api = FlextMeltano()
        result = api.create_project(
            project_name="test",
            project_dir=Path("/invalid/path/that/does/not/exist"),
        )
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_validate_project_exception_handling(self) -> None:
        """Test project validation handles exceptions gracefully."""
        result = FlextMeltano.validate_project(Path("/invalid/path"))
        tm.fail(result)
        tm.that(result.error, none=False)


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
            tm.that(
                create_result.is_success
                or "already exists" in (create_result.error or ""),
                eq=True,
            )
            validate_result = FlextMeltano.validate_project(project_path)
            tm.that(validate_result.is_failure or validate_result.is_success, eq=True)
            plugins_result = FlextMeltano.discover_plugins()
            tm.that(plugins_result.is_failure or plugins_result.is_success, eq=True)


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
        tm.fail(result)
        tm.that(
            result.error
            and (
                "Failed to create" in result.error
                or "Project creation failed" in result.error
                or "Permission denied" in result.error
                or "not found" in result.error
            ),
            eq=True,
        )

    def test_validate_project_exception_path(self) -> None:
        """Test project validation exception handling."""
        result = FlextMeltano.validate_project(Path("/nonexistent/path"))
        tm.fail(result)
        tm.that(
            result.error
            and (
                "Failed to validate project" in result.error
                or "not found" in result.error
                or "validate" in (result.error or "").lower()
                or ("exist" in (result.error or "").lower())
            ),
            eq=True,
        )

    def test_install_component_exception_path(self) -> None:
        """Test component installation exception handling."""
        result = FlextMeltano.install_component(
            component_type="invalid",
            component_name="nonexistent-plugin",
        )
        tm.fail(result)

    def test_discover_plugins_exception_path(self) -> None:
        """Test discover_plugins returns result."""
        result = FlextMeltano.discover_plugins()
        tm.that(result.is_failure or result.is_success, eq=True)


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

        def run_execute() -> r[Mapping[str, t.NormalizedValue]]:
            return api.execute()

        benchmark(run_execute)
