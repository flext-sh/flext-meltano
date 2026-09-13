"""FLEXT Meltano models - Pipeline context and configuration models."""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import Annotated

from flext_cli import m

from flext_meltano import c, t


class FlextMeltanoModelsContext:
    """Pipeline context and configuration models."""

    class PipelineExecutionContext(m.FlexibleModel):
        """Typed context envelope for ELT pipeline execution."""

        project_root: Annotated[str, m.Field(description="Project root path")]
        elt_context: t.FlatContainerMapping = m.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
            description="ELT execution context",
        )
        extractor_name: Annotated[str, m.Field(description="Extractor name")]
        loader_name: Annotated[t.NonEmptyStr, m.Field(description="Loader name")]
        execution_completed: Annotated[
            bool, m.Field(default=False, description="Execution completion flag")
        ] = False
        execution_result: t.FlatContainerMapping = m.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
            description="Execution result payload",
        )

        @m.field_validator("elt_context", "execution_result", mode="before")
        @classmethod
        def normalize_mapping_payloads(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.FlatContainerMapping:
            """Normalize mapping-like payloads into JSON-safe dictionaries."""
            match value:
                case Mapping():
                    return t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
                case _:
                    empty: t.FlatContainerMapping = {}
                    return empty

        @m.field_validator("elt_context", "execution_result", mode="after")
        @classmethod
        def freeze_mapping_payloads(
            cls, value: t.FlatContainerMapping
        ) -> t.FlatContainerMapping:
            """Expose normalized pipeline mappings as read-only values."""
            return MappingProxyType(dict(value))

        @m.field_validator(
            "project_root", "extractor_name", "loader_name", mode="before"
        )
        @classmethod
        def normalize_required_strings(cls, value: t.Meltano.ValidatorInput) -> str:
            """Normalize required string fields from context payloads."""
            normalized = "" if value is None else str(value)
            return normalized.strip()

    class PipelineResultContext(m.FlexibleModel):
        """Typed subset for extracting final pipeline result fields."""

        project_root: Annotated[
            str, m.Field(default="unknown", description="Project root path")
        ] = "unknown"
        execution_result: t.FlatContainerMapping = m.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
            description="Execution result payload",
        )

        @m.field_validator("execution_result", mode="before")
        @classmethod
        def normalize_execution_result(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.FlatContainerMapping:
            """Normalize execution result map payload."""
            match value:
                case Mapping():
                    return t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
                case _:
                    empty: t.FlatContainerMapping = {}
                    return empty

        @m.field_validator("execution_result", mode="after")
        @classmethod
        def freeze_execution_result(
            cls, value: t.FlatContainerMapping
        ) -> t.FlatContainerMapping:
            """Expose the normalized result payload as a read-only mapping."""
            return MappingProxyType(dict(value))

        @m.field_validator("project_root", mode="before")
        @classmethod
        def normalize_project_root(cls, value: t.Meltano.ValidatorInput) -> str:
            """Normalize project root from mixed payload values."""
            normalized = "unknown" if value is None else str(value)
            return normalized.strip() or "unknown"

    class PipelineExecutionScalarMap(m.FlexibleModel):
        """Scalar-only pipeline execution values normalized to strings."""

        values: t.StrMapping = m.Field(
            default_factory=lambda: MappingProxyType[str, str]({}),
            description="Execution values filtered to scalar strings",
        )

        @m.field_validator("values", mode="before")
        @classmethod
        def normalize_values(cls, value: t.Meltano.ValidatorInput) -> t.StrMapping:
            """Keep scalar execution values and stringify them."""
            match value:
                case Mapping():
                    return {
                        key: str(item)
                        for key, item in value.items()
                        if isinstance(item, (str, int, bool, float))
                    }
                case _:
                    return {}

        @m.field_validator("values", mode="after")
        @classmethod
        def freeze_values(cls, value: t.StrMapping) -> t.StrMapping:
            """Expose normalized scalar values as a read-only mapping."""
            return MappingProxyType(dict(value))

    class PluginComponentConfig(m.Entity):
        """Validated plugin component configuration for pipeline validators."""

        name: Annotated[t.NonEmptyStr, m.Field(description="Plugin name")]
        namespace: Annotated[str, m.Field(description="Plugin namespace")]
        pip_url: Annotated[t.NonEmptyStr, m.Field(description="Plugin pip URL")]
        executable: Annotated[str, m.Field(description="Plugin executable")]
        type: Annotated[str, m.Field(default="extractor", description="Plugin type")]

        @m.field_validator("name")
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
