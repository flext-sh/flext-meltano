"""FLEXT Meltano models - Data normalization payload models."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, MutableSequence, Sequence
from pathlib import Path
from typing import Annotated

from flext_cli import m, u
from pydantic import Field, field_validator

from flext_meltano import t


class FlextMeltanoModelsPayloadsData:
    """Data normalization payload models with validators."""

    class JsonSchemaPayload(m.ArbitraryTypesModel):
        """Typed schema payload used by API extract flow."""

        schema_definition: Annotated[
            t.FlatContainerMapping,
            Field(
                alias="schema",
                serialization_alias="schema",
                validation_alias="schema",
                description="Schema-like JSON payload",
            ),
        ] = Field(default_factory=dict, description="Schema-like JSON payload")

        @field_validator("schema_definition", mode="before")
        @classmethod
        def normalize_schema(
            cls, value: t.Meltano.ValidatorInput
        ) -> t.FlatContainerMapping:
            """Normalize mapping input before JSON validation."""
            match value:
                case Mapping():
                    return {str(key): item for key, item in value.items()}
                case _:
                    empty_schema: t.FlatContainerMapping = {}
                    return empty_schema

    class JsonRecordBatchPayload(m.ArbitraryTypesModel):
        """Typed record batch payload used by API load flow."""

        records: Annotated[
            Sequence[t.FlatContainerMapping],
            Field(description="Normalized record payloads"),
        ] = Field(
            default_factory=lambda: list[t.FlatContainerMapping](),
            description="Normalized record payloads",
        )

        @field_validator("records", mode="before")
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
                                    if u.is_primitive(item):
                                        record_dict[str(key)] = item
                                records.append(record_dict)
                            case _:
                                continue
                    return records
                case _:
                    return []

    class ConfigMappingPayload(m.ArbitraryTypesModel):
        """Normalized mapping payload with string keys."""

        values: Annotated[
            Mapping[
                str,
                t.Scalar
                | Sequence[t.Scalar | None]
                | Mapping[str, t.Scalar | None]
                | None,
            ],
            Field(description="Normalized mapping values"),
        ] = Field(default_factory=dict, description="Normalized mapping values")

        @field_validator("values", mode="before")
        @classmethod
        def normalize_values(
            cls,
            value: t.Meltano.ValidatorInput,
        ) -> Mapping[
            str,
            t.Scalar | Sequence[t.Scalar | None] | Mapping[str, t.Scalar | None] | None,
        ]:
            """Normalize mapping-like payloads to Mapping[str, value]."""
            if not isinstance(value, Mapping):
                return {}
            result: MutableMapping[
                str,
                t.Scalar
                | Sequence[t.Scalar | None]
                | Mapping[str, t.Scalar | None]
                | None,
            ] = {}
            for key, item in value.items():
                if u.is_scalar(item) or item is None:
                    result[str(key)] = item
                elif isinstance(item, list):
                    result[str(key)] = [
                        v if u.is_scalar(v) or v is None else str(v) for v in item
                    ]
                elif isinstance(item, Mapping):
                    result[str(key)] = {
                        str(k): v if u.is_scalar(v) or v is None else str(v)
                        for k, v in item.items()
                    }
                else:
                    result[str(key)] = str(item)
            return result

    class PathPayload(m.ArbitraryTypesModel):
        """Path normalization payload for runtime path conversions."""

        value: Annotated[Path, Field(description="Normalized path")] = Field(
            default_factory=Path, description="Normalized path"
        )

        @field_validator("value", mode="before")
        @classmethod
        def normalize_path(cls, value: t.Meltano.ValidatorInput) -> Path:
            """Normalize mixed path input into Path objects."""
            if value is None:
                return Path()
            return Path(str(value))

    class FileContentPayload(m.ArbitraryTypesModel):
        """Normalize str|dict content to writable string for file operations."""

        content: Annotated[
            str, Field(default="", description="Normalized writable string content")
        ] = ""

        @field_validator("content", mode="before")
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

        value: t.Meltano.VariantValue = Field(
            default=None, description="Normalized variant value"
        )

        @field_validator("value", mode="before")
        @classmethod
        def normalize_variant(
            cls,
            value: str | t.Meltano.ValidatorInput,
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
                        if u.is_primitive(v):
                            result[str(k)] = v
                        elif v is None:
                            result[str(k)] = ""
                        elif isinstance(v, (list, dict)):
                            result[str(k)] = str(v)
                    return result
                case _:
                    return str(value)
