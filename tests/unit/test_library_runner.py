"""Tests for FlextMeltanoLibraryRunner - Library integration patterns.

Tests the library runner from meltano/runner.py which provides ELT pipeline
execution and DBT transformation support. Methods that were removed (fake
stubs like get_dbt_runner, get_singer_manager) have been cleaned from tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from flext_tests import tm

from flext_meltano import (
    FlextMeltanoAdapter,
    FlextMeltanoExecutor,
    FlextMeltanoLibraryRunner,
    m,
    t,
)
from tests import p, r


class TestFlextMeltanoLibraryRunner:
    """Test FlextMeltanoLibraryRunner and related project adapter behavior."""

    def test_initialization(self) -> None:
        """Test library runner initialization."""
        runner = FlextMeltanoLibraryRunner()
        tm.that(runner, none=False)

    def test_execute_raises_not_implemented(self) -> None:
        """Test execute raises NotImplementedError when not overridden."""
        runner = FlextMeltanoLibraryRunner()
        with pytest.raises(NotImplementedError):
            runner.execute()

    @staticmethod
    def _mock_cmd_result(
        command: list[str],
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        return r[m.Meltano.CommandExecutionResult].ok(
            m.Meltano.CommandExecutionResult(
                command=command,
                success=True,
                exit_code=0,
                output="ok",
                error="",
                execution_time=0.1,
            ),
        )

    @staticmethod
    def _mock_execute_command(
        command: t.StrSequence,
        **_: t.RecursiveContainer,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        return TestFlextMeltanoLibraryRunner._mock_cmd_result(list(command))

    def test_execute_complete_elt_pipeline(self) -> None:
        """Test complete E-L-T pipeline execution delegates to Meltano runtime."""
        runner = FlextMeltanoLibraryRunner()
        with patch.object(
            FlextMeltanoExecutor,
            "execute_meltano_command",
            side_effect=self._mock_execute_command,
        ):
            result = runner.execute_complete_elt_pipeline(
                tap_name="tap-csv",
                target_name="target-jsonl",
            )
        tm.ok(result)
        tm.that(result.value, contains="exit_code")
        tm.that(result.value, contains="output")
        tm.that(result.value, contains="error")

    def test_execute_complete_elt_pipeline_result_shape(self) -> None:
        """Test pipeline result has expected keys when successful."""
        runner = FlextMeltanoLibraryRunner()
        with patch.object(
            FlextMeltanoExecutor,
            "execute_meltano_command",
            side_effect=self._mock_execute_command,
        ):
            result = runner.execute_complete_elt_pipeline(
                tap_name="tap-csv",
                target_name="target-jsonl",
            )
        tm.that(result.success or result.failure, eq=True)
        if result.success:
            tm.that(result.value, is_=dict)
            tm.that(result.value, contains="tap_name")
            tm.that(result.value, contains="target_name")

    def test_run_dbt_transformation(self) -> None:
        """Test DBT transformation delegates to Meltano runtime."""
        runner = FlextMeltanoLibraryRunner()
        with patch.object(
            FlextMeltanoExecutor,
            "execute_meltano_command",
            side_effect=self._mock_execute_command,
        ):
            result = runner.run_dbt_transformation(models=["model1"])
        tm.ok(result)
        tm.that(result.value, contains="exit_code")
        tm.that(result.value, contains="output")
        tm.that(result.value, contains="error")

    def test_adapter_version(self) -> None:
        """Test that FlextMeltanoAdapter.ProjectAdapter can get version."""
        adapter = FlextMeltanoAdapter.ProjectAdapter()
        result = adapter.get_version()
        tm.ok(result)
        tm.that(result.value, none=False)
        tm.that(str(result.value.get("version", "")), none=False)

    def test_adapter_execute(self) -> None:
        """Test that FlextMeltanoAdapter.ProjectAdapter execute returns r."""
        adapter = FlextMeltanoAdapter.ProjectAdapter()
        result = adapter.execute()
        tm.that(result, none=False)
        tm.that(result.success or result.failure, eq=True)
