"""FLEXT Meltano models - Plugin discovery models."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from flext_cli import FlextCliModels
from pydantic import Field, field_validator

from flext_meltano import t


class FlextMeltanoModelsDiscovery:
    """Plugin discovery source, item, and catalog models."""

    class PluginDiscoverySource(FlextCliModels.FlexibleModel):
        """Normalized raw plugin discovery payload from external sources."""

        default_variant: Annotated[
            str, Field(default="", description="Plugin default variant")
        ] = ""
        variants: t.ContainerMapping = Field(
            default_factory=dict, description="Available plugin variants"
        )
        logo_url: Annotated[str, Field(default="", description="Plugin logo URL")]
        description: Annotated[
            str, Field(default="", description="Plugin description")
        ] = ""

        @field_validator("default_variant", "logo_url", "description", mode="before")
        @classmethod
        def normalize_string_fields(cls, value: t.Meltano.ValidatorInput) -> str:
            """Normalize optional string fields from external payloads."""
            return "" if value is None else str(value)

        @field_validator("variants", mode="before")
        @classmethod
        def normalize_variants(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.ContainerMapping:
            """Normalize variant maps from external payloads."""
            match value:
                case Mapping():
                    return {str(key): item for key, item in value.items()}
                case _:
                    empty: t.ContainerMapping = {}
                    return empty

    class PluginDiscoveryItem(FlextCliModels.ArbitraryTypesModel):
        """Typed plugin discovery response item."""

        name: Annotated[t.NonEmptyStr, Field(description="Plugin name")]
        type: Annotated[t.NonEmptyStr, Field(description="Plugin type")]
        default_variant: Annotated[
            str, Field(default="", description="Default plugin variant")
        ] = ""
        variants: Annotated[
            str, Field(default="", description="Comma-separated variants")
        ] = ""
        logo_url: Annotated[str, Field(default="", description="Plugin logo URL")]
        description: Annotated[
            str, Field(default="", description="Plugin description")
        ] = ""

    class PluginDiscoveryCatalog(FlextCliModels.FlexibleModel):
        """Typed plugin discovery catalog keyed by plugin name."""

        plugins: Mapping[str, FlextMeltanoModelsDiscovery.PluginDiscoverySource] = (
            Field(default_factory=dict, description="Discovered plugins catalog")
        )

        @field_validator("plugins", mode="before")
        @classmethod
        def normalize_plugins(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.ContainerMapping:
            """Normalize plugin catalog mapping."""
            match value:
                case Mapping():
                    return {str(key): item for key, item in value.items()}
                case _:
                    empty: t.ContainerMapping = {}
                    return empty
