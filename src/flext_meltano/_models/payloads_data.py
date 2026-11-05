"""FLEXT Meltano models - Data normalization payload models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from types import MappingProxyType
from typing import Annotated

from flext_cli import m, u

from flext_meltano import t


class FlextMeltanoModelsPayloadsData:
    """Data normalization payload models with validators."""

    class ConfigMappingPayload(m.ArbitraryTypesModel):
        """Normalized mapping payload with string keys."""

        values: t.JsonMapping = m.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
            description="Normalized mapping values",
        )

        @m.field_validator("values", mode="before")
        @classmethod
        def normalize_values(cls, value: t.Meltano.ValidatorInput) -> t.JsonMapping:
            """Normalize mapping-like payloads to a JSON-safe mapping.

            Returns:
                The resulting ``t.JsonMapping``.

            """
            if isinstance(value, Mapping):
                return u.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
            return {}

        @m.field_validator("values", mode="after")
        @classmethod
        def freeze_values(cls, value: t.JsonMapping) -> t.JsonMapping:
            """Expose normalized mapping values as read-only.

            Returns:
                The resulting ``t.JsonMapping``.

            """
            return MappingProxyType(dict(value))

    class PathPayload(m.ArbitraryTypesModel):
        """Path normalization payload for runtime path conversions."""

        value: Annotated[Path, m.Field(description="Normalized path")] = m.Field(
            default_factory=Path,
            description="Normalized path",
        )

        @m.field_validator("value", mode="before")
        @classmethod
        def normalize_path(cls, value: t.Meltano.ValidatorInput) -> Path:
            """Normalize mixed path input into Path objects.

            Returns:
                The resulting ``Path``.

            """
            if value is None:
                return Path()
            return Path(str(value))


__all__: list[str] = ["FlextMeltanoModelsPayloadsData"]
