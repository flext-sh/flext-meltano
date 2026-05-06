"""Shared service foundation for flext-meltano components.

Centralizes access to configuration singleton while maintaining inheritance
aligned with `s` from flext-core, avoiding duplication of initialization
across library services.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated, Self, override

from flext_cli import u
from flext_core import FlextSettings, s
from flext_meltano import FlextMeltanoSettings, c, m, p, t


class FlextMeltanoServiceBase(s[t.JsonMapping]):
    """Base class for flext-meltano services with typed configuration access.

    Note: This is an abstract base class. Subclasses must implement the
    `execute` method from s.
    """

    settings_type: Annotated[
        type | None,
        u.Field(description="Settings class for Meltano service initialization"),
    ] = FlextMeltanoSettings

    service_name: Annotated[
        t.NonEmptyStr,
        u.Field(
            default="flext_meltano_service",
            description="Canonical Meltano service instance name",
        ),
    ] = "flext_meltano_service"
    service_version: Annotated[
        t.NonEmptyStr,
        u.Field(
            default=c.Meltano.DEFAULT_SERVICE_VERSION,
            description="Canonical Meltano service version",
        ),
    ] = c.Meltano.DEFAULT_SERVICE_VERSION
    source_name: Annotated[
        str | None,
        u.Field(default=None, description="Optional source specialization name"),
    ] = None
    sink_name: Annotated[
        str | None,
        u.Field(default=None, description="Optional sink specialization name"),
    ] = None
    transformation_name: Annotated[
        str | None,
        u.Field(
            default=None, description="Optional transformation specialization name"
        ),
    ] = None

    @u.model_validator(mode="before")
    @classmethod
    def _normalize_settings_alias(
        cls,
        data: t.MappingKV[str, t.JsonPayload | p.Base | type | None] | Self,
    ) -> t.MappingKV[str, t.JsonPayload | p.Base | type | None] | Self:
        """Accept ``settings`` as an alias for ``runtime_settings``."""
        if isinstance(data, cls) or not isinstance(data, Mapping):
            return data
        normalized: dict[str, t.JsonPayload | p.Base | type | None] = dict(data)
        settings = normalized.pop("settings", None)
        for field_name in ("service_name", "service_version"):
            if normalized.get(field_name) is None:
                normalized.pop(field_name, None)
        if settings is None or "runtime_settings" in normalized:
            return normalized
        if isinstance(settings, FlextSettings):
            normalized["runtime_settings"] = settings
        elif isinstance(settings, Mapping):
            normalized["runtime_settings"] = FlextMeltanoSettings.model_validate(
                settings
            )
        elif isinstance(settings, m.BaseModel):
            normalized["runtime_settings"] = FlextMeltanoSettings.model_validate(
                settings.model_dump()
            )
        else:
            normalized["runtime_settings"] = FlextMeltanoSettings()
        return normalized

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute the service using the canonical JSON payload contract."""
        raise NotImplementedError

    @property
    @override
    def settings(self) -> FlextMeltanoSettings:
        """Return the typed Meltano settings namespace."""
        if isinstance(self.runtime_settings, FlextMeltanoSettings):
            return self.runtime_settings
        try:
            return FlextMeltanoSettings.fetch_global()
        except ValueError:
            with FlextMeltanoSettings.singleton_disabled():
                return FlextMeltanoSettings()


s = FlextMeltanoServiceBase
__all__: list[str] = ["FlextMeltanoServiceBase"]
