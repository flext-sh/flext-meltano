"""Public API facade for flext-meltano."""

from __future__ import annotations

from typing import Self, override

from flext_cli import r
from flext_meltano import c, p, t, u
from flext_meltano.services.abstractions import FlextMeltanoAbstractions
from flext_meltano.services.adapters import FlextMeltanoAdapter
from flext_meltano.services.bridge import FlextMeltanoBridge
from flext_meltano.services.consumer_bases.facade import FlextMeltanoConsumerBases
from flext_meltano.services.dbt_project import FlextMeltanoDbtProjectMixin
from flext_meltano.services.dbt_runner import FlextMeltanoDbtRunnerMixin
from flext_meltano.services.executor import FlextMeltanoExecutor
from flext_meltano.services.library_runner import FlextMeltanoLibraryRunner
from flext_meltano.services.meltano_plugins import FlextMeltanoComponentService
from flext_meltano.services.meltano_project_sdk import FlextMeltanoProjectManager
from flext_meltano.services.project_service import FlextMeltanoProjectService
from flext_meltano.services.services import FlextMeltanoService
from flext_meltano.services.singer_catalog import FlextMeltanoSingerCatalogMixin
from flext_meltano.services.singer_state import FlextMeltanoSingerStateMixin
from flext_meltano.services.singer_tap import FlextMeltanoTapAbstractions
from flext_meltano.services.singer_target import FlextMeltanoTargetAbstractions
from flext_meltano.services.singer_translator import FlextMeltanoSingerCliTranslator
from flext_meltano.services.validators import FlextMeltanoValidators


class FlextMeltano(
    FlextMeltanoAbstractions,
    FlextMeltanoAdapter,
    FlextMeltanoBridge,
    FlextMeltanoComponentService,
    FlextMeltanoConsumerBases,
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


meltano: FlextMeltano = FlextMeltano.fetch_global()
"""Shared FlextMeltano facade instance."""


__all__: list[str] = ["FlextMeltano", "meltano"]
