"""FLEXT Meltano models - Core helpers and value types.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from flext_cli import m, u

from flext_meltano import t


class FlextMeltanoModelsCore:
    """Core model helpers and value types."""

    @staticmethod
    def normalize_json_mapping(
        value: t.Meltano.ValidatorInput,
    ) -> t.FlatContainerMapping:
        """Normalize mapping-like payloads into JSON-safe dictionaries.

        Returns:
            The resulting ``t.FlatContainerMapping``.
        """
        match value:
            case Mapping():
                return t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
            case _:
                empty: t.FlatContainerMapping = {}
                return empty

    @staticmethod
    def protect_sensitive_config(
        value: t.FlatContainerMapping,
    ) -> t.FlatContainerMapping:
        """Protect sensitive keys in configuration dict.

        Returns:
            The resulting ``t.FlatContainerMapping``.
        """
        sensitive_keys = {"password", "token", "api_key", "secret", "credentials"}

        def is_sensitive(k: str) -> bool:
            normalized = u.normalize(k, case="lower")
            return any(sensitive_key in normalized for sensitive_key in sensitive_keys)

        def redact(item: t.JsonValue) -> t.JsonValue:
            match item:
                case dict():
                    return {
                        key: "[PROTECTED]" if is_sensitive(key) else redact(nested)
                        for key, nested in item.items()
                    }
                case list():
                    return [redact(nested) for nested in item]
                case _:
                    return item

        return {
            key: "[PROTECTED]" if is_sensitive(key) else redact(item)
            for key, item in value.items()
        }

    @staticmethod
    def _validated_string_list(value: t.Meltano.ValidatorInput) -> t.StrSequence:
        """Normalize arbitrary values into a validated list of strings.

        Returns:
            The resulting ``t.StrSequence``.
        """
        validated: FlextMeltanoModelsCore.StringListValue = (
            FlextMeltanoModelsCore.StringListValue.model_validate({"items": value})
        )
        items: t.StrTuple = validated.items
        return items

    class SensitiveConfigSerializer:
        """Mixin serializing ``connection_config`` with sensitive data protection.

        One owner for the ``connection_config`` field serializer shared by every
        model carrying that field; consumers list this class first in their
        bases so the pydantic decorator machinery collects it through the MRO.
        """

        @u.field_serializer("connection_config")
        @staticmethod
        def serialize_connection_config(
            value: t.FlatContainerMapping,
        ) -> t.FlatContainerMapping:
            """Serialize connection config with sensitive data protection.

            Returns:
                The resulting ``t.FlatContainerMapping``.
            """
            return FlextMeltanoModelsCore.protect_sensitive_config(value)

        @u.field_serializer("stream_config", check_fields=False)
        @staticmethod
        def serialize_stream_config(value: t.FlatContainerMapping) -> t.JsonDict:
            """Export readonly stream mappings without changing their stored values.

            Returns:
                The resulting ``t.JsonDict``.
            """
            return dict(value)

    class StringListValue(m.ArbitraryTypesModel):
        """Validated string list wrapper for result normalization."""

        items: Annotated[
            t.StrTuple,
            m.Field(description="Normalized tuple of string values"),
        ] = m.Field(
            default_factory=tuple[str, ...],
            description="Normalized string values",
        )

        @m.field_validator("items", mode="before")
        @classmethod
        def normalize_items(cls, value: t.Meltano.ValidatorInput) -> t.StrTuple:
            """Convert sequence-like values into string tuples.

            Returns:
                The resulting ``t.StrTuple``.
            """
            if isinstance(value, (list, tuple, set)):
                return tuple(str(item) for item in value if item is not None)
            return ()
