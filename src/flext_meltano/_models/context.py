"""FLEXT Meltano models - Pipeline context and configuration models."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from flext_cli import m
from pydantic import Field, field_validator

from flext_meltano import c, t


class FlextMeltanoModelsContext:
    """Pipeline context and configuration models."""

    class PipelineExecutionContext(m.FlexibleModel):
        """Typed context envelope for ELT pipeline execution."""

        project_root: Annotated[str, Field(description="Project root path")]
        elt_context: t.FlatContainerMapping = Field(
            default_factory=dict, description="ELT execution context"
        )
        extractor_name: Annotated[str, Field(description="Extractor name")]
        loader_name: Annotated[t.NonEmptyStr, Field(description="Loader name")]
        execution_completed: Annotated[
            bool, Field(default=False, description="Execution completion flag")
        ] = False
        execution_result: t.FlatContainerMapping = Field(
            default_factory=dict, description="Execution result payload"
        )

        @field_validator("elt_context", "execution_result", mode="before")
        @classmethod
        def normalize_mapping_payloads(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.FlatContainerMapping:
            """Normalize mapping-like payloads into dictionaries."""
            match value:
                case Mapping():
                    return {str(key): item for key, item in value.items()}
                case _:
                    empty: t.FlatContainerMapping = {}
                    return empty

        @field_validator("project_root", "extractor_name", "loader_name", mode="before")
        @classmethod
        def normalize_required_strings(cls, value: t.Meltano.ValidatorInput) -> str:
            """Normalize required string fields from context payloads."""
            normalized = "" if value is None else str(value)
            return normalized.strip()

    class PipelineResultContext(m.FlexibleModel):
        """Typed subset for extracting final pipeline result fields."""

        project_root: Annotated[
            str, Field(default="unknown", description="Project root path")
        ] = "unknown"
        execution_result: t.FlatContainerMapping = Field(
            default_factory=dict, description="Execution result payload"
        )

        @field_validator("execution_result", mode="before")
        @classmethod
        def normalize_execution_result(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.FlatContainerMapping:
            """Normalize execution result map payload."""
            match value:
                case Mapping():
                    return {str(key): item for key, item in value.items()}
                case _:
                    empty: t.FlatContainerMapping = {}
                    return empty

        @field_validator("project_root", mode="before")
        @classmethod
        def normalize_project_root(cls, value: t.Meltano.ValidatorInput) -> str:
            """Normalize project root from mixed payload values."""
            normalized = "unknown" if value is None else str(value)
            return normalized.strip() or "unknown"

    class PipelineExecutionScalarMap(m.FlexibleModel):
        """Scalar-only pipeline execution values normalized to strings."""

        values: t.StrMapping = Field(
            default_factory=dict,
            description="Execution values filtered to scalar strings",
        )

        @field_validator("values", mode="before")
        @classmethod
        def normalize_values(cls, value: t.Meltano.ValidatorInput) -> t.StrMapping:
            """Keep scalar execution values and stringify them."""
            match value:
                case Mapping():
                    return {
                        str(key): str(item)
                        for key, item in value.items()
                        if isinstance(item, (str, int, bool, float))
                    }
                case _:
                    return {}

    class PluginComponentConfig(m.Entity):
        """Validated plugin component configuration for pipeline validators."""

        name: Annotated[t.NonEmptyStr, Field(description="Plugin name")]
        namespace: Annotated[str, Field(description="Plugin namespace")]
        pip_url: Annotated[t.NonEmptyStr, Field(description="Plugin pip URL")]
        executable: Annotated[str, Field(description="Plugin executable")]
        type: Annotated[str, Field(default="extractor", description="Plugin type")]

        @field_validator("name")
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
