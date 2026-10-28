"""Public API facade for flext-meltano.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from typing import Self, override

from flext_meltano import c, p, r, t, u
from flext_meltano.services import (
    FlextMeltanoAbstractions,
    FlextMeltanoExecutor,
    FlextMeltanoLibraryRunner,
    FlextMeltanoPluginDiscovery,
    FlextMeltanoService,
)
from flext_meltano.services.consumer_bases import FlextMeltanoConsumerBases


class FlextMeltano(
    FlextMeltanoAbstractions,
    FlextMeltanoConsumerBases,
    FlextMeltanoExecutor,
    FlextMeltanoLibraryRunner,
    FlextMeltanoPluginDiscovery,
    FlextMeltanoService,
):
    """MRO facade over all Meltano services. All operations return r[T]."""

    def tap(self, name: str, **settings: t.Scalar) -> p.Result[Self]:
        """Create a specialized Tap facade instance through the public API.

        Returns:
            The resulting ``p.Result[Self]``.

        """
        return self.create_component_service(
            name,
            "source_name",
            "source service",
            settings,
        )

    def target(self, name: str, **settings: t.Scalar) -> p.Result[Self]:
        """Create a specialized Target facade instance through the public API.

        Returns:
            The resulting ``p.Result[Self]``.

        """
        return self.create_component_service(
            name,
            "sink_name",
            "sink service",
            settings,
        )

    def dbt(self, name: str, **settings: t.Scalar) -> p.Result[Self]:
        """Create a specialized DBT facade instance through the public API.

        Returns:
            The resulting ``p.Result[Self]``.

        """
        return self.create_component_service(
            name,
            "transformation_name",
            "transformation service",
            settings,
        )

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute Meltano service with railway pattern.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        handlers_payload: t.JsonValueList = [
            handler.value for handler in c.Meltano.HANDLER_ALL
        ]
        payload: t.JsonDict = {
            c.ContextKey.SERVICE_NAME: self.service_name,
            "version": self.service_version,
            "status": "active",
            "timestamp": u.generate_iso_timestamp(),
            "handlers": handlers_payload,
        }
        return r[t.JsonMapping].ok(payload)


meltano: FlextMeltano = FlextMeltano.fetch_global()
"""Shared FlextMeltano facade instance."""


__all__: list[str] = ["FlextMeltano", "meltano"]
