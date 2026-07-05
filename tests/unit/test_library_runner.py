"""Behavioral tests for the public Meltano library-runner facade.

Exercises the observable contract of ``meltano.execute_complete_elt_pipeline``,
``meltano.run_dbt_transformation`` and ``meltano.run_elt_pipeline`` through the
public facade only: the ``r[T]`` outcome and the documented command-execution
payload shape. No private attributes, collaborators, or internals are touched.
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

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


class TestsFlextMeltanoLibraryRunner:
    """Assert the public library-runner contract via the ``meltano`` facade."""

    @pytest.fixture(scope="class")
    def elt_result(self) -> p.Result[t.JsonMapping]:
        """Run one complete ELT pipeline once and share its outcome."""
        return meltano.execute_complete_elt_pipeline(
            tap_name="tap-csv",
            target_name="target-jsonl",
        )

    @pytest.fixture(scope="class")
    def dbt_result(self) -> p.Result[t.JsonMapping]:
        """Run one DBT transformation once and share its outcome."""
        return meltano.run_dbt_transformation(models=["model1"])

    @pytest.fixture(scope="class")
    def elt_pipeline_result(self) -> p.Result[t.JsonMapping]:
        """Run one tap-to-target ELT pipeline once and share its outcome.

        Singer tap/target are genuine external plugin boundaries, so a
        ``Mock(spec=...)`` carrying only the public ``name`` used by the
        contract is the correct seam here.
        """
        tap = Mock(spec=p.Meltano.SingerTap)
        tap.name = "tap-csv"
        target = Mock(spec=p.Meltano.SingerTarget)
        target.name = "target-jsonl"
        return meltano.run_elt_pipeline(tap, target)

    def test_facade_exposes_library_runner_operations(self) -> None:
        """The public facade exposes the three library-runner operations."""
        assert callable(meltano.execute_complete_elt_pipeline)
        assert callable(meltano.run_dbt_transformation)
        assert callable(meltano.run_elt_pipeline)

    def test_execute_complete_elt_pipeline_succeeds(
        self,
        elt_result: p.Result[t.JsonMapping],
    ) -> None:
        """A complete ELT run reports a successful ``r[T]`` outcome."""
        assert elt_result.success
        assert elt_result.failure is False

    @pytest.mark.parametrize("key", _BASE_PAYLOAD_KEYS)
    def test_elt_payload_exposes_base_command_keys(
        self,
        elt_result: p.Result[t.JsonMapping],
        key: str,
    ) -> None:
        """The ELT payload carries every documented command-execution field."""
        assert key in elt_result.unwrap()

    def test_elt_payload_echoes_pipeline_identity(
        self,
        elt_result: p.Result[t.JsonMapping],
    ) -> None:
        """The ELT payload echoes the requested tap and target identity."""
        payload = elt_result.unwrap()
        assert payload["tap_name"] == "tap-csv"
        assert payload["target_name"] == "target-jsonl"

    def test_elt_payload_exit_code_is_int(
        self,
        elt_result: p.Result[t.JsonMapping],
    ) -> None:
        """Exit code is delivered as an integer, ready for callers to branch."""
        assert isinstance(elt_result.unwrap()["exit_code"], int)

    def test_elt_result_supports_result_combinators(
        self,
        elt_result: p.Result[t.JsonMapping],
    ) -> None:
        """The outcome is a real ``r[T]`` value that chains via ``map``."""
        exit_code = elt_result.map(lambda payload: payload["exit_code"]).unwrap()
        assert isinstance(exit_code, int)

    def test_run_dbt_transformation_succeeds(
        self,
        dbt_result: p.Result[t.JsonMapping],
    ) -> None:
        """A DBT transformation reports a successful ``r[T]`` outcome."""
        assert dbt_result.success

    @pytest.mark.parametrize("key", _BASE_PAYLOAD_KEYS)
    def test_dbt_payload_exposes_base_command_keys(
        self,
        dbt_result: p.Result[t.JsonMapping],
        key: str,
    ) -> None:
        """The DBT payload carries every documented command-execution field."""
        assert key in dbt_result.unwrap()

    def test_dbt_payload_reports_requested_models(
        self,
        dbt_result: p.Result[t.JsonMapping],
    ) -> None:
        """The DBT payload reports the models joined into its ``models`` field."""
        payload = dbt_result.unwrap()
        assert "models" in payload
        assert payload["models"] == "model1"

    def test_run_elt_pipeline_succeeds_and_echoes_identity(
        self,
        elt_pipeline_result: p.Result[t.JsonMapping],
    ) -> None:
        """A tap-to-target ELT run succeeds and echoes tap/target names."""
        assert elt_pipeline_result.success
        payload = elt_pipeline_result.unwrap()
        assert payload["tap_name"] == "tap-csv"
        assert payload["target_name"] == "target-jsonl"

    @pytest.mark.parametrize("key", _BASE_PAYLOAD_KEYS)
    def test_elt_pipeline_payload_exposes_base_command_keys(
        self,
        elt_pipeline_result: p.Result[t.JsonMapping],
        key: str,
    ) -> None:
        """The tap-to-target payload carries every documented command field."""
        assert key in elt_pipeline_result.unwrap()


__all__: list[str] = ["TestsFlextMeltanoLibraryRunner"]
