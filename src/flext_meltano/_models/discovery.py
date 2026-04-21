"""FLEXT Meltano models - Plugin discovery models."""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from typing import Annotated, ClassVar

from flext_cli import m, u

from flext_meltano import t


class FlextMeltanoModelsDiscovery:
    """Plugin discovery source, item, and catalog models."""

    class PluginDiscoverySource(m.FlexibleModel):
        """Normalized raw plugin discovery payload from external sources."""

        _flext_enforcement_exempt: ClassVar[bool] = True

        default_variant: Annotated[
            str, u.Field(default="", description="Plugin default variant")
        ] = ""
        variants: t.Cli.JsonMapping = u.Field(default_factory=dict)
        logo_url: Annotated[str, u.Field(default="", description="Plugin logo URL")]
        description: Annotated[
            str, u.Field(default="", description="Plugin description")
        ] = ""

        @u.field_validator("default_variant", "logo_url", "description", mode="before")
        @classmethod
        def normalize_string_fields(cls, value: t.Meltano.ValidatorInput) -> str:
            """Normalize optional string fields from external payloads."""
            return "" if value is None else str(value)

        @u.field_validator("variants", mode="before")
        @classmethod
        def normalize_variants(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.Cli.JsonMapping:
            """Normalize variant maps from external payloads."""
            match value:
                case Mapping():
                    return t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
                case _:
                    return {}

    class PluginDiscoveryItem(m.ArbitraryTypesModel):
        """Typed plugin discovery response item."""

        name: Annotated[t.NonEmptyStr, u.Field(description="Plugin name")]
        type: Annotated[t.NonEmptyStr, u.Field(description="Plugin type")]
        default_variant: Annotated[
            str, u.Field(default="", description="Default plugin variant")
        ] = ""
        variants: Annotated[
            str, u.Field(default="", description="Comma-separated variants")
        ] = ""
        logo_url: Annotated[str, u.Field(default="", description="Plugin logo URL")]
        description: Annotated[
            str, u.Field(default="", description="Plugin description")
        ] = ""

    class PluginDiscoveryCatalog(m.FlexibleModel):
        """Typed plugin discovery catalog keyed by plugin name."""

        _flext_enforcement_exempt: ClassVar[bool] = True

        plugins: Mapping[str, FlextMeltanoModelsDiscovery.PluginDiscoverySource] = (
            u.Field(default_factory=dict)
        )

        @u.field_validator("plugins", mode="before")
        @classmethod
        def normalize_plugins(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.Cli.JsonMapping:
            """Normalize plugin catalog mapping."""
            match value:
                case Mapping():
                    return t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
                case _:
                    return {}
