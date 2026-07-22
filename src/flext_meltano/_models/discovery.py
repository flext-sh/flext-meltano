"""FLEXT Meltano models - Plugin discovery models."""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated

from flext_cli import m, u
from flext_meltano import FlextMeltanoTypes as t


class FlextMeltanoModelsDiscovery:
    """Plugin discovery source, item, and catalog models."""

    class PluginDiscoverySource(m.FlexibleModel):
        """Normalized raw plugin discovery payload from external sources."""

        default_variant: Annotated[
            str, u.Field(default="", description="Plugin default variant")
        ] = ""
        variants: t.JsonMapping = u.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Available plugin variants keyed by variant name",
        )
        logo_url: Annotated[str, u.Field(default="", description="Plugin logo URL")]
        description: Annotated[
            str, u.Field(default="", description="Plugin description")
        ] = ""

        @u.field_validator("default_variant", "logo_url", "description", mode="before")
        @classmethod
        def normalize_string_fields(cls, value: t.Meltano.ValidatorInput) -> str:
            """Normalize optional string fields from external payloads."""
            return "" if value is None else str(value)

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

        plugins: t.MappingKV[str, FlextMeltanoModelsDiscovery.PluginDiscoverySource] = (
            u.Field(
                default_factory=lambda: MappingProxyType({}),
                description="Plugin discovery entries keyed by plugin name",
            )
        )
