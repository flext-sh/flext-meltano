"""FLEXT Meltano models - Data normalization payload models."""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from pathlib import Path
from types import MappingProxyType
from typing import Annotated

from flext_cli import m, u

from flext_meltano import c, t


class FlextMeltanoModelsPayloadsData:
    """Data normalization payload models with validators."""

    class JsonSchemaPayload(m.ArbitraryTypesModel):
        """Typed schema payload used by API extract flow."""

        schema_definition: Annotated[
            t.JsonMapping,
            u.Field(
                alias=c.Meltano.SchemaKey.SCHEMA,
                serialization_alias=c.Meltano.SchemaKey.SCHEMA,
                validation_alias=c.Meltano.SchemaKey.SCHEMA,
                description="Schema-like JSON payload",
            ),
        ] = u.Field(default_factory=lambda: MappingProxyType({}))

        @u.field_validator("schema_definition", mode="before")
        @classmethod
        def normalize_schema(cls, value: t.Meltano.ValidatorInput) -> t.JsonMapping:
            """Normalize mapping input before JSON validation."""
            match value:
                case Mapping():
                    normalized = t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
                    return MappingProxyType(dict(normalized.items()))
                case _:
                    return MappingProxyType({})

    class JsonRecordBatchPayload(m.ArbitraryTypesModel):
        """Typed record batch payload used by API load flow."""

        records: Annotated[
            t.SequenceOf[t.JsonMapping],
            u.Field(description="Normalized record payloads"),
        ] = u.Field(
            default_factory=lambda: list[t.JsonMapping](),
            description="Normalized record payloads",
        )

        @u.field_validator("records", mode="before")
        @classmethod
        def normalize_records(
            cls,
            value: t.Meltano.ValidatorInput,
        ) -> t.SequenceOf[t.JsonMapping] | t.StrSequence:
            """Normalize mixed record input into dict records."""
            match value:
                case list() | tuple():
                    records: t.MutableSequenceOf[t.JsonMapping] = []
                    for record in value:
                        match record:
                            case Mapping():
                                record_dict: t.MutableJsonMapping = {}
                                for key, item in record.items():
                                    if u.primitive(item):
                                        record_dict[key] = item
                                records.append(record_dict)
                            case _:
                                continue
                    return records
                case _:
                    return []

    class ConfigMappingPayload(m.ArbitraryTypesModel):
        """Normalized mapping payload with string keys."""

        values: Annotated[
            t.JsonMapping,
            u.Field(description="Normalized mapping values"),
        ] = u.Field(default_factory=lambda: MappingProxyType({}))

        @u.field_validator("values", mode="before")
        @classmethod
        def normalize_values(
            cls,
            value: t.Meltano.ValidatorInput,
        ) -> t.JsonMapping:
            """Normalize mapping-like payloads through the canonical CLI JSON adapter."""
            if not isinstance(value, Mapping):
                return MappingProxyType({})
            normalized = t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
            return MappingProxyType(dict(normalized.items()))

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

    class FileContentPayload(m.ArbitraryTypesModel):
        """Normalize str|dict content to writable string for file operations."""

        content: Annotated[
            str, u.Field(default="", description="Normalized writable string content")
        ] = ""

        @u.field_validator("content", mode="before")
        @classmethod
        def normalize_content(cls, value: t.Meltano.ValidatorInput) -> str:
            """Normalize dict content via yaml_dump_str, pass str through."""
            match value:
                case Mapping():
                    normalized = t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
                    return u.Cli.yaml_dump_str(normalized)
                case None:
                    return ""
                case _:
                    return str(value)

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
            """Normalize variant payload through the canonical CLI JSON adapter."""
            match value:
                case None:
                    return None
                case str():
                    return value
                case list() | tuple():
                    return [str(item) for item in value]
                case Mapping():
                    return dict(t.Cli.JSON_MAPPING_ADAPTER.validate_python(value))
                case _:
                    return str(value)

        @u.computed_field(return_type=t.JsonValue | None)
        def json_value(self) -> t.JsonValue | None:
            """Expose the normalized variant as a canonical JSON-compatible value."""
            return self.value
