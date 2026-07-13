"""Behavioral tests for the flat public Meltano component factories.

Exercises the observable contract of ``FlextMeltano.tap`` / ``.target`` / ``.dbt``
through the public ``meltano`` facade only: the returned ``r[T]`` outcome, the
public role fields, the derived ``service_name``, instance independence, and the
absence of side effects on the shared singleton. No private state is inspected.
"""

from __future__ import annotations

import pytest

from flext_meltano import meltano
from flext_meltano.api import FlextMeltano

__all__ = ["TestsFlextMeltanoSingerSdkAdapter"]


class TestsFlextMeltanoSingerSdkAdapter:
    """Validate the public tap/target/dbt factory contract."""

    def test_tap_factory_binds_source_role_only(self) -> None:
        """The tap factory succeeds and binds only the source role."""
        result = meltano.tap("tap-csv")

        assert result.success
        facade = result.unwrap()
        assert facade.source_name == "tap-csv"
        assert facade.sink_name is None
        assert facade.transformation_name is None

    def test_target_factory_binds_sink_role_only(self) -> None:
        """The target factory succeeds and binds only the sink role."""
        result = meltano.target("target-jsonl")

        assert result.success
        facade = result.unwrap()
        assert facade.source_name is None
        assert facade.sink_name == "target-jsonl"
        assert facade.transformation_name is None

    def test_dbt_factory_binds_transformation_role_only(self) -> None:
        """The dbt factory succeeds and binds only the transformation role."""
        result = meltano.dbt("analytics")

        assert result.success
        facade = result.unwrap()
        assert facade.source_name is None
        assert facade.sink_name is None
        assert facade.transformation_name == "analytics"

    @pytest.mark.parametrize(
        ("factory", "name", "role_field"),
        [
            ("tap", "tap-csv", "source_name"),
            ("target", "target-jsonl", "sink_name"),
            ("dbt", "analytics", "transformation_name"),
        ],
    )
    def test_factory_derives_service_name_from_component_name(
        self,
        factory: str,
        name: str,
        role_field: str,
    ) -> None:
        """Each factory derives ``<name>_service`` as the public service name."""
        result = getattr(meltano, factory)(name)

        facade = result.unwrap()
        assert facade.service_name == f"{name}_service"
        assert getattr(facade, role_field) == name

    @pytest.mark.parametrize(
        ("factory", "name", "role_field"),
        [
            ("tap", "tap-csv", "source_name"),
            ("target", "target-jsonl", "sink_name"),
            ("dbt", "analytics", "transformation_name"),
        ],
    )
    def test_factory_role_field_survives_public_model_dump(
        self,
        factory: str,
        name: str,
        role_field: str,
    ) -> None:
        """The bound role and the two cleared roles appear in the public dump."""
        facade = getattr(meltano, factory)(name).unwrap()

        dumped = facade.model_dump()
        role_fields = {"source_name", "sink_name", "transformation_name"}
        assert dumped[role_field] == name
        assert all(dumped[other] is None for other in role_fields - {role_field})

    def test_factory_returns_new_facade_distinct_from_singleton(self) -> None:
        """The factory yields a fresh facade, never the shared singleton."""
        facade = meltano.tap("tap-csv").unwrap()

        assert isinstance(facade, FlextMeltano)
        assert facade is not meltano

    def test_factories_produce_independent_facades(self) -> None:
        """Building a target does not mutate a previously built tap facade."""
        tap_facade = meltano.tap("tap-csv").unwrap()

        target_facade = meltano.target("target-jsonl").unwrap()

        assert target_facade is not tap_facade
        assert tap_facade.source_name == "tap-csv"
        assert tap_facade.sink_name is None

    def test_factory_does_not_mutate_shared_singleton(self) -> None:
        """Specializing a component leaves the shared facade's roles unbound."""
        meltano.tap("tap-csv")
        meltano.target("target-jsonl")
        meltano.dbt("analytics")

        assert meltano.source_name is None
        assert meltano.sink_name is None
        assert meltano.transformation_name is None

    @pytest.mark.parametrize(
        ("factory", "name"),
        [
            ("tap", "tap-csv"),
            ("target", "target-jsonl"),
            ("dbt", "analytics"),
        ],
    )
    def test_factory_is_idempotent_across_repeated_calls(
        self,
        factory: str,
        name: str,
    ) -> None:
        """Repeated calls yield equal public state on distinct instances."""
        first = getattr(meltano, factory)(name).unwrap()
        second = getattr(meltano, factory)(name).unwrap()

        assert first is not second
        assert first.model_dump() == second.model_dump()
