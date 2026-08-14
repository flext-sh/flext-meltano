"""FLEXT Meltano models - Core helpers and value types."""

from __future__ import annotations

from typing import Annotated

from flext_cli import m, u

from flext_core import r
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
            sensitive_keys_list: t.StrSequence = list(sensitive_keys)
            checks_result = u.process(
                sensitive_keys_list, lambda s: r[bool].ok(s in normalized)
            )
            checks = FlextMeltanoModelsCore.BooleanListValue.model_validate({
                "items": checks_result.unwrap_or([])
            }).items
            if checks:
                return any(checks)
            return False

        protected: t.MutableFlatContainerMapping = {}
        for key, item in value.items():
            protected[key] = "[PROTECTED]" if is_sensitive(key) else item
        return protected

    @staticmethod
    def _validated_string_list(value: t.Meltano.ValidatorInput) -> t.StrSequence:
        """Normalize arbitrary values into a validated list of strings."""
        return FlextMeltanoModelsCore.StringListValue.model_validate({
            "items": value
        }).items

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

    class BooleanListValue(m.ArbitraryTypesModel):
        """Validated boolean list wrapper for process output."""

        items: Annotated[
            t.VariadicTuple[bool],
            m.Field(description="Normalized tuple of boolean values"),
        ] = m.Field(default_factory=tuple, description="Normalized boolean values")

        @m.field_validator("items", mode="before")
        @classmethod
        def normalize_items(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.VariadicTuple[bool]:
            """Convert sequence-like values into a boolean tuple."""
            if isinstance(value, (list, tuple, set)):
                return tuple(bool(item) for item in value)
            return ()
