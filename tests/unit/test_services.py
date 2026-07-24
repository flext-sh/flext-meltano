"""Behavioral tests for the public Meltano facade."""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_meltano import meltano
from tests import c

pytestmark = pytest.mark.unit


class TestsFlextMeltanoServices:
    def test_component_factory_returns_specialized_facade(
        self, meltano_component_case: tuple[str, str, str]
    ) -> None:
        """Each public factory returns a specialized facade with the right name."""
        component_kind, component_name, attribute_name = meltano_component_case
        match component_kind:
            case "tap":
                result = meltano.tap(component_name)
            case "target":
                result = meltano.target(component_name)
            case "dbt":
                result = meltano.dbt(component_name)
            case _:
                raise ValueError(
                    f"Unsupported Meltano component kind: {component_kind}"
                )
        tm.that(result, ok=True)
        tm.ok(result)
        service = result.value
        tm.that(service, none=False)
        tm.that(getattr(service, attribute_name), eq=component_name)
        tm.that(service.service_version, eq=c.Meltano.DEFAULT_SERVICE_VERSION)

    @pytest.mark.parametrize(
        ("component_kind", "component_name"),
        [("tap", "tap-postgres"), ("target", "target-postgres"), ("dbt", "warehouse")],
        ids=["tap", "target", "dbt"],
    )
    def test_component_factory_accepts_direct_config(
        self, component_kind: str, component_name: str
    ) -> None:
        """Component factories accept direct settings without wrappers."""
        match component_kind:
            case "tap":
                result = meltano.tap(
                    component_name, host="localhost", database="testdb"
                )
            case "target":
                result = meltano.target(
                    component_name, host="localhost", database="testdb"
                )
            case "dbt":
                result = meltano.dbt(
                    component_name, host="localhost", database="testdb"
                )
            case _:
                raise ValueError(
                    f"Unsupported Meltano component kind: {component_kind}"
                )
        tm.that(result, ok=True)
        tm.ok(result)
        service = result.value
        tm.that(service, none=False)
        tm.that(service.service_name, eq=f"{component_name}_service")

    def test_component_factories_return_distinct_instances(self) -> None:
        """Public component factories never alias the same specialized facade."""
        tap_result = meltano.tap("tap-a")
        target_result = meltano.target("target-a")
        dbt_result = meltano.dbt("dbt-a")
        tm.that(tap_result, ok=True)
        tm.that(target_result, ok=True)
        tm.that(dbt_result, ok=True)
        tm.ok(tap_result)
        tm.ok(target_result)
        tm.ok(dbt_result)
        tap_service = tap_result.value
        target_service = target_result.value
        dbt_service = dbt_result.value
        tm.that(tap_service.source_name, eq="tap-a")
        tm.that(target_service.sink_name, eq="target-a")
        tm.that(dbt_service.transformation_name, eq="dbt-a")
        tm.that(tap_service is not target_service, eq=True)
        tm.that(target_service is not dbt_service, eq=True)
        tm.that(dbt_service is not tap_service, eq=True)

    def test_execute_returns_active_status_payload(self) -> None:
        """execute() reports an active service payload keyed to the facade state."""
        result = meltano.execute()
        tm.that(result, ok=True)
        tm.ok(result)
        payload = result.value
        tm.that(payload["status"], eq="active")
        tm.that(payload["service_name"], eq=meltano.service_name)
        tm.that(payload["version"], eq=meltano.service_version)
        tm.that("timestamp" in payload, eq=True)
        tm.that("handlers" in payload, eq=True)

    def test_execute_is_idempotent_across_calls(self) -> None:
        """Repeated execute() calls yield the same stable public contract."""
        first = meltano.execute()
        second = meltano.execute()
        tm.that(first, ok=True)
        tm.that(second, ok=True)
        tm.ok(first)
        tm.ok(second)
        tm.that(first.value["service_name"], eq=second.value["service_name"])
        tm.that(first.value["version"], eq=second.value["version"])
        tm.that(first.value["handlers"], eq=second.value["handlers"])
