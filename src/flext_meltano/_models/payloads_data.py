"""FLEXT Meltano models - Data normalization payload models."""

from __future__ import annotations

from collections.abc import (
    Mapping,
    MutableSequence,
    Sequence,
)
from pathlib import Path
from typing import Annotated, ClassVar

from flext_cli import m, u

from flext_meltano import c, t


class FlextMeltanoModelsPayloadsData:
    """Data normalization payload models with validators."""

    class JsonSchemaPayload(m.ArbitraryTypesModel):
        """Typed schema payload used by API extract flow."""

        _flext_enforcement_exempt: ClassVar[bool] = True

        schema_definition: Annotated[
            t.FlatContainerMapping,
            u.Field(
                alias=c.Meltano.SchemaKey.SCHEMA,
                serialization_alias=c.Meltano.SchemaKey.SCHEMA,
                validation_alias=c.Meltano.SchemaKey.SCHEMA,
                description="Schema-like JSON payload",
            ),
        ] = u.Field(default_factory=dict)

        @u.field_validator("schema_definition", mode="before")
        @classmethod
        def normalize_schema(cls, value: t.Meltano.ValidatorInput) -> t.Cli.JsonMapping:
            """Normalize mapping input before JSON validation."""
            match value:
                case Mapping():
                    return t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
                case _:
                    return {}

    class JsonRecordBatchPayload(m.ArbitraryTypesModel):
        """Typed record batch payload used by API load flow."""

        records: Annotated[
            Sequence[t.FlatContainerMapping],
            u.Field(description="Normalized record payloads"),
        ] = u.Field(
            default_factory=lambda: list[t.FlatContainerMapping](),
            description="Normalized record payloads",
        )

        @u.field_validator("records", mode="before")
        @classmethod
        def normalize_records(
            cls,
            value: t.Meltano.ValidatorInput,
        ) -> Sequence[t.FlatContainerMapping] | t.StrSequence:
            """Normalize mixed record input into dict records."""
            match value:
                case list() | tuple():
                    records: MutableSequence[t.FlatContainerMapping] = []
                    for record in value:
                        match record:
                            case Mapping():
                                record_dict: t.MutableFlatContainerMapping = {}
                                for key, item in record.items():
                                    if u.primitive(item):
                                        record_dict[str(key)] = item
                                records.append(record_dict)
                            case _:
                                continue
                    return records
                case _:
                    return []

    class ConfigMappingPayload(m.ArbitraryTypesModel):
        """Normalized mapping payload with string keys."""

        _flext_enforcement_exempt: ClassVar[bool] = True

        values: Annotated[
            t.Cli.JsonMapping,
            u.Field(description="Normalized mapping values"),
        ] = u.Field(default_factory=dict)

        @u.field_validator("values", mode="before")
        @classmethod
        def normalize_values(
            cls,
            value: t.Meltano.ValidatorInput,
        ) -> t.Cli.JsonMapping:
            """Normalize mapping-like payloads through the canonical CLI JSON adapter."""
            if not isinstance(value, Mapping):
                return {}
            return t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)

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
                    return u.Cli.yaml_dump_str(dict(value))
                case None:
                    return ""
                case _:
                    return str(value)

    class VariantPayload(m.ArbitraryTypesModel):
        """Normalize plugin variant from external extraction (str|list|dict)."""

        value: Annotated[
            t.Meltano.VariantValue,
            u.Field(description="Normalized variant value"),
        ] = None

        @u.field_validator("value", mode="before")
        @classmethod
        def normalize_variant(
            cls,
            value: str | t.Meltano.ValidatorInput,
        ) -> t.Meltano.VariantValue:
            """Normalize variant payload through the canonical CLI JSON adapter."""
            match value:
                case None:
                    return None
                case str():
                    return value
                case list() | tuple():
                    return [str(item) for item in value]
                case Mapping():
                    return t.Cli.JSON_MAPPING_ADAPTER.validate_python(value)
                case _:
                    return str(value)
