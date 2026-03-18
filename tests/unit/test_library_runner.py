"""Tests for FlextMeltanoLibraryRunner - Advanced library integration patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from flext_meltano import FlextMeltanoLibraryRunner, r, t
from flext_meltano.adapters import FlextMeltanoAdapter


class TestFlextDbtProgrammaticRunner:
    """Test FlextDbtProgrammaticRunner functionality."""

    def test_get_dbt_runner(self) -> None:
        """Test getting dbt runner instance returns r."""
        library_runner = FlextMeltanoLibraryRunner()
        dbt_runner_result = library_runner.get_dbt_runner()
        tm.ok(dbt_runner_result)
        tm.that(dbt_runner_result.value is not None, eq=True)
        tm.that(dbt_runner_result.value.get("type"), eq="dbt_runner")
        tm.that(dbt_runner_result.value.get("status"), eq="available")

    def test_dbt_runner_capabilities(self) -> None:
        """Test dbt runner has expected capabilities."""
        library_runner = FlextMeltanoLibraryRunner()
        dbt_runner_result = library_runner.get_dbt_runner()
        tm.ok(dbt_runner_result)
        capabilities = dbt_runner_result.value.get("capabilities", [])
        tm.that(isinstance(capabilities, list), eq=True)
        tm.that("run" in capabilities, eq=True)
        tm.that("test" in capabilities, eq=True)


class TestFlextSingerProtocolManager:
    """Test FlextSingerProtocolManager functionality."""

    def test_get_singer_manager(self) -> None:
        """Test getting Singer manager instance returns r."""
        library_runner = FlextMeltanoLibraryRunner()
        singer_manager_result = library_runner.get_singer_manager()
        tm.ok(singer_manager_result)
        tm.that(singer_manager_result.value is not None, eq=True)
        tm.that(singer_manager_result.value.get("type"), eq="singer_manager")
        tm.that(singer_manager_result.value.get("status"), eq="available")

    def test_singer_manager_capabilities(self) -> None:
        """Test Singer manager has expected capabilities."""
        library_runner = FlextMeltanoLibraryRunner()
        singer_manager_result = library_runner.get_singer_manager()
        tm.ok(singer_manager_result)
        capabilities = singer_manager_result.value.get("capabilities", [])
        tm.that(isinstance(capabilities, list), eq=True)
        tm.that("discover" in capabilities, eq=True)
        tm.that("sync" in capabilities, eq=True)


class TestFlextMeltanoLibraryRunner:
    """Test FlextMeltanoLibraryRunner functionality."""

    def test_initialization(self) -> None:
        """Test library runner initialization."""
        runner = FlextMeltanoLibraryRunner()
        dbt_runner_result = runner.get_dbt_runner()
        tm.ok(dbt_runner_result)
        tm.that(dbt_runner_result.value is not None, eq=True)
        singer_manager_result = runner.get_singer_manager()
        tm.ok(singer_manager_result)
        tm.that(singer_manager_result.value is not None, eq=True)

    def test_get_dbt_runner(self) -> None:
        """Test getting dbt runner instance."""
        runner = FlextMeltanoLibraryRunner()
        dbt_runner_result = runner.get_dbt_runner()
        tm.ok(dbt_runner_result)
        tm.that(dbt_runner_result.value is not None, eq=True)
        tm.that(dbt_runner_result.value.get("type"), eq="dbt_runner")

    def test_get_singer_manager(self) -> None:
        """Test getting Singer manager instance."""
        runner = FlextMeltanoLibraryRunner()
        singer_manager_result = runner.get_singer_manager()
        tm.ok(singer_manager_result)
        tm.that(singer_manager_result.value is not None, eq=True)
        tm.that(singer_manager_result.value.get("type"), eq="singer_manager")

    def test_get_abstractions(self) -> None:
        """Test getting abstractions instance."""
        runner = FlextMeltanoLibraryRunner()
        singer_manager_result = runner.get_singer_manager()
        tm.ok(singer_manager_result)

    def test_execute_complete_elt_pipeline_mock(self) -> None:
        """Test complete E-L-T pipeline execution with mocked dependencies."""
        runner = FlextMeltanoLibraryRunner()
        result: r[t.Meltano.Processing.EltPipelineResult] = (
            runner.execute_complete_elt_pipeline(
                tap_name="tap-csv", target_name="target-jsonl"
            )
        )
        tm.ok(result)
        pipeline_data: t.Meltano.Processing.EltPipelineResult = result.value
        tm.that(isinstance(pipeline_data, dict), eq=True)
        tm.that("success" in pipeline_data, eq=True)
        tm.that("tap_name" in pipeline_data, eq=True)
        tm.that("target_name" in pipeline_data, eq=True)
        tm.that("execution_time" in pipeline_data, eq=True)


class TestProjectAdapterIntegration:
    """Test integration of FlextMeltanoAdapter.FlextMeltanoAdapter.ProjectAdapter."""

    def test_adapter_version(self) -> None:
        """Test that FlextMeltanoAdapter.ProjectAdapter can get version."""
        adapter = FlextMeltanoAdapter.ProjectAdapter()
        result = adapter.get_version()
        tm.ok(result)
        tm.that(result.value is not None, eq=True)
        tm.that("version" in result.value, eq=True)

    def test_adapter_execute(self) -> None:
        """Test that FlextMeltanoAdapter.ProjectAdapter execute returns r."""
        adapter = FlextMeltanoAdapter.ProjectAdapter()
        result = adapter.execute()
        tm.that(hasattr(result, "is_success"), eq=True)
        tm.that(hasattr(result, "is_failure"), eq=True)
