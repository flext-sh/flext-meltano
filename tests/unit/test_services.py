"""Behavioral tests for the public Meltano facade."""

from __future__ import annotations

from collections.abc import Callable

import pytest

from flext_meltano import FlextMeltano, meltano
from tests import c, r, s, u

type ComponentFactory = Callable[..., r[FlextMeltano]]
type ComponentSelector = Callable[[FlextMeltano], str | None]

pytestmark = pytest.mark.unit


def unwrap_component(
    result: r[FlextMeltano],
    *,
    selector: ComponentSelector,
    expected_name: str,
) -> FlextMeltano:
    """Assert and unwrap a public Meltano component facade."""
    u.Tests.Matchers.that(result, ok=True)
    assert result.is_success
    service = result.value
    u.Tests.Matchers.that(service, is_=FlextMeltano)
    u.Tests.Matchers.that(selector(service), eq=expected_name)
    u.Tests.Matchers.that(service.service_version, eq=c.Meltano.DEFAULT_SERVICE_VERSION)
    return service


class TestFlextMeltanoPublicFacade:
    """Behavioral tests for the public Meltano facade."""

    def test_public_singleton_contract(self) -> None:
        """The exported singleton stays stable and inherits the service stack."""
        u.Tests.Matchers.that(meltano, is_=FlextMeltano)
        u.Tests.Matchers.that(type(meltano).get_instance() is meltano, eq=True)
        u.Tests.Matchers.that(s in FlextMeltano.__mro__, eq=True)

    def test_component_factory_returns_specialized_facade(
        self,
        meltano_component_case: tuple[ComponentFactory, str, ComponentSelector],
    ) -> None:
        """Each public factory returns a specialized facade with the right name."""
        factory, component_name, selector = meltano_component_case
        unwrap_component(
            factory(component_name),
            selector=selector,
            expected_name=component_name,
        )

    @pytest.mark.parametrize(
        ("factory", "component_name"),
        [
            (meltano.Tap, "tap-postgres"),
            (meltano.Target, "target-postgres"),
            (meltano.Dbt, "warehouse"),
        ],
        ids=["tap", "target", "dbt"],
    )
    def test_component_factory_accepts_direct_config(
        self,
        factory: ComponentFactory,
        component_name: str,
    ) -> None:
        """Component factories accept direct config without wrappers."""
        result = factory(component_name, host="localhost", database="testdb")
        u.Tests.Matchers.that(result, ok=True)
        assert result.is_success
        service = result.value
        u.Tests.Matchers.that(service, is_=FlextMeltano)
        u.Tests.Matchers.that(service.service_name, eq=f"{component_name}_service")

    def test_component_factories_return_distinct_instances(self) -> None:
        """Public component factories never alias the same specialized facade."""
        tap_service = unwrap_component(
            meltano.Tap("tap-a"),
            selector=lambda service: service.source_name,
            expected_name="tap-a",
        )
        target_service = unwrap_component(
            meltano.Target("target-a"),
            selector=lambda service: service.sink_name,
            expected_name="target-a",
        )
        dbt_service = unwrap_component(
            meltano.Dbt("dbt-a"),
            selector=lambda service: service.transformation_name,
            expected_name="dbt-a",
        )
        u.Tests.Matchers.that(tap_service is not target_service, eq=True)
        u.Tests.Matchers.that(target_service is not dbt_service, eq=True)
        u.Tests.Matchers.that(dbt_service is not tap_service, eq=True)

    def test_component_service_contract(
        self,
        meltano_component_case: tuple[ComponentFactory, str, ComponentSelector],
    ) -> None:
        """Every public component facade keeps the common service contract."""
        factory, component_name, selector = meltano_component_case
        service = unwrap_component(
            factory(component_name),
            selector=selector,
            expected_name=component_name,
        )
        u.Tests.Matchers.that(service.execute(), ok=True)
        u.Tests.Matchers.that(service.validate_config(), ok=True)
        u.Tests.Matchers.that(service.get_info(), ok=True)
        u.Tests.Matchers.that(service.get_default_config(), ok=True)
