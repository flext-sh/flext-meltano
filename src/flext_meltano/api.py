"""Public API facade for flext-meltano.

MRO facade over Meltano services (abstractions, adapters, bridge, executor,
file managers, pipeline, project, validators).
All operations return r[T].

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
    FlextMeltanoExecutor,
    FlextMeltanoFileManagers,
    FlextMeltanoProjectService,
    FlextMeltanoService,
    FlextMeltanoValidators,
    c,
    t,
    u,
)


class FlextMeltano(
    FlextMeltanoAbstractions,
    FlextMeltanoAdapter,
    FlextMeltanoBridge,
    FlextMeltanoExecutor,
    FlextMeltanoFileManagers,
    FlextMeltanoProjectService,
    FlextMeltanoService,
    FlextMeltanoValidators,
):
    """Coordinate Meltano operations and expose domain services.

    MRO facade over Meltano services (abstractions, adapters, bridge,
    executor, file managers, pipeline, project, validators).
    All operations return r[T].
    """

    _instance: ClassVar[FlextMeltano | None] = None

    @classmethod
    def get_instance(cls) -> FlextMeltano:
        """Return the shared Meltano facade instance."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute Meltano service with railway pattern."""
        return r[t.Meltano.MeltanoConfigDict].ok({
            "service_name": self.service_name,
            "version": self.service_version,
            "status": c.CommonStatus.ACTIVE.value,
            "timestamp": u.generate_iso_timestamp(),
            "handlers": list(c.Meltano.Handlers.ALL),
        })


meltano = FlextMeltano.get_instance()

__all__ = ["FlextMeltano", "meltano"]
