"""FLEXT Meltano models - Plugin configuration model.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated, Self

from flext_cli import m, u

from flext_meltano import c, t


class FlextMeltanoModelsProjectsPlugin:
    """Plugin configuration model."""

    class PluginModel(m.TimestampedModel):
        """Generic plugin configuration for pipeline operations."""

        name: Annotated[t.NonEmptyStr, m.Field(description="Plugin name")]
        namespace: Annotated[str, m.Field(description="Plugin namespace")]
        pip_url: Annotated[
            str | None,
            m.Field(default=None, description="Plugin pip URL"),
        ] = None
        executable: Annotated[
            str | None,
            m.Field(default=None, description="Plugin executable"),
        ] = None
        variant: Annotated[
            str,
            m.Field(default="standard", description="Plugin variant"),
        ] = "standard"
        settings: Annotated[
            t.FlatContainerMapping,
            m.Field(description="Plugin settings"),
        ] = m.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
            description="Plugin settings",
        )
        capabilities: Annotated[
            t.StrTuple,
            m.Field(description="Plugin capabilities"),
        ] = m.Field(default_factory=tuple, description="Plugin capabilities")
        config_files: Annotated[
            t.StrTuple,
            m.Field(description="Plugin configuration files"),
        ] = m.Field(default_factory=tuple, description="Plugin configuration files")

        @m.field_validator("settings", mode="after")
        @classmethod
        def freeze_settings(
            cls,
            value: t.FlatContainerMapping,
        ) -> t.FlatContainerMapping:
            """Expose plugin settings as a read-only mapping.

            Returns:
                The resulting ``t.FlatContainerMapping``.
            """
            return MappingProxyType(dict(value))

        @m.computed_field
        def full_plugin_name(self) -> str:
            """Full plugin name with namespace.

            Returns:
                The resulting ``str``.
            """
            return f"{self.namespace}.{self.name}"

        @m.computed_field
        def has_custom_executable(self) -> bool:
            """Check if plugin has custom executable.

            Returns:
                The resulting ``bool``.
            """
            return self.executable is not None

        @m.computed_field
        def plugin_complexity(self) -> str:
            """Plugin complexity assessment.

            Returns:
                The resulting ``str``.
            """
            settings_keys = list(self.settings.keys())
            settings_count = u.count(settings_keys)
            if settings_count == 0:
                return "minimal"
            if settings_count <= c.Meltano.VALIDATION_COMPLEXITY_SIMPLE_MAX_SETTINGS:
                return "simple"
            if settings_count <= c.Meltano.VALIDATION_COMPLEXITY_MODERATE_MAX_SETTINGS:
                return "moderate"
            return "complex"

        @m.computed_field
        def settings_count(self) -> int:
            """Number of plugin settings.

            Returns:
                The resulting ``int``.
            """
            keys: t.StrSequence = list(self.settings.keys())
            return u.count(keys)

        @u.model_validator(mode="after")
        def validate_plugin_consistency(self) -> Self:
            """Validate plugin consistency.

            Returns:
                The resulting ``Self``.

            Raises:
                ValueError: If Plugin namespace cannot contain dots; or if Plugin must
                    have either pip_url or executable.
            """
            if "." in self.namespace:
                msg = "Plugin namespace cannot contain dots"
                raise ValueError(msg)
            if not self.pip_url and not self.executable:
                msg = "Plugin must have either pip_url or executable"
                raise ValueError(msg)
            return self
