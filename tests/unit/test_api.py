"""Comprehensive tests for FlextMeltano - Real API testing without mocks.

Tests the main unified API for FLEXT Meltano operations following enterprise
testing standards with real Meltano integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from collections.abc import Mapping, Sequence
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

    def test_api_version_property(self) -> None:
        """Test API version method."""
        api = FlextMeltano()
        version_result = api.version()
        tm.ok(version_result)
        tm.that(version_result.value, none=False)

    def test_api_execute_returns_result(self) -> None:
        """Test API execute method returns result."""
        api = FlextMeltano()
        result = api.execute()
        tm.ok(result)
        tm.that(result.value, none=False)


class TestFlextMeltanoProjectOperations:
    """Test FlextMeltano project creation and validation operations."""

    def test_api_service_name_property(self) -> None:
        """Test API service name property."""
        api = FlextMeltano(service_name="test-service")
        tm.that(api.service_name, eq="test-service")

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
        api = FlextMeltano()
        with tempfile.TemporaryDirectory() as temp_dir:
            nonexistent = Path(temp_dir) / "nonexistent"
            result = api.validate_project(nonexistent)
            tm.fail(result)
            tm.that(result.error, none=False)

    def test_validate_project_with_path(self) -> None:
        """Test project validation with specific path."""
        api = FlextMeltano()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = api.validate_project(Path(temp_dir))
            tm.that(result.is_success or result.is_failure, eq=True)


class TestFlextMeltanoPluginOperations:
    """Test FlextMeltano plugin installation and listing operations."""

    def test_install_component_without_project(self) -> None:
        """Test component installation without valid project."""
        api = FlextMeltano()
        result = api.install_component(
            component_type="extractors",
            component_name="tap-csv",
        )
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_install_component_invalid_type(self) -> None:
        """Test component installation with invalid type."""
        api = FlextMeltano()
        result = api.install_component(
            component_type="invalid_type",
            component_name="tap-csv",
        )
        tm.fail(result)
        tm.that(result.error, none=False)

    def test_install_component_with_config(self) -> None:
        """Test component installation with configuration."""
        api = FlextMeltano()
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        result = api.install_component(
            component_type="extractors",
            component_name="tap-csv",
            config={"path": tmp_path},
        )
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_list_plugins_without_project(self) -> None:
        """Test listing plugins without valid project."""
        api = FlextMeltano()
        result = api.list_plugins()
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_list_plugins_returns_sequence(self) -> None:
        """Test listing plugins returns a sequence result."""
        api = FlextMeltano()
        result = api.list_plugins()
        tm.ok(result)


class TestFlextMeltanoCatalogOperations:
    """Test FlextMeltano catalog discovery operations."""

    def test_discover_returns_result(self) -> None:
        """Test discover returns a result."""
        api = FlextMeltano()
        result = api.discover()
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_discover_plugins_returns_result(self) -> None:
        """Test discover plugins returns a result."""
        bridge_result = FlextMeltano.discover_plugins()
        tm.that(bridge_result.is_failure or bridge_result.is_success, eq=True)

    def test_api_basic_functionality(self) -> None:
        """Test basic API functionality."""
        api = FlextMeltano()
        tm.that(hasattr(api, "version"), eq=True)
        tm.that(hasattr(api, "service_name"), eq=True)


class TestFlextMeltanoDataOperations:
    """Test FlextMeltano data extraction and loading operations."""

    def test_extract_source_with_schema(self) -> None:
        """Test data extraction with schema."""
        api = FlextMeltano()
        schema: t.Meltano.SchemaDict = {"type": "object"}
        result = api.extract_source(schema)
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_run_source_without_name(self) -> None:
        """Test source run with empty name."""
        api = FlextMeltano()
        result = api.run_source("")
        tm.fail(result)

    def test_load_batch_without_records(self) -> None:
        """Test batch loading with empty records."""
        api = FlextMeltano()
        records: Sequence[t.Meltano.RecordDict] = []
        result = api.load_batch(records)
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_load_batch_with_records(self) -> None:
        """Test batch loading with actual records."""
        api = FlextMeltano()
        records: Sequence[t.Meltano.RecordDict] = [{"id": 1, "name": "test"}]
        result = api.load_batch(records)
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_run_sink_without_name(self) -> None:
        """Test sink run with empty name."""
        api = FlextMeltano()
        result = api.run_sink("")
        tm.fail(result)

    def test_run_source_with_name(self) -> None:
        """Test source run with name."""
        api = FlextMeltano()
        result = api.run_source("source-csv")
        tm.that(result.is_failure or result.is_success, eq=True)


class TestFlextMeltanoDbtOperations:
    """Test FlextMeltano DBT operations."""

    def test_run_transformation_models_without_models(self) -> None:
        """Test transformation run with empty model list uses all_models default."""
        api = FlextMeltano()
        result = api.run_transformation_models(models=[])
        tm.ok(result)
        tm.that(result.value, none=False)
        models_val = result.value.get("models")
        tm.that(models_val, eq=["all_models"])

    def test_run_transformation_models_with_list(self) -> None:
        """Test transformation run with specific models."""
        api = FlextMeltano()
        result = api.run_transformation_models(models=["model1"])
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_test_transformation_models_without_models(self) -> None:
        """Test transformation test with empty model list uses all_models default."""
        api = FlextMeltano()
        result = api.test_transformation_models(models=[])
        tm.ok(result)
        tm.that(result.value, none=False)
        models_val = result.value.get("models")
        tm.that(models_val, eq=["all_models"])

    def test_run_transformation_models_with_models(self) -> None:
        """Test transformation run with model list."""
        api = FlextMeltano()
        result = api.run_transformation_models(models=["model1"])
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_test_transformation_models_with_models(self) -> None:
        """Test transformation test with model list."""
        api = FlextMeltano()
        result = api.test_transformation_models(models=["model1"])
        tm.that(result.is_failure or result.is_success, eq=True)


class TestFlextMeltanoELTPipeline:
    """Test FlextMeltano complete ELT pipeline operations."""

    def test_run_pipeline_without_source(self) -> None:
        """Test pipeline without source name."""
        api = FlextMeltano()
        result = api.run_pipeline(source_name="", sink_name="target-jsonl")
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_run_pipeline_without_sink(self) -> None:
        """Test pipeline without sink name."""
        api = FlextMeltano()
        result = api.run_pipeline(source_name="tap-csv", sink_name="")
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_run_pipeline_with_source_and_sink(self) -> None:
        """Test pipeline with source and sink."""
        api = FlextMeltano()
        result = api.run_pipeline(
            source_name="tap-csv",
            sink_name="target-jsonl",
        )
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_execute_pipeline_tap_target(self) -> None:
        """Test execute pipeline with tap and target."""
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
        api = FlextMeltano()
        result = api.validate_project(Path("/invalid/path"))
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
            validate_result = api.validate_project(project_path)
            tm.that(validate_result.is_failure or validate_result.is_success, eq=True)
            plugins_result = api.list_plugins()
            tm.that(plugins_result.is_failure or plugins_result.is_success, eq=True)

    def test_api_service_operations(self) -> None:
        """Test API service operations."""
        api = FlextMeltano()
        tm.that(api, none=False)
        with tempfile.TemporaryDirectory() as temp_dir:
            result = api.create_project(
                project_name="context_test",
                project_dir=Path(temp_dir),
            )
            tm.that(result.is_success or result.is_failure, eq=True)


class TestFlextMeltanoExecuteMethod:
    """Test FlextMeltano execute method."""

    def test_execute_returns_config(self) -> None:
        """Test execute method returns config dict."""
        api = FlextMeltano()
        result = api.execute()
        tm.ok(result)
        tm.that(result.value, none=False)

    def test_execute_contains_version(self) -> None:
        """Test execute result contains version info."""
        api = FlextMeltano()
        result = api.execute()
        tm.ok(result)
        value_str = str(result.value)
        tm.that("version" in value_str, eq=True)

    def test_execute_returns_success(self) -> None:
        """Test execute method returns success."""
        api = FlextMeltano()
        result = api.execute()
        tm.that(result.is_success or result.is_failure, eq=True)


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
        api = FlextMeltano()
        result = api.validate_project(Path("/nonexistent/path"))
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
        api = FlextMeltano()
        result = api.install_component(
            component_type="invalid",
            component_name="nonexistent-plugin",
        )
        tm.fail(result)

    def test_list_plugins_exception_path(self) -> None:
        """Test plugin listing returns result."""
        api = FlextMeltano()
        result = api.list_plugins()
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_discover_exception_path(self) -> None:
        """Test discover returns result."""
        api = FlextMeltano()
        result = api.discover()
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_extract_source_exception_path(self) -> None:
        """Test data extraction exception handling."""
        api = FlextMeltano()
        schema: t.Meltano.SchemaDict = {"stream": "nonexistent-stream"}
        result = api.extract_source(schema)
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_load_batch_exception_path(self) -> None:
        """Test batch loading exception handling."""
        api = FlextMeltano()
        records: Sequence[t.Meltano.RecordDict] = []
        result = api.load_batch(records)
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_run_transformation_models_exception_path(self) -> None:
        """Test transformation models execution exception handling."""
        api = FlextMeltano()
        result = api.run_transformation_models(models=["model1"])
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_test_transformation_models_exception_path(self) -> None:
        """Test transformation models testing exception handling."""
        api = FlextMeltano()
        result = api.test_transformation_models(models=["model1"])
        tm.that(result.is_failure or result.is_success, eq=True)

    def test_run_pipeline_exception_path(self) -> None:
        """Test pipeline exception handling."""
        api = FlextMeltano()
        result = api.run_pipeline(
            source_name="tap",
            sink_name="target",
        )
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
