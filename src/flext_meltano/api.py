"""Public API facade for flext-meltano.

MRO facade over Meltano services. All operations return r[T].

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, Self, override

from flext_core import r
from flext_meltano.constants import FlextMeltanoConstants as c
from flext_meltano.services.abstractions import FlextMeltanoAbstractions
from flext_meltano.services.adapters import FlextMeltanoAdapter
from flext_meltano.services.bridge import FlextMeltanoBridge
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
from flext_meltano.typings import FlextMeltanoTypes as t
from flext_meltano.utilities import FlextMeltanoUtilities as u


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
    def get_instance(cls) -> Self:
        """Return the shared Meltano facade instance."""
        instance = cls._instance
        if instance is None or not isinstance(instance, cls):
            instance = cls()
            cls._instance = instance
        return instance

    def tap(self, name: str, **settings: t.Scalar) -> r[Self]:
        """Create a specialized Tap facade instance through the public API."""
        return type(self).create_source_service(name, **settings)

    def target(self, name: str, **settings: t.Scalar) -> r[Self]:
        """Create a specialized Target facade instance through the public API."""
        return type(self).create_sink_service(name, **settings)

    def dbt(self, name: str, **settings: t.Scalar) -> r[Self]:
        """Create a specialized DBT facade instance through the public API."""
        return type(self).create_transformation_service(name, **settings)

    Tap = tap
    Target = target
    Dbt = dbt

    @override
    def execute(self) -> r[t.ContainerMapping]:
        """Execute Meltano service with railway pattern."""
        return r[t.ContainerMapping].ok({
            "service_name": self.service_name,
            "version": self.service_version,
            "status": c.CommonStatus.ACTIVE.value,
            "timestamp": u.generate_iso_timestamp(),
            "handlers": list(c.Meltano.HANDLER_ALL),
        })


meltano = FlextMeltano.get_instance()


__all__ = ["FlextMeltano", "meltano"]
