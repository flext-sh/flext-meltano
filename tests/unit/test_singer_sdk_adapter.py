"""Tests for the flat public Meltano component factories."""

from __future__ import annotations

from flext_meltano import meltano


class TestsFlextMeltanoSingerSdkAdapter:
    """Validate the current public tap/target/dbt factory surface."""

    def test_tap_factory_returns_specialized_facade(self) -> None:
        """The public tap factory returns a facade bound to the requested source."""
        result = meltano.tap("tap-csv")

        assert result.success
        assert result.value.source_name == "tap-csv"
        assert result.value.sink_name is None
        assert result.value.transformation_name is None

    def test_target_factory_returns_specialized_facade(self) -> None:
        """The public target factory returns a facade bound to the requested sink."""
        result = meltano.target("target-jsonl")

        assert result.success
        assert result.value.source_name is None
        assert result.value.sink_name == "target-jsonl"
        assert result.value.transformation_name is None

    def test_dbt_factory_returns_specialized_facade(self) -> None:
        """The public dbt factory returns a facade bound to the requested transformation."""
        result = meltano.dbt("analytics")

        assert result.success
        assert result.value.source_name is None
        assert result.value.sink_name is None
        assert result.value.transformation_name == "analytics"
