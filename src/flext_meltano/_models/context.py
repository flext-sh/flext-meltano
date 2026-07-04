"""FLEXT Meltano models - Pipeline context and configuration models."""

from __future__ import annotations

from typing import Annotated

from flext_cli import m, u
from flext_meltano.constants import FlextMeltanoConstants as c
from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoModelsContext:
    """Pipeline context and configuration models."""

    class PluginComponentConfig(m.Entity):
        """Validated plugin component configuration for pipeline validators."""

        name: Annotated[t.NonEmptyStr, u.Field(description="Plugin name")]
        namespace: Annotated[str, u.Field(description="Plugin namespace")]
        pip_url: Annotated[t.NonEmptyStr, u.Field(description="Plugin pip URL")]
        executable: Annotated[str, u.Field(description="Plugin executable")]
        type: Annotated[str, u.Field(default="extractor", description="Plugin type")]

        @u.field_validator("name")
        @classmethod
        def validate_name_business_rules(cls, v: str) -> str:
            """Validate plugin name business rules."""
            v = v.strip()
            if not v:
                msg = "Plugin name cannot be empty"
                raise ValueError(msg)
            if (
                v.startswith("target-")
                and len(v) < c.Meltano.PLUGIN_MIN_TARGET_PLUGIN_NAME_LENGTH
            ):
                msg = "Target plugin names must be at least 8 characters"
                raise ValueError(msg)
            if (
                v.startswith("tap-")
                and len(v) < c.Meltano.PLUGIN_MIN_TAP_PLUGIN_NAME_LENGTH
            ):
                msg = "Source component names must be at least 5 characters"
                raise ValueError(msg)
            return v
