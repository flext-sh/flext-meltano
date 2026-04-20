"""Shared service foundation for flext-meltano components.

Centralizes access to configuration singleton while maintaining inheritance
aligned with `s` from flext-core, avoiding duplication of initialization
across library services.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from types import ModuleType
from typing import Annotated, override

from flext_cli import u
from flext_core import FlextSettings, s

from flext_meltano import FlextMeltanoSettings, c, p, t


class FlextMeltanoServiceBase(s[Mapping[str, t.Container]]):
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

    def __init__(
        self,
        settings: FlextSettings | Mapping[str, t.Container] | None = None,
        *,
        settings_type: type[FlextSettings] | None = None,
        initial_context: p.Context | None = None,
        _subproject: str | None = None,
        _services: Mapping[str, t.RegisterableService] | None = None,
        _factories: Mapping[str, t.FactoryCallable] | None = None,
        _resources: Mapping[str, t.ResourceCallable] | None = None,
        _container_overrides: t.ScalarMapping | None = None,
        _wire_modules: Sequence[ModuleType] | None = None,
        _wire_packages: t.StrSequence | None = None,
        _wire_classes: Sequence[type] | None = None,
        service_name: t.NonEmptyStr | None = None,
        service_version: t.NonEmptyStr | None = None,
        source_name: str | None = None,
        sink_name: str | None = None,
        transformation_name: str | None = None,
    ) -> None:
        """Accept canonical settings input and pass typed runtime state forward."""
        runtime_settings = settings if isinstance(settings, FlextSettings) else None
        normalized_overrides: Mapping[str, t.Container] | None = None
        if isinstance(settings, Mapping) and runtime_settings is None:
            normalized_overrides = {str(key): value for key, value in settings.items()}
        super().__init__(
            settings=runtime_settings,
            settings_type=settings_type or FlextMeltanoSettings,
            settings_overrides=normalized_overrides,
            initial_context=initial_context,
        )
        if service_name is not None:
            self.service_name = service_name
        if service_version is not None:
            self.service_version = service_version
        if source_name is not None:
            self.source_name = source_name
        if sink_name is not None:
            self.sink_name = sink_name
        if transformation_name is not None:
            self.transformation_name = transformation_name

    @property
    @override
    def settings(self) -> FlextMeltanoSettings:
        """Return the typed Meltano settings namespace."""
        settings = super().settings
        if not isinstance(settings, FlextMeltanoSettings):
            msg = "Meltano service runtime settings must be FlextMeltanoSettings"
            raise TypeError(msg)
        return settings


s = FlextMeltanoServiceBase
__all__: list[str] = ["FlextMeltanoServiceBase"]
