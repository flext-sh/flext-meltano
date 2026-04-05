"""Public API facade for flext-meltano.

MRO facade over Meltano services. All operations return r[T].

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar, override

from flext_core import r
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
    def get_instance(cls) -> FlextMeltano:
        """Return the shared Meltano facade instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

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
