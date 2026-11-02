"""Behavioral tests for the public Meltano library-runner facade.

Exercises the observable contract of ``meltano.run_dbt_transformation`` through
the public facade only: the ``r[T]`` outcome and the typed command-execution
result. No private attributes, collaborators, or internals are touched.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest

from tests import c, meltano, p, tm


@pytest.mark.docker
class TestsFlextMeltanoLibraryRunner:
    """Assert the public library-runner contract via the ``meltano`` facade."""

    # Attributes the typed CommandExecutionResult exposes per the public contract.
    _COMMAND_RESULT_ATTRIBUTES: tuple[str, ...] = (
        c.HandlerMode.COMMAND,
        "success",
        "output",
        "error",
        "exit_code",
        "execution_time",
    )

    @pytest.fixture(scope="class")
    def dbt_result() -> p.Result[p.Meltano.CommandExecutionResult]:
        """Run one DBT transformation once and share its typed outcome.

        Returns:
            The resulting ``p.Result[p.Meltano.CommandExecutionResult]``.

        """
        return meltano.run_dbt_transformation(models=["model1"])

    @staticmethod
    def test_run_dbt_transformation_succeeds(
        dbt_result: p.Result[p.Meltano.CommandExecutionResult],
    ) -> None:
        """A DBT transformation reports a successful ``r[T]`` outcome."""
        tm.ok(dbt_result)

    @staticmethod
    @pytest.mark.parametrize("attribute", _COMMAND_RESULT_ATTRIBUTES)
    def test_dbt_result_exposes_command_execution_fields(
        dbt_result: p.Result[p.Meltano.CommandExecutionResult],
        attribute: str,
    ) -> None:
        """The typed CommandExecutionResult carries every documented field."""
        tm.that(hasattr(dbt_result.unwrap(), attribute), truth=True)

    @staticmethod
    def test_dbt_result_command_targets_requested_models(
        dbt_result: p.Result[p.Meltano.CommandExecutionResult],
    ) -> None:
        """The executed dbt command carries the requested model name."""
        tm.that(dbt_result.unwrap().command, has="model1")
