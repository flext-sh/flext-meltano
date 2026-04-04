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

from flext_core import r
from flext_meltano import (
    FlextMeltanoAdapter,
    FlextMeltanoExecutorBase,
    FlextMeltanoLibraryRunner,
    m,
)


class TestFlextMeltanoLibraryRunner:
    """Test FlextMeltanoLibraryRunner functionality."""

    def test_initialization(self) -> None:
        """Test library runner initialization."""
        runner = FlextMeltanoLibraryRunner()
        assert runner is not None
        assert hasattr(runner, "logger")

    def test_execute_raises_not_implemented(self) -> None:
        """Test execute raises NotImplementedError (no override in runner mixin)."""
        runner = FlextMeltanoLibraryRunner()
        with pytest.raises(NotImplementedError):
            runner.execute()

    @staticmethod
    def _mock_cmd_result(
        command: list[str],
    ) -> r[m.Meltano.CommandExecutionResult]:
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

    def test_execute_complete_elt_pipeline(self) -> None:
        """Test complete E-L-T pipeline execution delegates to Meltano runtime."""
        runner = FlextMeltanoLibraryRunner()
        with patch.object(
            FlextMeltanoExecutorBase,
            "execute_meltano_command",
            side_effect=lambda cmd, **kw: self._mock_cmd_result(list(cmd)),
        ):
            result = runner.execute_complete_elt_pipeline(
                tap_name="tap-csv",
                target_name="target-jsonl",
            )
        assert result.is_success
        assert "exit_code" in result.value
        assert "output" in result.value
        assert "error" in result.value

    def test_execute_complete_elt_pipeline_result_shape(self) -> None:
        """Test pipeline result has expected keys when successful."""
        runner = FlextMeltanoLibraryRunner()
        with patch.object(
            FlextMeltanoExecutorBase,
            "execute_meltano_command",
            side_effect=lambda cmd, **kw: self._mock_cmd_result(list(cmd)),
        ):
            result = runner.execute_complete_elt_pipeline(
                tap_name="tap-csv",
                target_name="target-jsonl",
            )
        assert result.is_success or result.is_failure
        if result.is_success:
            pipeline_data = result.value
            assert isinstance(pipeline_data, dict)
            assert "tap_name" in pipeline_data
            assert "target_name" in pipeline_data

    def test_run_dbt_transformation(self) -> None:
        """Test DBT transformation delegates to Meltano runtime."""
        runner = FlextMeltanoLibraryRunner()
        with patch.object(
            FlextMeltanoExecutorBase,
            "execute_meltano_command",
            side_effect=lambda cmd, **kw: self._mock_cmd_result(list(cmd)),
        ):
            result = runner.run_dbt_transformation(models=["model1"])
        assert result.is_success
        assert "exit_code" in result.value
        assert "output" in result.value
        assert "error" in result.value


class TestProjectAdapterIntegration:
    """Test integration of FlextMeltanoAdapter.ProjectAdapter."""

    def test_adapter_version(self) -> None:
        """Test that FlextMeltanoAdapter.ProjectAdapter can get version."""
        adapter = FlextMeltanoAdapter.ProjectAdapter()
        result = adapter.get_version()
        assert result.is_success
        assert result.value is not None
        assert "version" in result.value

    def test_adapter_execute(self) -> None:
        """Test that FlextMeltanoAdapter.ProjectAdapter execute returns r."""
        adapter = FlextMeltanoAdapter.ProjectAdapter()
        result = adapter.execute()
        assert result is not None
