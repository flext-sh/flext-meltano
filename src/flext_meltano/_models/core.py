"""FLEXT Meltano models - Core helpers and value types."""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from typing import Annotated

from flext_cli import m, u

from flext_meltano import p, t


class FlextMeltanoModelsCore:
    """Core model helpers and value types."""

    @staticmethod
    def protect_sensitive_config(
        value: Mapping[str, t.Container],
    ) -> Mapping[str, t.Container]:
        """Protect sensitive keys in configuration dict."""
        sensitive_keys = {"password", "token", "api_key", "secret", "credentials"}

        def is_sensitive(k: str) -> bool:
            normalized = u.normalize(k, case="lower")
            sensitive_keys_list: t.StrSequence = list(sensitive_keys)
            checks_result = u.process(
                sensitive_keys_list,
                lambda s: p.Result[bool].ok(s in normalized),
            )
            checks = FlextMeltanoModelsCore.BooleanListValue.model_validate({
                "items": checks_result.unwrap_or([]),
            }).items
            if checks:
                return any(checks)
            return False

        protected: t.MutableRecursiveContainerMapping = {}
        for key, item in value.items():
            protected[key] = "[PROTECTED]" if is_sensitive(key) else item
        return protected

    @staticmethod
    def _validated_string_list(value: t.Meltano.ValidatorInput) -> t.StrSequence:
        """Normalize arbitrary values into a validated list of strings."""
        return FlextMeltanoModelsCore.StringListValue.model_validate({
            "items": value,
        }).items

    class StringListValue(m.ArbitraryTypesModel):
        """Validated string list wrapper for result normalization."""

        items: Annotated[
            t.StrSequence,
            u.Field(description="Normalized list of string values"),
        ] = u.Field(default_factory=tuple)

        @u.field_validator("items", mode="before")
        @classmethod
        def normalize_items(cls, value: t.Meltano.ValidatorInput) -> t.StrSequence:
            """Convert sequence-like values into string lists."""
            if isinstance(value, (list, tuple, set)):
                return [str(item) for item in value if item is not None]
            return []

    class BooleanListValue(m.ArbitraryTypesModel):
        """Validated boolean list wrapper for process output."""

        items: Annotated[
            Sequence[bool],
            u.Field(description="Normalized list of boolean values"),
        ] = u.Field(
            default_factory=lambda: list[bool](),
            description="Normalized boolean values",
        )

        @u.field_validator("items", mode="before")
        @classmethod
        def normalize_items(cls, value: t.Meltano.ValidatorInput) -> Sequence[bool]:
            """Convert sequence-like values into booleans."""
            if isinstance(value, (list, tuple, set)):
                return [bool(item) for item in value]
            return []
