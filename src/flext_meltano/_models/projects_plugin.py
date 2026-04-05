"""FLEXT Meltano models - Plugin configuration model."""

from __future__ import annotations

from typing import Annotated, Self

from flext_cli import FlextCliModels, u
from pydantic import Field, computed_field, model_validator

from flext_meltano import c, t


class FlextMeltanoModelsProjectsPlugin:
    """Plugin configuration model."""

    class PluginModel(FlextCliModels.TimestampedModel):
        """Generic plugin configuration for pipeline operations."""

        name: Annotated[t.NonEmptyStr, Field(description="Plugin name")]
        namespace: Annotated[str, Field(description="Plugin namespace")]
        pip_url: Annotated[
            str | None, Field(default=None, description="Plugin pip URL")
        ] = None
        executable: Annotated[
            str | None, Field(default=None, description="Plugin executable")
        ] = None
        variant: Annotated[
            str, Field(default="standard", description="Plugin variant")
        ] = "standard"
        settings: Annotated[
            t.ContainerMapping, Field(description="Plugin settings")
        ] = Field(default_factory=dict, description="Plugin settings")
        capabilities: Annotated[
            t.StrSequence, Field(description="Plugin capabilities")
        ] = Field(default_factory=list, description="Plugin capabilities")
        config_files: Annotated[
            t.StrSequence, Field(description="Plugin configuration files")
        ] = Field(default_factory=list, description="Plugin configuration files")

        @computed_field
        def full_plugin_name(self) -> str:
            """Full plugin name with namespace."""
            return f"{self.namespace}.{self.name}"

        @computed_field
        def has_custom_executable(self) -> bool:
            """Check if plugin has custom executable."""
            return self.executable is not None

        @computed_field
        def plugin_complexity(self) -> str:
            """Plugin complexity assessment."""
            settings_keys = list(self.settings.keys())
            settings_count = u.count(settings_keys)
            if settings_count == 0:
                return "minimal"
            if (
                settings_count
                <= c.Meltano.ModelValidation.COMPLEXITY_SIMPLE_MAX_SETTINGS
            ):
                return "simple"
            if (
                settings_count
                <= c.Meltano.ModelValidation.COMPLEXITY_MODERATE_MAX_SETTINGS
            ):
                return "moderate"
            return "complex"

        @computed_field
        def settings_count(self) -> int:
            """Number of plugin settings."""
            keys: t.StrSequence = list(self.settings.keys())
            return u.count(keys)

        @model_validator(mode="after")
        def validate_plugin_consistency(self) -> Self:
            """Validate plugin consistency."""
            if "." in self.namespace:
                msg = "Plugin namespace cannot contain dots"
                raise ValueError(msg)
            if not self.pip_url and not self.executable:
                msg = "Plugin must have either pip_url or executable"
                raise ValueError(msg)
            return self
