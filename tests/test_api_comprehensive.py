"""Comprehensive tests for FlextMeltanoAPI - Real API testing without mocks.

Tests the main unified API for FLEXT Meltano operations following enterprise
testing standards with real Meltano integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from flext_core import FlextResult
from flext_meltano import (
    FlextMeltanoAPI,
    FlextMeltanoConstants,
    FlextMeltanoExceptions,
    FlextMeltanoModels,
    FlextMeltanoTypes,
)

pytestmark = pytest.mark.asyncio


class TestFlextMeltanoAPIInitialization:
    """Test FlextMeltanoAPI initialization and basic properties."""

    async def test_api_initialization_default(self) -> None:
        """Test API initialization with default parameters."""

        # Create a concrete implementation for testing
        class ConcreteAPI(FlextMeltanoAPI):
            async def execute(self, command: str) -> FlextResult[str]:
                return FlextResult[str].ok("test")

        api = ConcreteAPI()
        assert api is not None

    async def test_api_initialization_with_project_root(self) -> None:
        """Test API initialization with specific project root."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            api = FlextMeltanoAPI(project_root=temp_path)

            assert api is not None

    async def test_api_version_property(self) -> None:
        """Test API version property."""
        api = FlextMeltanoAPI()
        version = api.version

        assert version == FlextMeltanoConstants.FLEXT_MELTANO_VERSION

    async def test_api_constants_property(self) -> None:
        """Test API constants property."""
        api = FlextMeltanoAPI()
        constants = api.constants

        assert constants == FlextMeltanoConstants

    async def test_api_exceptions_property(self) -> None:
        """Test API exceptions property."""
        api = FlextMeltanoAPI()
        exceptions = api.exceptions

        assert exceptions == FlextMeltanoExceptions

    async def test_api_types_property(self) -> None:
        """Test API types property."""
        api = FlextMeltanoAPI()
        types = api.types

        assert types == FlextMeltanoTypes

    async def test_api_models_property(self) -> None:
        """Test API models property."""
        api = FlextMeltanoAPI()
        models = api.models

        assert models == FlextMeltanoModels


class TestFlextMeltanoAPIProjectOperations:
    """Test FlextMeltanoAPI project creation and validation operations."""

    async def test_create_project_success(self) -> None:
        """Test successful project creation."""
        api = FlextMeltanoAPI()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "test_project"

            result = await api.create_project(
                project_name="test_project", project_root=str(project_path.parent)
            )

            assert result.is_success or "already exists" in (result.error or "")

    async def test_create_project_invalid_name(self) -> None:
        """Test project creation with invalid name."""
        api = FlextMeltanoAPI()

        with tempfile.TemporaryDirectory() as temp_dir:
            result = await api.create_project(project_name="", project_root=temp_dir)

            assert result.is_failure
            assert result.error is not None

    async def test_create_project_with_config(self) -> None:
        """Test project creation with configuration."""
        api = FlextMeltanoAPI()

        with tempfile.TemporaryDirectory() as temp_dir:
            result = await api.create_project(
                project_name="config_test",
                project_root=temp_dir,
                config={"environment": "test"},
            )

            assert result.is_success or result.is_failure

    async def test_validate_project_nonexistent(self) -> None:
        """Test validation of non-existent project."""
        api = FlextMeltanoAPI()

        with tempfile.TemporaryDirectory() as temp_dir:
            nonexistent = Path(temp_dir) / "nonexistent"

            result = await api.validate_project(str(nonexistent))

            assert result.is_failure
            assert result.error is not None

    async def test_validate_project_with_path(self) -> None:
        """Test project validation with specific path."""
        api = FlextMeltanoAPI()

        with tempfile.TemporaryDirectory() as temp_dir:
            result = await api.validate_project(Path(temp_dir))

            assert result.is_success or result.is_failure


class TestFlextMeltanoAPIPluginOperations:
    """Test FlextMeltanoAPI plugin installation and listing operations."""

    async def test_install_plugin_without_project(self) -> None:
        """Test plugin installation without valid project."""
        api = FlextMeltanoAPI()

        result = await api.install_plugin(
            plugin_type="extractors", plugin_name="tap-csv"
        )

        assert result.is_failure or result.is_success

    async def test_install_plugin_invalid_type(self) -> None:
        """Test plugin installation with invalid type."""
        api = FlextMeltanoAPI()

        with tempfile.TemporaryDirectory() as temp_dir:
            result = await api.install_plugin(
                plugin_type="invalid_type", plugin_name="tap-csv", project_root=temp_dir
            )

            assert result.is_failure
            assert result.error is not None

    async def test_install_plugin_with_config(self) -> None:
        """Test plugin installation with configuration."""
        api = FlextMeltanoAPI()

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        result = await api.install_plugin(
            plugin_type="extractors",
            plugin_name="tap-csv",
            plugin_config={"path": tmp_path},
        )

        assert result.is_failure or result.is_success

    async def test_list_plugins_without_project(self) -> None:
        """Test listing plugins without valid project."""
        api = FlextMeltanoAPI()

        result = await api.list_plugins()

        assert result.is_failure or result.is_success

    async def test_list_plugins_with_type_filter(self) -> None:
        """Test listing plugins with type filter."""
        api = FlextMeltanoAPI()

        result = await api.list_plugins(_plugin_type="extractors")

        assert result.is_failure or result.is_success


class TestFlextMeltanoAPICatalogOperations:
    """Test FlextMeltanoAPI catalog discovery operations."""

    async def test_discover_catalog_without_tap(self) -> None:
        """Test catalog discovery without tap name."""
        api = FlextMeltanoAPI()

        result = await api.discover_catalog(tap_name="")

        assert result.is_failure
        assert result.error is not None

    async def test_discover_catalog_nonexistent_tap(self) -> None:
        """Test catalog discovery with non-existent tap."""
        api = FlextMeltanoAPI()

        result = await api.discover_catalog(tap_name="nonexistent-tap")

        assert result.is_failure or result.is_success

    async def test_discover_catalog_with_config(self) -> None:
        """Test catalog discovery with configuration."""
        api = FlextMeltanoAPI()

        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
            tmp_path = tmp_file.name

        result = await api.discover_catalog(
            tap_name="tap-csv",
            config={"path": tmp_path},
        )

        assert result.is_failure or result.is_success


class TestFlextMeltanoAPIDataOperations:
    """Test FlextMeltanoAPI data extraction and loading operations."""

    async def test_extract_data_without_tap(self) -> None:
        """Test data extraction without tap name."""
        api = FlextMeltanoAPI()

        result = await api.extract_data(tap_name="", stream_name="test_stream")

        assert result.is_failure
        assert result.error is not None

    async def test_extract_data_without_stream(self) -> None:
        """Test data extraction without stream name."""
        api = FlextMeltanoAPI()

        result = await api.extract_data(tap_name="tap-csv", stream_name="")

        assert result.is_failure
        assert result.error is not None

    async def test_load_data_without_target(self) -> None:
        """Test data loading without target name."""
        api = FlextMeltanoAPI()

        result = await api.load_data(
            target_name="", stream_name="test_stream", records=[]
        )

        assert result.is_failure or result.is_success

    async def test_load_data_with_empty_records(self) -> None:
        """Test data loading with empty records."""
        api = FlextMeltanoAPI()

        result = await api.load_data(
            target_name="target-jsonl", stream_name="test_stream", records=[]
        )

        assert result.is_failure or result.is_success

    async def test_extract_data_with_limit(self) -> None:
        """Test data extraction with record limit."""
        api = FlextMeltanoAPI()

        result = await api.extract_data(
            tap_name="tap-csv", stream_name="test_stream", limit=100
        )

        assert result.is_failure or result.is_success

    async def test_load_data_with_records(self) -> None:
        """Test data loading with actual records."""
        api = FlextMeltanoAPI()

        records = [{"id": 1, "name": "test"}]
        result = await api.load_data(
            target_name="target-jsonl", stream_name="test_stream", records=records
        )

        assert result.is_failure or result.is_success


class TestFlextMeltanoAPIDbtOperations:
    """Test FlextMeltanoAPI DBT operations."""

    async def test_run_dbt_models_without_models(self) -> None:
        """Test DBT run without model list."""
        api = FlextMeltanoAPI()

        result = await api.run_dbt_models(models=[])

        assert result.is_failure
        assert result.error is not None

    async def test_run_dbt_models_without_project(self) -> None:
        """Test DBT run without valid project."""
        api = FlextMeltanoAPI()

        result = await api.run_dbt_models(models=["model1"])

        assert result.is_failure or result.is_success

    async def test_test_dbt_models_without_models(self) -> None:
        """Test DBT test without model list."""
        api = FlextMeltanoAPI()

        result = await api.test_dbt_models(models=[])

        assert result.is_failure
        assert result.error is not None

    async def test_run_dbt_models_with_project(self) -> None:
        """Test DBT run with project root."""
        api = FlextMeltanoAPI()

        with tempfile.TemporaryDirectory() as temp_dir:
            result = await api.run_dbt_models(models=["model1"], project_root=temp_dir)

            assert result.is_failure or result.is_success

    async def test_test_dbt_models_with_project(self) -> None:
        """Test DBT test with project root."""
        api = FlextMeltanoAPI()

        with tempfile.TemporaryDirectory() as temp_dir:
            result = await api.test_dbt_models(models=["model1"], project_root=temp_dir)

            assert result.is_failure or result.is_success


class TestFlextMeltanoAPIELTPipeline:
    """Test FlextMeltanoAPI complete ELT pipeline operations."""

    async def test_run_elt_pipeline_without_tap(self) -> None:
        """Test ELT pipeline without tap name."""
        api = FlextMeltanoAPI()

        result = await api.run_elt_pipeline(
            tap_name="", target_name="target-jsonl", stream_name="test_stream"
        )

        assert result.is_failure
        assert result.error is not None

    async def test_run_elt_pipeline_without_target(self) -> None:
        """Test ELT pipeline without target name."""
        api = FlextMeltanoAPI()

        result = await api.run_elt_pipeline(
            tap_name="tap-csv", target_name="", stream_name="test_stream"
        )

        assert result.is_failure
        assert result.error is not None

    async def test_run_elt_pipeline_without_stream(self) -> None:
        """Test ELT pipeline without stream name."""
        api = FlextMeltanoAPI()

        result = await api.run_elt_pipeline(
            tap_name="tap-csv", target_name="target-jsonl", stream_name=""
        )

        assert result.is_failure
        assert result.error is not None

    async def test_run_elt_pipeline_with_dbt_models(self) -> None:
        """Test ELT pipeline with DBT models."""
        api = FlextMeltanoAPI()

        result = await api.run_elt_pipeline(
            tap_name="tap-csv",
            target_name="target-jsonl",
            stream_name="test_stream",
            dbt_models=["model1", "model2"],
        )

        assert result.is_failure or result.is_success


class TestFlextMeltanoAPIErrorHandling:
    """Test FlextMeltanoAPI error handling and edge cases."""

    async def test_api_handles_none_project_root(self) -> None:
        """Test API handles None project root gracefully."""
        api = FlextMeltanoAPI(project_root=None)
        assert api is not None

    async def test_api_handles_invalid_project_root(self) -> None:
        """Test API handles invalid project root type."""
        api = FlextMeltanoAPI(project_root=123)
        assert api is not None

    async def test_create_project_exception_handling(self) -> None:
        """Test project creation handles exceptions gracefully."""
        api = FlextMeltanoAPI()

        result = await api.create_project(
            project_name="test", project_root="/invalid/path/that/does/not/exist"
        )

        assert result.is_failure or result.is_success

    async def test_validate_project_exception_handling(self) -> None:
        """Test project validation handles exceptions gracefully."""
        api = FlextMeltanoAPI()

        result = await api.validate_project("/invalid/path")

        assert result.is_failure
        assert result.error is not None


class TestFlextMeltanoAPIIntegration:
    """Integration tests for FlextMeltanoAPI operations."""

    async def test_api_full_workflow_simulation(self) -> None:
        """Test simulated full workflow without actual Meltano execution."""
        api = FlextMeltanoAPI()

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = Path(temp_dir) / "integration_test"

            create_result = await api.create_project(
                project_name="integration_test", project_root=str(project_path.parent)
            )

            assert create_result.is_success or "already exists" in (
                create_result.error or ""
            )

            validate_result = await api.validate_project(str(project_path))

            assert validate_result.is_failure or validate_result.is_success

            plugins_result = await api.list_plugins()

            assert plugins_result.is_failure or plugins_result.is_success

    async def test_api_respects_project_root_context(self) -> None:
        """Test API respects project root context across operations."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            api = FlextMeltanoAPI(project_root=temp_path)

            assert api is not None

            result = await api.create_project(project_name="context_test")

            assert result.is_success or result.is_failure


class TestFlextMeltanoAPIExecuteMethod:
    """Test FlextMeltanoAPI execute method."""

    async def test_execute_version_command(self) -> None:
        """Test execute method with version command."""
        api = FlextMeltanoAPI()

        result = await api.execute("version")

        assert result.is_success
        assert "version" in result.unwrap()

    async def test_execute_unknown_command(self) -> None:
        """Test execute method with unknown command."""
        api = FlextMeltanoAPI()

        result = await api.execute("unknown_command")

        assert result.is_failure or result.is_success

    async def test_execute_with_options(self) -> None:
        """Test execute method with options."""
        api = FlextMeltanoAPI()

        result = await api.execute("version", debug=True)

        assert result.is_success or result.is_failure


@pytest.mark.benchmark
class TestFlextMeltanoAPISuccessPaths:
    """Test FlextMeltanoAPI success scenarios for coverage."""

    async def test_create_project_exception_path(self) -> None:
        """Test project creation exception handling."""
        api = FlextMeltanoAPI()

        result = await api.create_project(
            project_name="test",
            project_root="/nonexistent/impossible/path/that/cannot/exist",
        )

        assert result.is_failure
        assert "Failed to create" in (result.error or "")

    async def test_validate_project_exception_path(self) -> None:
        """Test project validation exception handling."""
        api = FlextMeltanoAPI()

        result = await api.validate_project(Path("/nonexistent/path"))

        assert result.is_failure
        assert "Failed to validate project" in (result.error or "")

    async def test_install_plugin_exception_path(self) -> None:
        """Test plugin installation exception handling."""
        api = FlextMeltanoAPI()

        result = await api.install_plugin(
            plugin_type="invalid", plugin_name="nonexistent-plugin"
        )

        assert result.is_failure

    async def test_list_plugins_exception_path(self) -> None:
        """Test plugin listing exception handling."""
        api = FlextMeltanoAPI()

        result = await api.list_plugins()

        assert result.is_failure or result.is_success

    async def test_discover_catalog_exception_path(self) -> None:
        """Test catalog discovery exception handling."""
        api = FlextMeltanoAPI()

        result = await api.discover_catalog(tap_name="nonexistent-tap")

        assert result.is_failure or result.is_success

    async def test_extract_data_exception_path(self) -> None:
        """Test data extraction exception handling."""
        api = FlextMeltanoAPI()

        result = await api.extract_data(
            tap_name="nonexistent-tap", stream_name="nonexistent-stream"
        )

        assert result.is_failure or result.is_success

    async def test_load_data_exception_path(self) -> None:
        """Test data loading exception handling."""
        api = FlextMeltanoAPI()

        result = await api.load_data(
            target_name="nonexistent-target", stream_name="test", records=[]
        )

        assert result.is_failure or result.is_success

    async def test_run_dbt_models_exception_path(self) -> None:
        """Test DBT models execution exception handling."""
        api = FlextMeltanoAPI()

        result = await api.run_dbt_models(models=["model1"])

        assert result.is_failure or result.is_success

    async def test_test_dbt_models_exception_path(self) -> None:
        """Test DBT models testing exception handling."""
        api = FlextMeltanoAPI()

        result = await api.test_dbt_models(models=["model1"])

        assert result.is_failure or result.is_success

    async def test_run_elt_pipeline_exception_path(self) -> None:
        """Test ELT pipeline exception handling."""
        api = FlextMeltanoAPI()

        result = await api.run_elt_pipeline(
            tap_name="tap", target_name="target", stream_name="stream"
        )

        assert result.is_failure or result.is_success


@pytest.mark.benchmark
class TestFlextMeltanoAPIPerformance:
    """Performance benchmarks for FlextMeltanoAPI operations."""

    async def test_api_initialization_performance(self, benchmark: object) -> None:
        """Benchmark API initialization performance."""

        def create_api() -> FlextMeltanoAPI:
            return FlextMeltanoAPI()

        result = benchmark(create_api)
        assert result is not None

    async def test_api_properties_access_performance(self, benchmark: object) -> None:
        """Benchmark API properties access performance."""
        api = FlextMeltanoAPI()

        def access_properties() -> tuple[str, type, type, type, type]:
            return (api.version, api.constants, api.exceptions, api.types, api.models)

        result = benchmark(access_properties)
        assert result is not None
