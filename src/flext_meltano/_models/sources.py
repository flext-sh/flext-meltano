"""FLEXT Meltano models - Source and configuration models."""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated, ClassVar, Self

from flext_cli import m, u
from flext_meltano._models.core import FlextMeltanoModelsCore
from flext_meltano._models.sources_params import FlextMeltanoModelsSourcesParams
from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoModelsSources:
    """Source and configuration models."""

    StreamDefinition: ClassVar[
        type[FlextMeltanoModelsSourcesParams.StreamDefinition]
    ] = FlextMeltanoModelsSourcesParams.StreamDefinition

    class TapConfig(m.Entity):
        """Generic tap configuration for data extraction."""

        tap_type: Annotated[str, u.Field(description="Type of the tap")]
        connection_config: Annotated[
            t.JsonMapping, u.Field(description="Connection configuration")
        ]
        stream_config: Annotated[
            t.JsonMapping,
            u.Field(description="Stream-specific configuration"),
        ] = u.Field(default_factory=lambda: MappingProxyType({}))
        tap_version: Annotated[str, u.Field(description="Tap version")] = "latest"

        @u.computed_field()
        @property
        def config_size(self) -> int:
            """Total number of configuration parameters."""
            return u.count(list(self.connection_config.keys())) + u.count(
                list(self.stream_config.keys())
            )

        @u.computed_field()
        @property
        def has_stream_config(self) -> bool:
            """Check if stream configuration is present."""
            return bool(self.stream_config)

        @u.computed_field()
        @property
        def tap_identifier(self) -> str:
            """Unique tap identifier."""
            return f"{self.tap_type}:{self.tap_version}"

        @u.field_serializer("connection_config")
        def serialize_connection_config(self, value: t.JsonMapping) -> t.JsonMapping:
            """Serialize connection settings with sensitive data protection."""
            return FlextMeltanoModelsCore.protect_sensitive_config(value)

        @u.model_validator(mode="after")
        def validate_tap_config(self) -> Self:
            """Validate tap configuration consistency."""
            if not self.tap_type or not self.tap_type.strip():
                msg = "tap_type cannot be empty"
                raise ValueError(msg)
            if not self.connection_config:
                msg = "Connection configuration cannot be empty"
                raise ValueError(msg)
            return self

    class TargetConfig(m.Entity):
        """Generic target configuration for data loading."""

        target_type: Annotated[str, u.Field(description="Type of the target")]
        connection_config: Annotated[
            t.JsonMapping, u.Field(description="Connection configuration")
        ] = u.Field(default_factory=lambda: MappingProxyType({}))
        batch_size: Annotated[
            int | None, u.Field(default=None, description="Batch size for data loading")
        ] = None
        batch_wait_limit: Annotated[
            float | None,
            u.Field(default=None, description="Batch wait limit in seconds"),
        ] = None
        target_version: Annotated[
            str, u.Field(default="latest", description="Target version")
        ] = "latest"

        @u.computed_field()
        @property
        def config_size(self) -> int:
            """Total number of configuration parameters."""
            return len(self.connection_config)

        @u.computed_field()
        @property
        def has_connection_config(self) -> bool:
            """Check if connection configuration is present."""
            return bool(self.connection_config)

        @u.computed_field()
        @property
        def target_identifier(self) -> str:
            """Unique target identifier."""
            return f"{self.target_type}:{self.target_version}"

        @u.field_serializer("connection_config")
        def serialize_connection_config(self, value: t.JsonMapping) -> t.JsonMapping:
            """Serialize connection settings with sensitive data protection."""
            return FlextMeltanoModelsCore.protect_sensitive_config(value)

        @u.model_validator(mode="after")
        def validate_target_config(self) -> Self:
            """Validate target configuration consistency."""
            if not self.target_type or not self.target_type.strip():
                msg = "target_type cannot be empty"
                raise ValueError(msg)
            return self

    class DataSourceConfig(m.Entity):
        """Generic data source configuration with validation."""

        source_type: Annotated[str, u.Field(description="Type of the data source")]
        connection_config: Annotated[
            t.JsonMapping, u.Field(description="Connection configuration")
        ]
        stream_config: Annotated[
            t.JsonMapping,
            u.Field(description="Stream-specific configuration"),
        ] = u.Field(default_factory=lambda: MappingProxyType({}))
        source_version: Annotated[
            str, u.Field(default="latest", description="Source version")
        ] = "latest"

        @u.computed_field()
        @property
        def config_size(self) -> int:
            """Total number of configuration parameters."""
            return u.count(list(self.connection_config.keys())) + u.count(
                list(self.stream_config.keys())
            )

        @u.computed_field()
        @property
        def has_stream_config(self) -> bool:
            """Check if stream configuration is present."""
            return bool(self.stream_config)

        @u.computed_field()
        @property
        def source_identifier(self) -> str:
            """Unique source identifier."""
            return f"{self.source_type}:{self.source_version}"

        @u.field_serializer("connection_config")
        def serialize_connection_config(self, value: t.JsonMapping) -> t.JsonMapping:
            """Serialize connection settings with sensitive data protection."""
            return FlextMeltanoModelsCore.protect_sensitive_config(value)

        @u.model_validator(mode="after")
        def validate_source_config(self) -> Self:
            """Validate source configuration consistency."""
            if not self.source_type or not self.source_type.strip():
                msg = "Source type cannot be empty"
                raise ValueError(msg)
            if not self.connection_config:
                msg = "Connection configuration cannot be empty"
                raise ValueError(msg)
            return self
