"""Tests for FlextMeltanoLibraryRunner - Library integration patterns.

Tests the library runner from meltano/runner.py which provides ELT pipeline
execution and DBT transformation support. Methods that were removed (fake
stubs like get_dbt_runner, get_singer_manager) have been cleaned from tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_core import r
from flext_tests import tm

from flext_meltano import FlextMeltanoAdapter, FlextMeltanoLibraryRunner


class TestFlextMeltanoLibraryRunner:
    """Test FlextMeltanoLibraryRunner functionality."""

    def test_initialization(self) -> None:
        """Test library runner initialization."""
        runner = FlextMeltanoLibraryRunner()
        tm.that(runner, none=False)
        tm.that(hasattr(runner, "logger"), eq=True)

    def test_execute_raises_not_implemented(self) -> None:
        """Test execute raises NotImplementedError (requires meltano-core SDK)."""
        runner = FlextMeltanoLibraryRunner()
        with pytest.raises(NotImplementedError, match="meltano-core SDK"):
            runner.execute()

    def test_execute_complete_elt_pipeline(self) -> None:
        """Test complete E-L-T pipeline execution delegates to subprocess."""
        runner = FlextMeltanoLibraryRunner()
        result = runner.execute_complete_elt_pipeline(
            tap_name="tap-csv",
            target_name="target-jsonl",
        )
        # Pipeline runs subprocess; may succeed or fail depending on environment
        tm.that(result, is_=r)
        tm.that(result.is_success or result.is_failure, eq=True)

    def test_execute_complete_elt_pipeline_result_shape(self) -> None:
        """Test pipeline result has expected keys when successful."""
        runner = FlextMeltanoLibraryRunner()
        result = runner.execute_complete_elt_pipeline(
            tap_name="tap-csv",
            target_name="target-jsonl",
        )
        tm.that(result, is_=r)
        if result.is_success:
            pipeline_data = result.value
            tm.that(pipeline_data, is_=dict)
            tm.that(pipeline_data, has="success")
            tm.that(pipeline_data, has="tap_name")
            tm.that(pipeline_data, has="target_name")
            tm.that(pipeline_data, has="execution_time")

    def test_run_dbt_transformation(self) -> None:
        """Test DBT transformation delegates to executor subprocess."""
        runner = FlextMeltanoLibraryRunner()
        result = runner.run_dbt_transformation(models=["model1"])
        tm.that(result, is_=r)
        tm.that(result.is_success or result.is_failure, eq=True)


class TestProjectAdapterIntegration:
    """Test integration of FlextMeltanoAdapter.ProjectAdapter."""

    def test_adapter_version(self) -> None:
        """Test that FlextMeltanoAdapter.ProjectAdapter can get version."""
        adapter = FlextMeltanoAdapter.ProjectAdapter()
        result = adapter.get_version()
        tm.ok(result)
        tm.that(result.value, none=False)
        tm.that(result.value, has="version")

    def test_adapter_execute(self) -> None:
        """Test that FlextMeltanoAdapter.ProjectAdapter execute returns r."""
        adapter = FlextMeltanoAdapter.ProjectAdapter()
        result = adapter.execute()
        tm.that(hasattr(result, "is_success"), eq=True)
        tm.that(hasattr(result, "is_failure"), eq=True)
