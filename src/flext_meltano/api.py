"""Public API facade for flext-meltano.

MRO facade over Meltano services. All operations return r[T].

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Self, override

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
    # Singer domain
    FlextMeltanoSingerCatalogMixin,
    FlextMeltanoSingerStateMixin,
    FlextMeltanoTapAbstractions,
    FlextMeltanoTargetAbstractions,
    FlextMeltanoSingerCliTranslator,
    # DBT domain
    FlextMeltanoDbtProjectMixin,
    FlextMeltanoDbtRunnerMixin,
    # Meltano SDK + component management
    FlextMeltanoComponentService,
    FlextMeltanoProjectManager,
    FlextMeltanoLibraryRunner,
    # Meltano runtime
    FlextMeltanoAbstractions,
    FlextMeltanoAdapter,
    FlextMeltanoBridge,
    FlextMeltanoExecutor,
    FlextMeltanoProjectService,
    FlextMeltanoService,
    FlextMeltanoValidators,
):
    """MRO facade over all Meltano services. All operations return r[T]."""

    _instance: ClassVar[FlextMeltano | None] = None

    @classmethod
    def fetch_instance(cls) -> Self:
        """Return the shared Meltano facade instance."""
        instance = cls._instance
        if instance is None or not isinstance(instance, cls):
            instance = cls()
            cls._instance = instance
        return instance

    def tap(self, name: str, **settings: t.Scalar) -> p.Result[Self]:
        """Create a specialized Tap facade instance through the public API."""
        return type(self).create_source_service(name, **settings)

    def target(self, name: str, **settings: t.Scalar) -> p.Result[Self]:
        """Create a specialized Target facade instance through the public API."""
        return type(self).create_sink_service(name, **settings)

    def dbt(self, name: str, **settings: t.Scalar) -> p.Result[Self]:
        """Create a specialized DBT facade instance through the public API."""
        return type(self).create_transformation_service(name, **settings)

    Tap = tap
    Target = target
    Dbt = dbt

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute Meltano service with railway pattern."""
        payload: t.JsonMapping = {
            "service_name": self.service_name,
            "version": self.service_version,
            "status": c.CommonStatus.ACTIVE.value,
            "timestamp": u.generate_iso_timestamp(),
            "handlers": list(c.Meltano.HANDLER_ALL),
        }
        return r[t.JsonMapping].ok(payload)


meltano = FlextMeltano.fetch_instance()


__all__: list[str] = ["FlextMeltano", "meltano"]
