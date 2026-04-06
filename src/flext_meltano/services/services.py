"""FLEXT Pipeline Services - Generic service orchestration with flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import r
from flext_meltano import FlextMeltanoServiceBase, c, t, u


class FlextMeltanoService(FlextMeltanoServiceBase):
    """Generic data pipeline service with factory methods."""

    @staticmethod
    def _create_specialized_service(
        component_name: str,
        *,
        field_name: str,
        component_label: str,
    ) -> r[FlextMeltanoService]:
        """Create a specialized Meltano service using a shared utility path."""

        def _build() -> FlextMeltanoService:
            kwargs: t.MutableOptionalStrMapping = {
                "service_name": f"{component_name}_service",
                "service_version": c.Meltano.DEFAULT_SERVICE_VERSION,
                "source_name": None,
                "sink_name": None,
                "transformation_name": None,
            }
            kwargs[field_name] = component_name
            return FlextMeltanoService(
                service_name=kwargs["service_name"] or "",
                service_version=kwargs["service_version"] or "",
                source_name=kwargs.get("source_name"),
                sink_name=kwargs.get("sink_name"),
                transformation_name=kwargs.get("transformation_name"),
            )

        return u.try_(
            _build,
            catch=c.Meltano.OPERATION_ERRORS,
        ).map_error(
            lambda ex: f"Failed to create {component_label} '{component_name}': {ex}"
        )

    @staticmethod
    def create_sink_service(
        sink_name: str, **_config: t.Scalar
    ) -> r[FlextMeltanoService]:
        """Create data sink service."""
        return FlextMeltanoService._create_specialized_service(
            sink_name,
            field_name="sink_name",
            component_label="sink service",
        )

    @staticmethod
    def create_source_service(
        source_name: str, **_config: t.Scalar
    ) -> r[FlextMeltanoService]:
        """Create data source service."""
        return FlextMeltanoService._create_specialized_service(
            source_name,
            field_name="source_name",
            component_label="source service",
        )

    @staticmethod
    def create_transformation_service(
        transformation_name: str, **_config: t.Scalar
    ) -> r[FlextMeltanoService]:
        """Create transformation service."""
        return FlextMeltanoService._create_specialized_service(
            transformation_name,
            field_name="transformation_name",
            component_label="transformation service",
        )

    @staticmethod
    def create_dbt_service(name: str, **cfg: t.Scalar) -> r[FlextMeltanoService]:
        """Create DBT transformation service."""
        return FlextMeltanoService.create_transformation_service(name, **cfg)

    @staticmethod
    def create_tap_service(name: str, **cfg: t.Scalar) -> r[FlextMeltanoService]:
        """Create Singer tap service."""
        return FlextMeltanoService.create_source_service(name, **cfg)

    @staticmethod
    def create_target_service(name: str, **cfg: t.Scalar) -> r[FlextMeltanoService]:
        """Create Singer target service."""
        return FlextMeltanoService.create_sink_service(name, **cfg)

    @staticmethod
    def configure_environment(
        environment_name: str, config: t.ContainerMapping | None = None
    ) -> r[t.ContainerMapping]:
        """Configure environment."""
        if not environment_name:
            return r[t.ContainerMapping].fail("Environment name is required")
        if environment_name not in c.Meltano.ENVIRONMENTS_VALID:
            return r[t.ContainerMapping].fail(
                "Invalid environment: "
                f"{environment_name}. "
                f"Valid: {c.Meltano.ENVIRONMENTS_VALID}"
            )
        return r[t.ContainerMapping].ok({
            "status": c.Meltano.OperationStatus.CONFIGURED,
            "environment": environment_name,
            "configuration": config or {},
        })

    @staticmethod
    def configure_pipeline(
        source_name: str,
        sink_name: str,
        _config: t.ContainerMapping | None = None,
    ) -> r[t.ContainerMapping]:
        """Configure generic data pipeline."""
        return r[t.ContainerMapping].ok({
            "status": c.Meltano.OperationStatus.CONFIGURED,
            "source": source_name,
            "sink": sink_name,
        })

    @staticmethod
    def install_component(
        component_type: str,
        component_name: str,
        config: t.ContainerMapping | None = None,
    ) -> r[t.ContainerMapping]:
        """Install pipeline component with validation."""
        if not component_type or not component_name:
            return r[t.ContainerMapping].fail("Component type and name are required")
        if component_type not in c.Meltano.COMPONENT_TYPES_VALID:
            return r[t.ContainerMapping].fail(
                f"Invalid component type: {component_type}"
            )
        return r[t.ContainerMapping].ok({
            "status": c.Meltano.OperationStatus.INSTALLED,
            "component_name": component_name,
            "component_type": component_type,
            "configuration": config or {},
        })

    @staticmethod
    def validate_service_config(config: t.ContainerMapping) -> r[bool]:
        """Validate service configuration dictionary."""
        if not u.guard(config, dict):
            return r[bool].fail("Configuration must be a dictionary")
        return r[bool].ok(value=True)

    @override
    def execute(self) -> r[t.ContainerMapping]:
        """Execute service with railway pattern."""
        return r[t.ContainerMapping].ok({
            "status": c.CommonStatus.ACTIVE,
            "service_name": c.Meltano.METADATA_APPLICATION_NAME,
            "version": c.Meltano.FLEXT_MELTANO_VERSION,
            "handlers": list(c.Meltano.HANDLER_ALL),
        })

    def get_default_config(self) -> r[t.ContainerMapping]:
        """Get default configuration from current settings."""
        return r[t.ContainerMapping].ok(self.settings.model_dump())

    def get_info(self) -> r[t.Meltano.OptionalScalarMap]:
        """Get service information."""
        return r[t.Meltano.OptionalScalarMap].ok({
            "name": c.Meltano.METADATA_APPLICATION_NAME,
            "version": c.Meltano.FLEXT_MELTANO_VERSION,
            "type": "pipeline_service",
            "description": c.Meltano.METADATA_APPLICATION_DESCRIPTION,
        })

    def validate_config(self) -> r[bool]:
        """Validate current service configuration."""
        return self.validate_service_config(self.settings.model_dump())


__all__ = ["FlextMeltanoService"]
