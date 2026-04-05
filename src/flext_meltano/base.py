"""Shared service foundation for flext-meltano components.

Centralizes access to configuration singleton while maintaining inheritance
aligned with `FlextService` from flext-core, avoiding duplication of initialization
across library services.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from types import ModuleType
from typing import Annotated, override

from pydantic import Field

from flext_core import FlextService
from flext_meltano import FlextMeltanoSettings, c, p, t


class FlextMeltanoServiceBase(FlextService[t.ContainerMapping]):
    """Base class for flext-meltano services with typed configuration access.

    Note: This is an abstract base class. Subclasses must implement the
    `execute` method from FlextService.
    """

    config_type: type | None = Field(
        default=FlextMeltanoSettings,
        description="Configuration class for Meltano service initialization",
    )

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
            default=c.Meltano.DEFAULT_SERVICE_VERSION,
            description="Canonical Meltano service version",
        ),
    ] = c.Meltano.DEFAULT_SERVICE_VERSION
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

    def __init__(
        self,
        /,
        config: FlextMeltanoSettings | t.ContainerMapping | None = None,
        *,
        config_type: type[p.Settings] | None = None,
        config_overrides: t.ContainerMapping | None = None,
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
        """Accept canonical `config` input and map it to service overrides."""
        normalized_overrides = config_overrides
        if normalized_overrides is None and config is not None:
            normalized_overrides = (
                config.model_dump()
                if isinstance(config, FlextMeltanoSettings)
                else {str(key): value for key, value in config.items()}
            )
        super().__init__(
            config_type=config_type,
            config_overrides=normalized_overrides,
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
        config = self.config
        if isinstance(config, FlextMeltanoSettings):
            return config
        empty_overrides: t.MutableContainerMapping = {}
        normalized_overrides: t.MutableContainerMapping = (
            {str(key): value for key, value in self.config_overrides.items()}
            if self.config_overrides
            else empty_overrides
        )
        return FlextMeltanoSettings.model_validate(normalized_overrides)


s = FlextMeltanoServiceBase
__all__ = ["FlextMeltanoServiceBase"]
