"""FLEXT Meltano models - Source and configuration models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated, Self

from flext_cli import m

from flext_meltano import t
from flext_meltano._models import FlextMeltanoModelsCore


class FlextMeltanoModelsSources:
    """Source and configuration models."""

    class TapConfig(
        FlextMeltanoModelsCore.SensitiveConfigSerializer,
        m.Entity,
    ):
        """Generic tap configuration for data extraction."""

        connection_config: Annotated[
            t.FlatContainerMapping,
            m.Field(description="Connection configuration"),
        ]
        stream_config: Annotated[
            t.FlatContainerMapping,
            m.Field(description="Stream-specific configuration"),
        ] = m.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
            description="Stream-specific configuration",
        )
        tap_type: Annotated[str, m.Field(description="Type of the tap")]
        tap_version: Annotated[str, m.Field(description="Tap version")] = "latest"

        @m.field_validator("stream_config", mode="after")
        @classmethod
        def freeze_stream_config(
            cls,
            value: t.FlatContainerMapping,
        ) -> t.FlatContainerMapping:
            """Expose stream configuration as a read-only mapping.

            Args:
                value: The validated stream configuration mapping.

            Returns:
                The resulting ``t.FlatContainerMapping``.

            """
            return MappingProxyType(dict(value))

        @m.model_validator(mode="after")
        def validate_tap_config(self) -> Self:
            """Validate tap configuration consistency.

            Returns:
                The resulting ``Self``.

            Raises:
                ValueError: If the tap type is empty, or the connection configuration
                    is empty.

            """
            if not self.tap_type or not self.tap_type.strip():
                msg = "tap_type cannot be empty"
                raise ValueError(msg)
            if not self.connection_config:
                msg = "Connection configuration cannot be empty"
                raise ValueError(msg)
            return self

    class TargetConfig(
        FlextMeltanoModelsCore.SensitiveConfigSerializer,
        m.Entity,
    ):
        """Generic target configuration for data loading."""

        target_type: Annotated[str, m.Field(description="Type of the target")]
        connection_config: Annotated[
            t.FlatContainerMapping,
            m.Field(description="Connection configuration"),
        ] = m.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
            description="Connection configuration",
        )
        batch_size: Annotated[
            int | None,
            m.Field(default=None, description="Batch size for data loading"),
        ] = None
        batch_wait_limit: Annotated[
            float | None,
            m.Field(default=None, description="Batch wait limit in seconds"),
        ] = None
        target_version: Annotated[
            str,
            m.Field(default="latest", description="Target version"),
        ] = "latest"

        @m.field_validator("connection_config", mode="after")
        @classmethod
        def freeze_connection_config(
            cls,
            value: t.FlatContainerMapping,
        ) -> t.FlatContainerMapping:
            """Expose target connection configuration as read-only.

            Args:
                value: The validated connection configuration mapping.

            Returns:
                The resulting ``t.FlatContainerMapping``.

            """
            return MappingProxyType(dict(value))

        @m.model_validator(mode="after")
        def validate_target_config(self) -> Self:
            """Validate target configuration consistency.

            Returns:
                The resulting ``Self``.

            Raises:
                ValueError: If the target type is empty.

            """
            if not self.target_type or not self.target_type.strip():
                msg = "target_type cannot be empty"
                raise ValueError(msg)
            return self


__all__: list[str] = ["FlextMeltanoModelsSources"]
