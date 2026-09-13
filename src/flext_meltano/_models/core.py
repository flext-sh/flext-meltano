"""FLEXT Meltano models - Core helpers and value types."""

from __future__ import annotations

from typing import Annotated

from flext_cli import m, u

from flext_meltano import t


class FlextMeltanoModelsCore:
    """Core model helpers and value types."""

    @staticmethod
    def protect_sensitive_config(
        value: t.FlatContainerMapping,
    ) -> t.FlatContainerMapping:
        """Protect sensitive keys in configuration dict."""
        sensitive_keys = {"password", "token", "api_key", "secret", "credentials"}

        def is_sensitive(k: str) -> bool:
            normalized = u.normalize(k, case="lower")
            return any(sensitive_key in normalized for sensitive_key in sensitive_keys)

        protected: t.MutableFlatContainerMapping = {}
        for key, item in value.items():
            protected[key] = "[PROTECTED]" if is_sensitive(key) else item
        return protected

    @staticmethod
    def _validated_string_list(value: t.Meltano.ValidatorInput) -> t.StrSequence:
        """Normalize arbitrary values into a validated list of strings."""
        validated: FlextMeltanoModelsCore.StringListValue = (
            FlextMeltanoModelsCore.StringListValue.model_validate({"items": value})
        )
        items: t.StrTuple = validated.items
        return items

    class StringListValue(m.ArbitraryTypesModel):
        """Validated string list wrapper for result normalization."""

        items: Annotated[
            t.StrTuple, m.Field(description="Normalized tuple of string values")
        ] = m.Field(default_factory=tuple, description="Normalized string values")

        @m.field_validator("items", mode="before")
        @classmethod
        def normalize_items(cls, value: t.Meltano.ValidatorInput) -> t.StrTuple:
            """Convert sequence-like values into string tuples."""
            if isinstance(value, (list, tuple, set)):
                return tuple(str(item) for item in value if item is not None)
            return ()
