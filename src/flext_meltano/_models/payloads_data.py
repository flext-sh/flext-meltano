"""FLEXT Meltano models - Data normalization payload models."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from types import MappingProxyType
from typing import Annotated

from flext_cli import m, u

from flext_meltano import t


class FlextMeltanoModelsPayloadsData:
    """Data normalization payload models with validators."""

    class JsonSchemaPayload(m.ArbitraryTypesModel):
        """Typed schema payload used by API extract flow."""

        schema_definition: Annotated[
            t.FlatContainerMapping,
            m.Field(
                alias="schema",
                serialization_alias="schema",
                validation_alias="schema",
                description="Schema-like JSON payload",
            ),
        ] = m.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Schema-like JSON payload",
        )

        @m.field_validator("schema_definition", mode="before")
        @classmethod
        def normalize_schema(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.FlatContainerMapping:
            """Normalize mapping input before JSON validation."""
            match value:
                case Mapping():
                    return t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
                case _:
                    empty_schema: t.FlatContainerMapping = {}
                    return empty_schema

        @m.field_validator("schema_definition", mode="after")
        @classmethod
        def freeze_schema(cls, value: t.FlatContainerMapping) -> t.FlatContainerMapping:
            """Expose the normalized schema as a read-only mapping."""
            return MappingProxyType(dict(value))

    class JsonRecordBatchPayload(m.ArbitraryTypesModel):
        """Typed record batch payload used by API load flow."""

        records: Annotated[
            t.VariadicTuple[t.FlatContainerMapping],
            m.Field(description="Normalized record payloads"),
        ] = m.Field(default_factory=tuple, description="Normalized record payloads")

        @m.field_validator("records", mode="before")
        @classmethod
        def normalize_records(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.VariadicTuple[t.FlatContainerMapping]:
            """Normalize mixed record input into JSON-safe record tuples."""
            if isinstance(value, (list, tuple)):
                return tuple(
                    t.Cli.JSON_MAPPING_ADAPTER.validate_python(record)
                    for record in value
                    if isinstance(record, Mapping)
                )
            return ()

    class ConfigMappingPayload(m.ArbitraryTypesModel):
        """Normalized mapping payload with string keys."""

        values: t.JsonMapping = m.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Normalized mapping values",
        )

        @m.field_validator("values", mode="before")
        @classmethod
        def normalize_values(cls, value: t.Meltano.ValidatorInput) -> t.JsonMapping:
            """Normalize mapping-like payloads to a JSON-safe mapping."""
            if isinstance(value, Mapping):
                return t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
            return {}

        @m.field_validator("values", mode="after")
        @classmethod
        def freeze_values(cls, value: t.JsonMapping) -> t.JsonMapping:
            """Expose normalized mapping values as read-only."""
            return MappingProxyType(dict(value))

    class PathPayload(m.ArbitraryTypesModel):
        """Path normalization payload for runtime path conversions."""

        value: Annotated[Path, m.Field(description="Normalized path")] = m.Field(
            default_factory=Path, description="Normalized path"
        )

        @m.field_validator("value", mode="before")
        @classmethod
        def normalize_path(cls, value: t.Meltano.ValidatorInput) -> Path:
            """Normalize mixed path input into Path objects."""
            if value is None:
                return Path()
            return Path(str(value))

    class FileContentPayload(m.ArbitraryTypesModel):
        """Normalize str|dict content to writable string for file operations."""

        content: Annotated[
            str, m.Field(default="", description="Normalized writable string content")
        ] = ""

        @m.field_validator("content", mode="before")
        @classmethod
        def normalize_content(cls, value: t.Meltano.ValidatorInput) -> str:
            """Normalize dict content via yaml_dump_str, pass str through."""
            match value:
                case Mapping():
                    return u.Cli.yaml_dump_str(dict(value))
                case None:
                    return ""
                case _:
                    return str(value)

    class VariantPayload(m.ArbitraryTypesModel):
        """Normalize plugin variant from external extraction (str|list|dict)."""

        value: t.Meltano.VariantValue = m.Field(
            default=None, description="Normalized variant value"
        )

        @m.field_validator("value", mode="before")
        @classmethod
        def normalize_variant(
            cls, value: str | t.Meltano.ValidatorInput
        ) -> str | t.StrSequence | t.ScalarMapping | None:
            """Normalize variant_raw into typed union."""
            match value:
                case None:
                    return None
                case str():
                    return value
                case list() | tuple():
                    return [str(item) for item in value]
                case Mapping():
                    result: t.MutableConfigurationMapping = {}
                    for k, v in value.items():
                        if u.primitive(v):
                            result[k] = v
                        elif v is None:
                            result[k] = ""
                        elif isinstance(v, (list, dict)):
                            result[k] = str(v)
                    return result
                case _:
                    return str(value)
