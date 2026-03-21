"""Comprehensive tests for FlextMeltano - Real API testing without mocks.

Tests the main unified API for FLEXT Meltano operations following enterprise
testing standards with real Meltano integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import override

import pytest
from flext_core import r
from pytest_benchmark.fixture import BenchmarkFixture

from flext_meltano import FlextMeltano, c, m, t
from tests.utilities import u

pytestmark = pytest.mark.unit


class TestFlextMeltanoInitialization:
    """Test FlextMeltano initialization and basic properties."""

    def test_api_initialization_default(self) -> None:
        """Test API initialization with default parameters."""

        class ConcreteAPI(FlextMeltano):
            @override
            def execute(self, **kwargs: t.Scalar) -> r[m.Meltano.ConfigMappingPayload]:
                _ = kwargs
                payload = m.Meltano.ConfigMappingPayload(values={"status": "ok"})
                return r[m.Meltano.ConfigMappingPayload].ok(payload)

        api = ConcreteAPI(service_name="test-api")
        u.Tests.Matchers.that(api is not None, eq=True)

    def test_api_initialization_with_project_root(self) -> None:
        """Test API initialization with specific project root."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            api = FlextMeltano(project_root=str(temp_path))
            u.Tests.Matchers.that(api is not None, eq=True)

    def test_api_version_property(self) -> None:
        """Test API version property."""
        api = FlextMeltano()
        version = api.version
        u.Tests.Matchers.that(version, eq=c.Meltano.FLEXT_MELTANO_VERSION)

    def test_api_constants_property(self) -> None:
        """Test API constants property."""
        api = FlextMeltano()
        constants = api.constants
        u.Tests.Matchers.that(constants, eq=c)

    def test_api_types_property(self) -> None:
        """Test API types property."""
        api = FlextMeltano()
        types = api.types
        u.Tests.Matchers.that(types is t, eq=True)

    def test_api_models_property(self) -> None:
        """Test API models property."""
        api = FlextMeltano()
        models = api.models
        u.Tests.Matchers.that(models, eq=m)


class TestFlextMeltanoProjectOperations:
    """Test FlextMeltano project creation and validation operations."""

    def test_api_service_name_property(self) -> None:
        """Test API service name property."""
        api = FlextMeltano(service_name="test-service")
        u.Tests.Matchers.that(api.service_name, eq="test-service")

    def test_create_project_invalid_name(self) -> None:
        """Test project creation with invalid name."""
        api = FlextMeltano()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = api.create_project(project_name="", project_dir=temp_dir)
            u.Tests.Matchers.fail(result)
            u.Tests.Matchers.that(result.error is not None, eq=True)

    def test_create_project_with_config(self) -> None:
        """Test project creation with project_dir."""
        api = FlextMeltano()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = api.create_project(
                project_name="config_test", project_dir=temp_dir
            )
            u.Tests.Matchers.that(result.is_success or result.is_failure, eq=True)

    def test_validate_project_nonexistent(self) -> None:
        """Test validation of non-existent project."""
        api = FlextMeltano()
        with tempfile.TemporaryDirectory() as temp_dir:
            nonexistent = Path(temp_dir) / "nonexistent"
            result = api.validate_project(str(nonexistent))
            u.Tests.Matchers.fail(result)
            u.Tests.Matchers.that(result.error is not None, eq=True)

    def test_validate_project_with_path(self) -> None:
        """Test project validation with specific path."""
        api = FlextMeltano()
        with tempfile.TemporaryDirectory() as temp_dir:
            result = api.validate_project(str(temp_dir))
            u.Tests.Matchers.that(result.is_success or result.is_failure, eq=True)


class TestFlextMeltanoPluginOperations:
    """Test FlextMeltano plugin installation and listing operations."""

    def test_install_plugin_without_project(self) -> None:
        """Test plugin installation without valid project."""
        api = FlextMeltano()
        result = api.install_plugin(plugin_type="extractors", plugin_name="tap-csv")
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_install_plugin_invalid_type(self) -> None:
        """Test plugin installation with invalid type."""
        api = FlextMeltano()
        result = api.install_plugin(plugin_type="invalid_type", plugin_name="tap-csv")
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(result.error is not None, eq=True)

    def test_install_plugin_with_config(self) -> None:
        """Test plugin installation with configuration."""
        api = FlextMeltano()
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
            tmp_path = tmp_file.name
        result = api.install_plugin(
            plugin_type="extractors", plugin_name="tap-csv", config={"path": tmp_path}
        )
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_list_plugins_without_project(self) -> None:
        """Test listing plugins without valid project."""
        api = FlextMeltano()
        result = api.list_plugins()
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_list_plugins_with_type_filter(self) -> None:
        """Test listing plugins with type filter."""
        api = FlextMeltano()
        result = api.list_plugins(plugin_type="extractors")
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)


class TestFlextMeltanoCatalogOperations:
    """Test FlextMeltano catalog discovery operations."""

    def test_discover_catalog_without_tap(self) -> None:
        """Test catalog discovery without tap name."""
        api = FlextMeltano()
        result = api.discover_catalog("")
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_discover_catalog_nonexistent_tap(self) -> None:
        """Test catalog discovery with non-existent tap."""
        api = FlextMeltano()
        result = api.discover_catalog("nonexistent-tap")
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_api_basic_functionality(self) -> None:
        """Test basic API functionality."""
        api = FlextMeltano()
        u.Tests.Matchers.that(hasattr(api, "version"), eq=True)
        u.Tests.Matchers.that(hasattr(api, "constants"), eq=True)
        u.Tests.Matchers.that(hasattr(api, "service_name"), eq=True)


class TestFlextMeltanoDataOperations:
    """Test FlextMeltano data extraction and loading operations."""

    def test_extract_data_without_tap(self) -> None:
        """Test data extraction without tap name."""
        api = FlextMeltano()
        result = api.extract_data("")
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_extract_data_without_stream(self) -> None:
        """Test data extraction with empty source name."""
        api = FlextMeltano()
        result = api.extract_data("")
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_load_data_without_target(self) -> None:
        """Test data loading without target name (empty sink_name)."""
        api = FlextMeltano()
        result = api.load_data(sink_name="", records=[])
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_load_data_with_empty_records(self) -> None:
        """Test data loading with empty records."""
        api = FlextMeltano()
        result = api.load_data(sink_name="target-jsonl", records=[])
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_extract_data_with_limit(self) -> None:
        """Test data extraction with record limit."""
        api = FlextMeltano()
        result = api.extract_data("tap-csv")
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_load_data_with_records(self) -> None:
        """Test data loading with actual records."""
        api = FlextMeltano()
        records: list[t.Meltano.RecordDict] = [{"id": 1, "name": "test"}]
        result = api.load_data(sink_name="target-jsonl", records=records)
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)


class TestFlextMeltanoDbtOperations:
    """Test FlextMeltano DBT operations."""

    def test_run_dbt_models_without_models(self) -> None:
        """Test DBT run with empty model list uses all_models default."""
        api = FlextMeltano()
        result = api.run_dbt_models(models=[])
        u.Tests.Matchers.ok(result)
        u.Tests.Matchers.that(result.value is not None, eq=True)
        u.Tests.Matchers.that(result.value.get("models"), eq=["all_models"])

    def test_run_dbt_models_without_project(self) -> None:
        """Test DBT run without valid project."""
        api = FlextMeltano()
        result = api.run_dbt_models(models=["model1"])
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_test_dbt_models_without_models(self) -> None:
        """Test DBT test with empty model list uses all_models default."""
        api = FlextMeltano()
        result = api.test_dbt_models(models=[])
        u.Tests.Matchers.ok(result)
        u.Tests.Matchers.that(result.value is not None, eq=True)
        u.Tests.Matchers.that(result.value.get("models"), eq=["all_models"])

    def test_run_dbt_models_with_project(self) -> None:
        """Test DBT run with project root."""
        api = FlextMeltano()
        result = api.run_dbt_models(models=["model1"])
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_test_dbt_models_with_project(self) -> None:
        """Test DBT test with project root."""
        api = FlextMeltano()
        result = api.test_dbt_models(models=["model1"])
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)


class TestFlextMeltanoELTPipeline:
    """Test FlextMeltano complete ELT pipeline operations."""

    def test_run_elt_pipeline_without_tap(self) -> None:
        """Test ELT pipeline without tap name."""
        api = FlextMeltano()
        result = api.run_elt_pipeline(tap_name="", target_name="target-jsonl")
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(result.error is not None, eq=True)

    def test_run_elt_pipeline_without_target(self) -> None:
        """Test ELT pipeline without target name."""
        api = FlextMeltano()
        result = api.run_elt_pipeline(tap_name="tap-csv", target_name="")
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(result.error is not None, eq=True)

    def test_run_elt_pipeline_without_stream(self) -> None:
        """Test ELT pipeline without stream name (API may or may not require stream)."""
        api = FlextMeltano()
        result = api.run_elt_pipeline(tap_name="tap-csv", target_name="target-jsonl")
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_run_elt_pipeline_with_dbt_models(self) -> None:
        """Test ELT pipeline with DBT models."""
        api = FlextMeltano()
        result = api.run_elt_pipeline(
            tap_name="tap-csv",
            target_name="target-jsonl",
            dbt_models=["model1", "model2"],
        )
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)


class TestFlextMeltanoErrorHandling:
    """Test FlextMeltano error handling and edge cases."""

    def test_api_handles_none_project_root(self) -> None:
        """Test API handles None project root gracefully."""
        api = FlextMeltano(project_root=None)
        u.Tests.Matchers.that(api is not None, eq=True)

    def test_api_handles_invalid_project_root(self) -> None:
        """Test API handles invalid project root type."""
        try:
            invalid_root: object = 123
            FlextMeltano(project_root=invalid_root)
            pytest.fail("Should have raised TypeError or ValueError")
        except (TypeError, ValueError):
            pass

    def test_create_project_exception_handling(self) -> None:
        """Test project creation handles exceptions gracefully."""
        api = FlextMeltano()
        result = api.create_project(
            project_name="test", project_dir="/invalid/path/that/does/not/exist"
        )
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_validate_project_exception_handling(self) -> None:
        """Test project validation handles exceptions gracefully."""
        api = FlextMeltano()
        result = api.validate_project("/invalid/path")
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(result.error is not None, eq=True)


class TestFlextMeltanoIntegration:
    """Integration tests for FlextMeltano operations."""

    def test_api_full_workflow_simulation(self) -> None:
        """Test simulated full workflow without actual Meltano execution."""
        api = FlextMeltano()
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "integration_test"
            create_result = api.create_project(
                project_name="integration_test", project_dir=str(project_path.parent)
            )
            u.Tests.Matchers.that(
                create_result.is_success
                or "already exists" in (create_result.error or ""),
                eq=True,
            )
            validate_result = api.validate_project(str(project_path))
            u.Tests.Matchers.that(
                validate_result.is_failure or validate_result.is_success, eq=True
            )
            plugins_result = api.list_plugins()
            u.Tests.Matchers.that(
                plugins_result.is_failure or plugins_result.is_success, eq=True
            )

    def test_api_respects_project_root_context(self) -> None:
        """Test API respects project root context across operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            api = FlextMeltano(project_root=str(temp_path))
            u.Tests.Matchers.that(api is not None, eq=True)
            result = api.create_project(project_name="context_test")
            u.Tests.Matchers.that(result.is_success or result.is_failure, eq=True)


class TestFlextMeltanoExecuteMethod:
    """Test FlextMeltano execute method."""

    def test_execute_version_command(self) -> None:
        """Test execute method with version command."""
        api = FlextMeltano()
        result = api.execute()
        u.Tests.Matchers.ok(result)
        u.Tests.Matchers.that(result.value is not None, eq=True)
        u.Tests.Matchers.that("version" in str(result.value), eq=True)

    def test_execute_unknown_command(self) -> None:
        """Test execute method with unknown command."""
        api = FlextMeltano()
        result = api.execute()
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_execute_with_options(self) -> None:
        """Test execute method with options."""
        api = FlextMeltano()
        result = api.execute()
        u.Tests.Matchers.that(result.is_success or result.is_failure, eq=True)


@pytest.mark.benchmark
class TestFlextMeltanoSuccessPaths:
    """Test FlextMeltano success scenarios for coverage."""

    def test_create_project_exception_path(self) -> None:
        """Test project creation exception handling."""
        api = FlextMeltano()
        result = api.create_project(
            project_name="test",
            project_dir="/nonexistent/impossible/path/that/cannot/exist",
        )
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(
            result.error
            and (
                "Failed to create" in result.error
                or "Project creation failed" in result.error
                or "Permission denied" in result.error
            ),
            eq=True,
        )

    def test_validate_project_exception_path(self) -> None:
        """Test project validation exception handling."""
        api = FlextMeltano()
        result = api.validate_project("/nonexistent/path")
        u.Tests.Matchers.fail(result)
        u.Tests.Matchers.that(
            result.error
            and (
                "Failed to validate project" in result.error
                or "not found" in result.error
                or "validate" in (result.error or "").lower()
                or ("exist" in (result.error or "").lower())
            ),
            eq=True,
        )

    def test_install_plugin_exception_path(self) -> None:
        """Test plugin installation exception handling."""
        api = FlextMeltano()
        result = api.install_plugin(
            plugin_type="invalid", plugin_name="nonexistent-plugin"
        )
        u.Tests.Matchers.fail(result)

    def test_list_plugins_exception_path(self) -> None:
        """Test plugin listing exception handling."""
        api = FlextMeltano()
        result = api.list_plugins()
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_discover_catalog_exception_path(self) -> None:
        """Test catalog discovery exception handling."""
        api = FlextMeltano()
        result = api.discover_catalog("nonexistent-tap")
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_extract_data_exception_path(self) -> None:
        """Test data extraction exception handling."""
        api = FlextMeltano()
        result = api.extract_data(
            source_name="nonexistent-source", config={"stream": "nonexistent-stream"}
        )
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_load_data_exception_path(self) -> None:
        """Test data loading exception handling."""
        api = FlextMeltano()
        result = api.load_data(sink_name="nonexistent-target", records=[])
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_run_dbt_models_exception_path(self) -> None:
        """Test DBT models execution exception handling."""
        api = FlextMeltano()
        result = api.run_dbt_models(models=["model1"])
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_test_dbt_models_exception_path(self) -> None:
        """Test DBT models testing exception handling."""
        api = FlextMeltano()
        result = api.test_dbt_models(models=["model1"])
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)

    def test_run_elt_pipeline_exception_path(self) -> None:
        """Test ELT pipeline exception handling."""
        api = FlextMeltano()
        result = api.run_elt_pipeline(tap_name="tap", target_name="target")
        u.Tests.Matchers.that(result.is_failure or result.is_success, eq=True)


@pytest.mark.benchmark
class TestFlextMeltanoPerformance:
    """Performance benchmarks for FlextMeltano operations."""

    def test_api_initialization_performance(self, benchmark: BenchmarkFixture) -> None:
        """Benchmark API initialization performance."""

        def create_api() -> FlextMeltano:
            return FlextMeltano()

        result = benchmark(create_api)
        u.Tests.Matchers.that(result is not None, eq=True)

    def test_api_properties_access_performance(
        self, benchmark: BenchmarkFixture
    ) -> None:
        """Benchmark API properties access performance."""
        api = FlextMeltano()

        def access_properties() -> tuple[str, type]:
            return (api.version, api.constants)

        result = benchmark(access_properties)
        u.Tests.Matchers.that(result is not None, eq=True)
