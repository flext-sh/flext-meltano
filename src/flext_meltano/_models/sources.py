"""FLEXT Meltano models - Source and configuration models."""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated, ClassVar, Self

from flext_cli import m, u

from flext_meltano import t
from flext_meltano._models.core import FlextMeltanoModelsCore
from flext_meltano._models.sources_params import FlextMeltanoModelsSourcesParams


class FlextMeltanoModelsSources:
    """Source and configuration models."""

    StreamDefinition: ClassVar[
        type[FlextMeltanoModelsSourcesParams.StreamDefinition]
    ] = FlextMeltanoModelsSourcesParams.StreamDefinition

    class TapConfig(m.Entity):
        """Generic tap configuration for data extraction."""

        tap_type: Annotated[str, m.Field(description="Type of the tap")]
        connection_config: Annotated[
            t.FlatContainerMapping, m.Field(description="Connection configuration")
        ]
        stream_config: Annotated[
            t.FlatContainerMapping, m.Field(description="Stream-specific configuration")
        ] = m.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Stream-specific configuration",
        )
        tap_version: Annotated[str, m.Field(description="Tap version")] = "latest"

        @m.computed_field
        def config_size(self) -> int:
            """Total number of configuration parameters."""
            return u.count(list(self.connection_config.keys())) + u.count(
                list(self.stream_config.keys())
            )

        @m.computed_field
        def has_stream_config(self) -> bool:
            """Check if stream configuration is present."""
            return bool(self.stream_config)

        @m.computed_field
        def tap_identifier(self) -> str:
            """Unique tap identifier."""
            return f"{self.tap_type}:{self.tap_version}"

        @u.field_serializer("connection_config")
        def serialize_connection_config(
            self, value: t.FlatContainerMapping
        ) -> t.FlatContainerMapping:
            """Serialize connection config with sensitive data protection."""
            return FlextMeltanoModelsCore.protect_sensitive_config(value)

        @m.field_validator("stream_config", mode="after")
        @classmethod
        def freeze_stream_config(
            cls, value: t.FlatContainerMapping
        ) -> t.FlatContainerMapping:
            """Expose stream configuration as a read-only mapping."""
            return MappingProxyType(dict(value))

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

        target_type: Annotated[str, m.Field(description="Type of the target")]
        connection_config: Annotated[
            t.FlatContainerMapping, m.Field(description="Connection configuration")
        ] = m.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Connection configuration",
        )
        batch_size: Annotated[
            int | None, m.Field(default=None, description="Batch size for data loading")
        ] = None
        batch_wait_limit: Annotated[
            float | None,
            m.Field(default=None, description="Batch wait limit in seconds"),
        ] = None
        target_version: Annotated[
            str, m.Field(default="latest", description="Target version")
        ] = "latest"

        @m.computed_field
        def config_size(self) -> int:
            """Total number of configuration parameters."""
            return len(self.connection_config)

        @m.computed_field
        def has_connection_config(self) -> bool:
            """Check if connection configuration is present."""
            return bool(self.connection_config)

        @m.computed_field
        def target_identifier(self) -> str:
            """Unique target identifier."""
            return f"{self.target_type}:{self.target_version}"

        @u.field_serializer("connection_config")
        def serialize_connection_config(
            self, value: t.FlatContainerMapping
        ) -> t.FlatContainerMapping:
            """Serialize connection config with sensitive data protection."""
            return FlextMeltanoModelsCore.protect_sensitive_config(value)

        @m.field_validator("connection_config", mode="after")
        @classmethod
        def freeze_connection_config(
            cls, value: t.FlatContainerMapping
        ) -> t.FlatContainerMapping:
            """Expose target connection configuration as read-only."""
            return MappingProxyType(dict(value))

        @u.model_validator(mode="after")
        def validate_target_config(self) -> Self:
            """Validate target configuration consistency."""
            if not self.target_type or not self.target_type.strip():
                msg = "target_type cannot be empty"
                raise ValueError(msg)
            return self

    class DataSourceConfig(m.Entity):
        """Generic data source configuration with validation."""

        source_type: Annotated[str, m.Field(description="Type of the data source")]
        connection_config: Annotated[
            t.FlatContainerMapping, m.Field(description="Connection configuration")
        ]
        stream_config: Annotated[
            t.FlatContainerMapping, m.Field(description="Stream-specific configuration")
        ] = m.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Stream-specific configuration",
        )
        source_version: Annotated[
            str, m.Field(default="latest", description="Source version")
        ] = "latest"

        @m.computed_field
        def config_size(self) -> int:
            """Total number of configuration parameters."""
            return u.count(list(self.connection_config.keys())) + u.count(
                list(self.stream_config.keys())
            )

        @m.computed_field
        def has_stream_config(self) -> bool:
            """Check if stream configuration is present."""
            return bool(self.stream_config)

        @m.computed_field
        def source_identifier(self) -> str:
            """Unique source identifier."""
            return f"{self.source_type}:{self.source_version}"

        @u.field_serializer("connection_config")
        def serialize_connection_config(
            self, value: t.FlatContainerMapping
        ) -> t.FlatContainerMapping:
            """Serialize connection config with sensitive data protection."""
            return FlextMeltanoModelsCore.protect_sensitive_config(value)

        @m.field_validator("stream_config", mode="after")
        @classmethod
        def freeze_stream_config(
            cls, value: t.FlatContainerMapping
        ) -> t.FlatContainerMapping:
            """Expose source stream configuration as read-only."""
            return MappingProxyType(dict(value))

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
