"""Behavioral tests for the public Meltano library-runner facade.

Exercises the observable contract of ``meltano.execute_complete_elt_pipeline``,
``meltano.run_dbt_transformation`` and ``meltano.run_elt_pipeline`` through the
public facade only: the ``r[T]`` outcome and the documented command-execution
payload shape. No private attributes, collaborators, or internals are touched.
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_meltano import meltano, p, t

# Keys every command-execution payload must expose per the public contract
# (u.Meltano.build_command_execution_payload): status/success/output/error/
# exit_code plus the execution_time duration field.
_BASE_PAYLOAD_KEYS: tuple[str, ...] = (
    "status",
    "success",
    "output",
    "error",
    "exit_code",
    "execution_time",
)

# Attributes the typed CommandExecutionResult exposes per the public contract.
_COMMAND_RESULT_ATTRIBUTES: tuple[str, ...] = (
    "command",
    "success",
    "output",
    "error",
    "exit_code",
    "execution_time",
)


class TestsFlextMeltanoLibraryRunner:
    """Assert the public library-runner contract via the ``meltano`` facade."""

    @pytest.fixture(scope="class")
    @staticmethod
    def elt_result() -> p.Result[t.JsonMapping]:
        """Run one complete ELT pipeline once and share its outcome."""
        return meltano.execute_complete_elt_pipeline(
            tap_name="tap-csv", target_name="target-jsonl"
        )

    @pytest.fixture(scope="class")
    @staticmethod
    def dbt_result() -> p.Result[p.Meltano.CommandExecutionResult]:
        """Run one DBT transformation once and share its typed outcome."""
        return meltano.run_dbt_transformation(models=["model1"])

    @pytest.fixture(scope="class")
    @staticmethod
    def elt_pipeline_result() -> p.Result[t.JsonMapping]:
        """Run one tap-to-target ELT pipeline once and share its outcome."""
        return meltano.run_elt_pipeline("tap-csv", "target-jsonl")

    def test_facade_exposes_library_runner_operations(self) -> None:
        """The public facade exposes the three library-runner operations."""
        assert callable(meltano.execute_complete_elt_pipeline)
        assert callable(meltano.run_dbt_transformation)
        assert callable(meltano.run_elt_pipeline)

    def test_execute_complete_elt_pipeline_succeeds(
        self, elt_result: p.Result[t.JsonMapping]
    ) -> None:
        """A complete ELT run reports a successful ``r[T]`` outcome."""
        tm.ok(elt_result)
        tm.that(elt_result.failure, eq=False)

    @pytest.mark.parametrize("key", _BASE_PAYLOAD_KEYS)
    def test_elt_payload_exposes_base_command_keys(
        self, elt_result: p.Result[t.JsonMapping], key: str
    ) -> None:
        """The ELT payload carries every documented command-execution field."""
        tm.that(elt_result.unwrap(), has=key)

    def test_elt_payload_echoes_pipeline_identity(
        self, elt_result: p.Result[t.JsonMapping]
    ) -> None:
        """The ELT payload echoes the requested tap and target identity."""
        payload = elt_result.unwrap()
        tm.that(payload["tap_name"], eq="tap-csv")
        tm.that(payload["target_name"], eq="target-jsonl")

    def test_elt_payload_exit_code_is_int(
        self, elt_result: p.Result[t.JsonMapping]
    ) -> None:
        """Exit code is delivered as an integer, ready for callers to branch."""
        tm.that(elt_result.unwrap()["exit_code"], is_=int)

    def test_elt_result_supports_result_combinators(
        self, elt_result: p.Result[t.JsonMapping]
    ) -> None:
        """The outcome is a real ``r[T]`` value that chains via ``map``."""
        exit_code = elt_result.map(lambda payload: payload["exit_code"]).unwrap()
        tm.that(exit_code, is_=int)

    def test_run_dbt_transformation_succeeds(
        self, dbt_result: p.Result[p.Meltano.CommandExecutionResult]
    ) -> None:
        """A DBT transformation reports a successful ``r[T]`` outcome."""
        tm.ok(dbt_result)

    @pytest.mark.parametrize("attribute", _COMMAND_RESULT_ATTRIBUTES)
    def test_dbt_result_exposes_command_execution_fields(
        self, dbt_result: p.Result[p.Meltano.CommandExecutionResult], attribute: str
    ) -> None:
        """The typed CommandExecutionResult carries every documented field."""
        assert hasattr(dbt_result.unwrap(), attribute)

    def test_dbt_result_command_targets_requested_models(
        self, dbt_result: p.Result[p.Meltano.CommandExecutionResult]
    ) -> None:
        """The executed dbt command carries the requested model name."""
        tm.that(dbt_result.unwrap().command, has="model1")

    def test_run_elt_pipeline_succeeds_and_echoes_identity(
        self, elt_pipeline_result: p.Result[t.JsonMapping]
    ) -> None:
        """A tap-to-target ELT run succeeds and echoes tap/target names."""
        tm.ok(elt_pipeline_result)
        payload = elt_pipeline_result.unwrap()
        tm.that(payload["tap_name"], eq="tap-csv")
        tm.that(payload["target_name"], eq="target-jsonl")

    @pytest.mark.parametrize("key", _BASE_PAYLOAD_KEYS)
    def test_elt_pipeline_payload_exposes_base_command_keys(
        self, elt_pipeline_result: p.Result[t.JsonMapping], key: str
    ) -> None:
        """The tap-to-target payload carries every documented command field."""
        tm.that(elt_pipeline_result.unwrap(), has=key)


__all__: list[str] = ["TestsFlextMeltanoLibraryRunner"]
