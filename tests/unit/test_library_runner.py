"""Real-execution tests for the public Meltano library-runner facade."""

from __future__ import annotations

from flext_meltano import meltano


class TestsFlextMeltanoLibraryRunner:
    """Exercise the library-runner mixin through the public Meltano facade."""

    def test_public_facade_exposes_library_runner_methods(self) -> None:
        """The root API exposes the library-runner operations directly."""
        assert callable(meltano.execute_complete_elt_pipeline)
        assert callable(meltano.run_dbt_transformation)
        assert callable(meltano.run_elt_pipeline)

    def test_execute_complete_elt_pipeline_returns_real_payload(self) -> None:
        """Complete ELT execution returns the current public command payload shape."""
        result = meltano.execute_complete_elt_pipeline(
            tap_name="tap-csv",
            target_name="target-jsonl",
        )

        assert result.success
        assert result.value["tap_name"] == "tap-csv"
        assert result.value["target_name"] == "target-jsonl"
        assert isinstance(result.value["exit_code"], int)
        assert "output" in result.value
        assert "error" in result.value

    def test_run_dbt_transformation_returns_real_payload(self) -> None:
        """DBT transformation execution returns the current public command payload shape."""
        result = meltano.run_dbt_transformation(models=["model1"])

        assert result.success
        assert isinstance(result.value["exit_code"], int)
        assert "output" in result.value
        assert "error" in result.value
        assert "models" in result.value
