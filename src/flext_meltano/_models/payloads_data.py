"""FLEXT Meltano models - Data normalization payload models."""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from pathlib import Path
from types import MappingProxyType
from typing import Annotated

from flext_cli import m, u
from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoModelsPayloadsData:
    """Data normalization payload models with validators."""

    class ConfigMappingPayload(m.ArbitraryTypesModel):
        """Normalized mapping payload with string keys."""

        values: Annotated[
            t.JsonMapping,
            u.Field(description="Normalized mapping values"),
        ] = u.Field(default_factory=lambda: MappingProxyType({}))

    class PathPayload(m.ArbitraryTypesModel):
        """Path normalization payload for runtime path conversions."""

        value: Annotated[Path, u.Field(description="Normalized path")] = u.Field(
            default_factory=Path, description="Normalized path"
        )

        @u.field_validator("value", mode="before")
        @classmethod
        def normalize_path(cls, value: t.Meltano.ValidatorInput) -> Path:
            """Normalize mixed path input into Path objects."""
            if value is None:
                return Path()
            return Path(str(value))

    class VariantPayload(m.ArbitraryTypesModel):
        """Normalize plugin variant from external extraction (str|list|dict)."""

        value: Annotated[
            t.JsonValue | None,
            u.Field(description="Normalized variant value"),
        ] = None

        @u.field_validator("value", mode="before")
        @classmethod
        def normalize_variant(
            cls,
            value: str | t.Meltano.ValidatorInput,
        ) -> t.JsonValue | None:
            """Normalize variant payload through canonical Pydantic models."""
            match value:
                case None:
                    return None
                case str():
                    return value
                case list() | tuple():
                    return [str(item) for item in value]
                case Mapping():
                    return t.json_value_adapter().validate_python(value)
                case _:
                    return str(value)

        @u.computed_field(return_type=t.JsonValue | None)
        def json_value(self) -> t.JsonValue | None:
            """Expose the normalized variant as a canonical JSON-compatible value."""
            return self.value
