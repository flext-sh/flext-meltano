"""FLEXT Pipeline Services - Generic service orchestration with flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Self, override

from flext_meltano import FlextMeltanoServiceBase, FlextMeltanoSettings, c, p, r, t, u


class FlextMeltanoService(FlextMeltanoServiceBase):
    """Generic data pipeline service with factory methods."""

    @classmethod
    def _create_specialized_service(
        cls,
        component_name: str,
        *,
        field_name: str,
        component_label: str,
        settings: t.JsonMapping | None = None,
    ) -> p.Result[Self]:
        """Create a specialized Meltano service.

        Pydantic v2 owns every validation step:
        - ``cls.model_validate(payload)`` validates the construction payload
          and raises ``ValidationError`` for unknown ``field_name``;
        - ``FlextMeltanoSettings.model_validate(settings)`` validates the
          runtime settings payload (per-field coercion + type narrowing).

        ``settings`` is typed as ``t.MappingKV[str, object]`` because the
        downstream Pydantic validator handles every concrete value type —
        keeps the signature broad enough for both ``Scalar`` and ``JsonValue``
        callers without manual coercion at the boundary.
        """
        try:
            instance = cls.model_validate({
                "service_name": f"{component_name}_service",
                "service_version": c.Meltano.DEFAULT_SERVICE_VERSION,
                field_name: component_name,
            })
            if settings is not None:
                instance = instance.model_copy(
                    update={
                        "runtime_settings": FlextMeltanoSettings.model_validate(
                            settings,
                        ),
                    },
                )
            return r.ok(instance)
        except c.Meltano.OPERATION_ERRORS as ex:
            return r.fail(
                f"Failed to create {component_label} '{component_name}': {ex}",
            )

    @classmethod
    def create_sink_service(cls, sink_name: str, **config: t.Scalar) -> p.Result[Self]:
        """Create data sink service.

        Pydantic validates ``config`` via ``FlextMeltanoSettings.model_validate``
        inside ``_create_specialized_service``.
        """
        settings_payload: t.JsonDict | None = (
            {key: u.normalize_to_json_value(value) for key, value in config.items()}
            if config
            else None
        )
        return cls._create_specialized_service(
            sink_name,
            field_name="sink_name",
            component_label="sink service",
            settings=settings_payload,
        )

    @classmethod
    def create_source_service(
        cls, source_name: str, **config: t.Scalar
    ) -> p.Result[Self]:
        """Create data source service.

        Pydantic validates ``config`` via ``FlextMeltanoSettings.model_validate``
        inside ``_create_specialized_service``.
        """
        settings_payload: t.JsonDict | None = (
            {key: u.normalize_to_json_value(value) for key, value in config.items()}
            if config
            else None
        )
        return cls._create_specialized_service(
            source_name,
            field_name="source_name",
            component_label="source service",
            settings=settings_payload,
        )

    @classmethod
    def create_transformation_service(
        cls, transformation_name: str, **config: t.Scalar
    ) -> p.Result[Self]:
        """Create transformation service.

        Pydantic validates ``config`` via ``FlextMeltanoSettings.model_validate``
        inside ``_create_specialized_service``.
        """
        settings_payload: t.JsonDict | None = (
            {key: u.normalize_to_json_value(value) for key, value in config.items()}
            if config
            else None
        )
        return cls._create_specialized_service(
            transformation_name,
            field_name="transformation_name",
            component_label="transformation service",
            settings=settings_payload,
        )

    @staticmethod
    def configure_environment(
        environment_name: str, settings: t.JsonMapping | None = None
    ) -> p.Result[t.Meltano.ServicePayload]:
        """Configure environment."""
        if not environment_name:
            return r[t.Meltano.ServicePayload].fail("Environment name is required")
        normalized_environment = str(
            c.Meltano.ENVIRONMENT_ALIASES.get(
                environment_name.strip().lower(),
                environment_name.strip().lower(),
            )
        )
        if normalized_environment not in c.Meltano.ENVIRONMENTS_VALID:
            return r[t.Meltano.ServicePayload].fail(
                "Invalid environment: "
                f"{environment_name}. "
                f"Valid: {c.Meltano.ENVIRONMENTS_VALID}"
            )
        configuration: t.JsonDict = (
            dict(settings.items()) if settings is not None else {}
        )
        payload: t.JsonDict = {
            "status": c.Meltano.OperationStatus.CONFIGURED,
            "environment": normalized_environment,
            "configuration": configuration,
        }
        return r[t.Meltano.ServicePayload].ok(payload)

    @staticmethod
    def configure_pipeline(
        source_name: str,
        sink_name: str,
        config: t.JsonMapping | None = None,
    ) -> p.Result[t.JsonMapping]:
        """Configure generic data pipeline."""
        payload: t.JsonMapping = {
            "status": c.Meltano.OperationStatus.CONFIGURED,
            "source": source_name,
            "sink": sink_name,
            "configuration": (dict(config.items()) if config is not None else {}),
        }
        return r[t.JsonMapping].ok(payload)

    @staticmethod
    def install_component(
        component_type: str,
        component_name: str,
        settings: t.JsonMapping | None = None,
    ) -> p.Result[t.Meltano.ServicePayload]:
        """Install pipeline component with validation."""
        if not component_type or not component_name:
            return r[t.Meltano.ServicePayload].fail(
                "Component type and name are required"
            )
        if component_type not in c.Meltano.COMPONENT_TYPES_VALID:
            return r[t.Meltano.ServicePayload].fail(
                f"Invalid component type: {component_type}"
            )
        configuration: t.JsonDict = (
            dict(settings.items()) if settings is not None else {}
        )
        payload: t.JsonDict = {
            "status": c.Meltano.OperationStatus.INSTALLED,
            "component_name": component_name,
            "component_type": component_type,
            "configuration": configuration,
        }
        return r[t.Meltano.ServicePayload].ok(payload)

    @staticmethod
    def validate_service_config(
        settings: t.JsonMapping,
    ) -> p.Result[bool]:
        """Validate service configuration dictionary."""
        if not isinstance(settings, dict):
            return r[bool].fail("Configuration must be a dictionary")
        return r[bool].ok(value=True)

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute service with railway pattern."""
        handlers_payload: list[t.JsonValue] = [
            handler.value for handler in c.Meltano.HANDLER_ALL
        ]
        payload: t.JsonDict = {
            "status": "active",
            "service_name": c.Meltano.METADATA_APPLICATION_NAME,
            "version": c.Meltano.FLEXT_MELTANO_VERSION,
            "handlers": handlers_payload,
        }
        return r[t.JsonMapping].ok(payload)

    def fetch_default_config(self) -> p.Result[t.JsonMapping]:
        """Get default configuration from current settings."""
        return r[t.JsonMapping].ok(self.settings.model_dump(mode="json"))

    def fetch_info(self) -> p.Result[t.Meltano.OptionalScalarMap]:
        """Get service information."""
        return r[t.Meltano.OptionalScalarMap].ok({
            "name": c.Meltano.METADATA_APPLICATION_NAME,
            "version": c.Meltano.FLEXT_MELTANO_VERSION,
            "type": c.Meltano.ServiceType.PIPELINE,
            "description": c.Meltano.METADATA_APPLICATION_DESCRIPTION,
        })

    def validate_config(self) -> p.Result[bool]:
        """Validate current service configuration."""
        return self.validate_service_config(self.settings.model_dump())


__all__: list[str] = ["FlextMeltanoService"]
