"""Shared service foundation for flext-meltano components.

Centralizes access to configuration singleton while maintaining inheritance
aligned with `FlextService` from flext-core, avoiding duplication of initialization
across library services.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, override

from flext_core import FlextSettings, p, s, t
from pydantic import Field

from flext_meltano import FlextMeltanoSettings, c


class FlextMeltanoServiceBase(s[Mapping[str, t.NormalizedValue]]):
    """Base class for flext-meltano services with typed configuration access.

    Note: This is an abstract base class. Subclasses must implement the
    `execute` method from FlextService.
    """

    config_type: type[p.Settings] | None = FlextMeltanoSettings

    service_name: Annotated[
        t.NonEmptyStr,
        Field(
            default="flext_meltano_service",
            description="Canonical Meltano service instance name",
        ),
    ] = "flext_meltano_service"
    service_version: Annotated[
        t.NonEmptyStr,
        Field(
            default=c.Meltano.Defaults.SERVICE_VERSION,
            description="Canonical Meltano service version",
        ),
    ] = c.Meltano.Defaults.SERVICE_VERSION
    source_name: Annotated[
        str | None,
        Field(default=None, description="Optional source specialization name"),
    ] = None
    sink_name: Annotated[
        str | None,
        Field(default=None, description="Optional sink specialization name"),
    ] = None
    transformation_name: Annotated[
        str | None,
        Field(default=None, description="Optional transformation specialization name"),
    ] = None

    @property
    @override
    def settings(self) -> FlextMeltanoSettings:
        """Return the typed Meltano settings namespace."""
        config = self.config
        if isinstance(config, FlextMeltanoSettings):
            return config
        return FlextSettings.get_global().get_namespace(
            "meltano",
            FlextMeltanoSettings,
        )


__all__ = ["FlextMeltanoServiceBase"]
