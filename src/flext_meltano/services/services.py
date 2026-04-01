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
        return u.try_(
            lambda: FlextMeltanoService(
                service_name=f"{component_name}_service",
                service_version=c.Meltano.Defaults.SERVICE_VERSION,
                **{field_name: component_name},
            ),
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
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
        environment_name: str, config: t.Meltano.MeltanoConfigDict | None = None
    ) -> r[t.Meltano.MeltanoConfigDict]:
        """Configure environment."""
        if not environment_name:
            return r[t.Meltano.MeltanoConfigDict].fail("Environment name is required")
        if environment_name not in c.Meltano.Environments.VALID:
            return r[t.Meltano.MeltanoConfigDict].fail(
                "Invalid environment: "
                f"{environment_name}. "
                f"Valid: {c.Meltano.Environments.VALID}"
            )
        return r[t.Meltano.MeltanoConfigDict].ok(
            u.Meltano.build_status_payload(
                c.Meltano.Enums.OperationStatus.CONFIGURED,
                extra_fields={
                    "environment": environment_name,
                    "configuration": config or {},
                },
            )
        )

    @staticmethod
    def configure_pipeline(
        source_name: str,
        sink_name: str,
        _config: t.Meltano.MeltanoConfigDict | None = None,
    ) -> r[t.Meltano.MeltanoConfigDict]:
        """Configure generic data pipeline."""
        return r[t.Meltano.MeltanoConfigDict].ok(
            u.Meltano.build_status_payload(
                c.Meltano.Enums.OperationStatus.CONFIGURED,
                extra_fields={
                    "source": source_name,
                    "sink": sink_name,
                },
            )
        )

    @staticmethod
    def install_component(
        component_type: str,
        component_name: str,
        config: t.Meltano.MeltanoConfigDict | None = None,
    ) -> r[t.Meltano.MeltanoConfigDict]:
        """Install pipeline component with validation."""
        if not component_type or not component_name:
            return r[t.Meltano.MeltanoConfigDict].fail(
                "Component type and name are required"
            )
        if component_type not in c.Meltano.ComponentTypes.VALID:
            return r[t.Meltano.MeltanoConfigDict].fail(
                f"Invalid component type: {component_type}"
            )
        return r[t.Meltano.MeltanoConfigDict].ok(
            u.Meltano.build_status_payload(
                c.Meltano.Enums.OperationStatus.INSTALLED,
                extra_fields={
                    "component_name": component_name,
                    "component_type": component_type,
                    "configuration": config or {},
                },
            )
        )

    @staticmethod
    def validate_service_config(config: t.Meltano.MeltanoConfigDict) -> r[bool]:
        """Validate service configuration dictionary."""
        if not u.guard(config, dict):
            return r[bool].fail("Configuration must be a dictionary")
        return r[bool].ok(value=True)

    def create_from_config(
        self, config: t.Meltano.MeltanoConfigDict | t.NormalizedValue
    ) -> r[t.Meltano.MeltanoConfigDict]:
        """Create a service instance from configuration."""
        if not isinstance(config, dict):
            return r[t.Meltano.MeltanoConfigDict].fail(
                "Configuration must be a dictionary"
            )
        return r[t.Meltano.MeltanoConfigDict].ok(dict(config))

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute service with railway pattern."""
        return r[t.Meltano.MeltanoConfigDict].ok(
            u.Meltano.build_status_payload(
                c.CommonStatus.ACTIVE,
                extra_fields={
                    "service_name": c.Meltano.Metadata.APPLICATION_NAME,
                    "version": c.Meltano.FLEXT_MELTANO_VERSION,
                    "handlers": list(c.Meltano.Handlers.ALL),
                },
            )
        )

    def get_default_config(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Get default configuration from current settings."""
        return r[t.Meltano.MeltanoConfigDict].ok(
            u.Meltano.coerce_config_mapping(self.settings)
        )

    def get_info(self) -> r[t.Meltano.PluginInfo]:
        """Get service information."""
        return r[t.Meltano.PluginInfo].ok({
            "name": c.Meltano.Metadata.APPLICATION_NAME,
            "version": c.Meltano.FLEXT_MELTANO_VERSION,
            "type": "pipeline_service",
            "description": c.Meltano.Metadata.APPLICATION_DESCRIPTION,
        })

    def get_service_status(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Get service status."""
        return self.execute()

    def get_version_info(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Get version information."""
        return r[t.Meltano.MeltanoConfigDict].ok({
            "api_version": c.Meltano.FLEXT_MELTANO_VERSION,
            "service_name": c.Meltano.Metadata.APPLICATION_NAME,
        })

    def validate_config(self) -> r[bool]:
        """Validate current service configuration."""
        return self.validate_service_config(
            u.Meltano.coerce_config_mapping(self.settings)
        )


__all__ = ["FlextMeltanoService"]
