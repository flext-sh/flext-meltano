"""FLEXT Pipeline Services - Generic service orchestration with flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Self, override

from flext_meltano import FlextMeltanoServiceBase, c, p, r, t, u


class FlextMeltanoService(FlextMeltanoServiceBase):
    """Generic data pipeline service with factory methods."""

    @classmethod
    def _create_specialized_service(
        cls,
        component_name: str,
        *,
        field_name: str,
        component_label: str,
    ) -> p.Result[Self]:
        """Create a specialized Meltano service using a shared utility path."""
        try:
            service_kwargs: t.MutableOptionalStrMapping = {
                "source_name": None,
                "sink_name": None,
                "transformation_name": None,
            }
            service_kwargs[field_name] = component_name
            return r[Self].ok(
                cls(
                    service_name=f"{component_name}_service",
                    service_version=c.Meltano.DEFAULT_SERVICE_VERSION,
                    source_name=service_kwargs["source_name"],
                    sink_name=service_kwargs["sink_name"],
                    transformation_name=service_kwargs["transformation_name"],
                )
            )
        except c.Meltano.OPERATION_ERRORS as ex:
            return r[Self].fail(
                f"Failed to create {component_label} '{component_name}': {ex}"
            )

    @classmethod
    def create_sink_service(cls, sink_name: str, **_config: t.Scalar) -> p.Result[Self]:
        """Create data sink service."""
        return cls._create_specialized_service(
            sink_name,
            field_name="sink_name",
            component_label="sink service",
        )

    @classmethod
    def create_source_service(
        cls, source_name: str, **_config: t.Scalar
    ) -> p.Result[Self]:
        """Create data source service."""
        return cls._create_specialized_service(
            source_name,
            field_name="source_name",
            component_label="source service",
        )

    @classmethod
    def create_transformation_service(
        cls, transformation_name: str, **_config: t.Scalar
    ) -> p.Result[Self]:
        """Create transformation service."""
        return cls._create_specialized_service(
            transformation_name,
            field_name="transformation_name",
            component_label="transformation service",
        )

    @staticmethod
    def configure_environment(
        environment_name: str, settings: Mapping[str, t.Container] | None = None
    ) -> p.Result[Mapping[str, t.Container]]:
        """Configure environment."""
        if not environment_name:
            return r[Mapping[str, t.Container]].fail("Environment name is required")
        if environment_name not in c.Meltano.ENVIRONMENTS_VALID:
            return r[Mapping[str, t.Container]].fail(
                "Invalid environment: "
                f"{environment_name}. "
                f"Valid: {c.Meltano.ENVIRONMENTS_VALID}"
            )
        payload: Mapping[str, t.Container] = {
            "status": c.Meltano.OperationStatus.CONFIGURED,
            "environment": environment_name,
            "configuration": settings or {},
        }
        return r[Mapping[str, t.Container]].ok(payload)

    @staticmethod
    def configure_pipeline(
        source_name: str,
        sink_name: str,
        _config: Mapping[str, t.Container] | None = None,
    ) -> p.Result[Mapping[str, t.Container]]:
        """Configure generic data pipeline."""
        payload: Mapping[str, t.Container] = {
            "status": c.Meltano.OperationStatus.CONFIGURED,
            "source": source_name,
            "sink": sink_name,
        }
        return r[Mapping[str, t.Container]].ok(payload)

    @staticmethod
    def install_component(
        component_type: str,
        component_name: str,
        settings: Mapping[str, t.Container] | None = None,
    ) -> p.Result[Mapping[str, t.Container]]:
        """Install pipeline component with validation."""
        if not component_type or not component_name:
            return r[Mapping[str, t.Container]].fail(
                "Component type and name are required"
            )
        if component_type not in c.Meltano.COMPONENT_TYPES_VALID:
            return r[Mapping[str, t.Container]].fail(
                f"Invalid component type: {component_type}"
            )
        payload: Mapping[str, t.Container] = {
            "status": c.Meltano.OperationStatus.INSTALLED,
            "component_name": component_name,
            "component_type": component_type,
            "configuration": settings or {},
        }
        return r[Mapping[str, t.Container]].ok(payload)

    @staticmethod
    def validate_service_config(
        settings: Mapping[str, t.Container],
    ) -> p.Result[bool]:
        """Validate service configuration dictionary."""
        if not u.guard(settings, dict):
            return r[bool].fail("Configuration must be a dictionary")
        return r[bool].ok(value=True)

    @override
    def execute(self) -> p.Result[Mapping[str, t.Container]]:
        """Execute service with railway pattern."""
        payload: Mapping[str, t.Container] = {
            "status": c.CommonStatus.ACTIVE,
            "service_name": c.Meltano.METADATA_APPLICATION_NAME,
            "version": c.Meltano.FLEXT_MELTANO_VERSION,
            "handlers": list(c.Meltano.HANDLER_ALL),
        }
        return r[Mapping[str, t.Container]].ok(payload)

    def fetch_default_config(self) -> p.Result[Mapping[str, t.Container]]:
        """Get default configuration from current settings."""
        return r[Mapping[str, t.Container]].ok(self.settings.model_dump())

    def fetch_info(self) -> p.Result[t.Meltano.OptionalScalarMap]:
        """Get service information."""
        return r[t.Meltano.OptionalScalarMap].ok({
            "name": c.Meltano.METADATA_APPLICATION_NAME,
            "version": c.Meltano.FLEXT_MELTANO_VERSION,
            "type": "pipeline_service",
            "description": c.Meltano.METADATA_APPLICATION_DESCRIPTION,
        })

    def validate_config(self) -> p.Result[bool]:
        """Validate current service configuration."""
        return self.validate_service_config(self.settings.model_dump())


__all__: list[str] = ["FlextMeltanoService"]
