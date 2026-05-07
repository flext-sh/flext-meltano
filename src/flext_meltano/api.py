"""Public API facade for flext-meltano."""

from __future__ import annotations

from typing import Self, override

from flext_cli import r
from flext_meltano import (
    FlextMeltanoAbstractions,
    FlextMeltanoAdapter,
    FlextMeltanoBridge,
    FlextMeltanoComponentService,
    FlextMeltanoDbtProjectMixin,
    FlextMeltanoDbtRunnerMixin,
    FlextMeltanoExecutor,
    FlextMeltanoLibraryRunner,
    FlextMeltanoProjectManager,
    FlextMeltanoProjectService,
    FlextMeltanoService,
    FlextMeltanoSingerCatalogMixin,
    FlextMeltanoSingerCliTranslator,
    FlextMeltanoSingerStateMixin,
    FlextMeltanoTapAbstractions,
    FlextMeltanoTargetAbstractions,
    FlextMeltanoValidators,
    c,
    p,
    t,
    u,
)


class FlextMeltano(
    FlextMeltanoAbstractions,
    FlextMeltanoAdapter,
    FlextMeltanoBridge,
    FlextMeltanoComponentService,
    FlextMeltanoDbtProjectMixin,
    FlextMeltanoDbtRunnerMixin,
    FlextMeltanoExecutor,
    FlextMeltanoLibraryRunner,
    FlextMeltanoProjectManager,
    FlextMeltanoProjectService,
    FlextMeltanoService,
    FlextMeltanoSingerCatalogMixin,
    FlextMeltanoSingerCliTranslator,
    FlextMeltanoSingerStateMixin,
    FlextMeltanoTapAbstractions,
    FlextMeltanoTargetAbstractions,
    FlextMeltanoValidators,
):
    """MRO facade over all Meltano services. All operations return r[T]."""

    def tap(self, name: str, **settings: t.Scalar) -> p.Result[Self]:
        """Create a specialized Tap facade instance through the public API."""
        return type(self).create_source_service(name, **settings)

    def target(self, name: str, **settings: t.Scalar) -> p.Result[Self]:
        """Create a specialized Target facade instance through the public API."""
        return type(self).create_sink_service(name, **settings)

    def dbt(self, name: str, **settings: t.Scalar) -> p.Result[Self]:
        """Create a specialized DBT facade instance through the public API."""
        return type(self).create_transformation_service(name, **settings)

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute Meltano service with railway pattern."""
        handlers_payload: t.JsonValueList = [
            handler.value for handler in c.Meltano.HANDLER_ALL
        ]
        payload: t.JsonDict = {
            "service_name": self.service_name,
            "version": self.service_version,
            "status": "active",
            "timestamp": u.generate_iso_timestamp(),
            "handlers": handlers_payload,
        }
        return r[t.JsonMapping].ok(payload)


meltano = FlextMeltano.fetch_global()


__all__: list[str] = ["FlextMeltano", "meltano"]
