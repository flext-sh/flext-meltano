"""FLEXT Meltano models - Pipeline context and configuration models."""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from types import MappingProxyType
from typing import Annotated

from flext_cli import m, u

from flext_meltano import c, t


class FlextMeltanoModelsContext:
    """Pipeline context and configuration models."""

    class PipelineExecutionContext(m.FlexibleModel):
        """Typed context envelope for ELT pipeline execution."""

        project_root: Annotated[str, u.Field(description="Project root path")]
        elt_context: t.JsonMapping = u.Field(
            default_factory=lambda: MappingProxyType({}),
            description="ELT execution context",
        )
        extractor_name: Annotated[str, u.Field(description="Extractor name")]
        loader_name: Annotated[t.NonEmptyStr, u.Field(description="Loader name")]
        execution_completed: Annotated[
            bool, u.Field(default=False, description="Execution completion flag")
        ] = False
        execution_result: t.JsonMapping = u.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Execution result payload",
        )

        @u.field_validator("elt_context", "execution_result", mode="before")
        @classmethod
        def normalize_mapping_payloads(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.JsonMapping:
            """Normalize mapping-like payloads into dictionaries."""
            match value:
                case Mapping():
                    normalized = t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
                    return MappingProxyType({
                        str(key): item for key, item in normalized.items()
                    })
                case _:
                    return MappingProxyType({})

        @u.field_validator(
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
            str, u.Field(default=c.IDENTIFIER_UNKNOWN, description="Project root path")
        ] = c.IDENTIFIER_UNKNOWN
        execution_result: t.JsonMapping = u.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Execution result payload",
        )

        @u.field_validator("execution_result", mode="before")
        @classmethod
        def normalize_execution_result(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.JsonMapping:
            """Normalize execution result map payload."""
            match value:
                case Mapping():
                    normalized = t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
                    return MappingProxyType({
                        str(key): item for key, item in normalized.items()
                    })
                case _:
                    return MappingProxyType({})

        @u.field_validator("project_root", mode="before")
        @classmethod
        def normalize_project_root(cls, value: t.Meltano.ValidatorInput) -> str:
            """Normalize project root from mixed payload values."""
            normalized = c.IDENTIFIER_UNKNOWN if value is None else str(value)
            return normalized.strip() or c.IDENTIFIER_UNKNOWN

    class PipelineExecutionScalarMap(m.FlexibleModel):
        """Scalar-only pipeline execution values normalized to strings."""

        values: t.StrMapping = u.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Execution values filtered to scalar strings",
        )

        @u.field_validator("values", mode="before")
        @classmethod
        def normalize_values(cls, value: t.Meltano.ValidatorInput) -> t.StrMapping:
            """Keep scalar execution values and stringify them."""
            match value:
                case Mapping():
                    return MappingProxyType({
                        str(key): str(item)
                        for key, item in value.items()
                        if u.matches_type(item, (str, int, bool, float))
                    })
                case _:
                    return MappingProxyType({})

    class PluginComponentConfig(m.Entity):
        """Validated plugin component configuration for pipeline validators."""

        name: Annotated[t.NonEmptyStr, u.Field(description="Plugin name")]
        namespace: Annotated[str, u.Field(description="Plugin namespace")]
        pip_url: Annotated[t.NonEmptyStr, u.Field(description="Plugin pip URL")]
        executable: Annotated[str, u.Field(description="Plugin executable")]
        type: Annotated[str, u.Field(default="extractor", description="Plugin type")]

        @u.field_validator("name")
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
