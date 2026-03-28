"""FLEXT Meltano models - Singer protocol message models."""

from __future__ import annotations

from typing import Annotated, Literal, Self

from flext_cli import FlextCliModels
from pydantic import Field, model_validator

from flext_meltano import t


class FlextMeltanoModelsSinger:
    """Singer protocol message models."""

    class SingerSchemaMessage(FlextCliModels.ArbitraryTypesModel):
        """Canonical Singer SCHEMA message model."""

        type: Annotated[
            Literal["SCHEMA"],
            Field(default="SCHEMA", description="Singer message discriminator"),
        ] = "SCHEMA"
        stream: Annotated[t.NonEmptyStr, Field(description="Singer stream name")]
        schema_definition: Annotated[
            t.FlatContainerMapping,
            Field(
                alias="schema",
                serialization_alias="schema",
                validation_alias="schema",
                description="Singer JSON schema payload",
            ),
        ]
        key_properties: Annotated[
            t.StrSequence, Field(description="Singer stream key properties")
        ] = Field(default_factory=list)
        bookmark_properties: Annotated[
            t.StrSequence,
            Field(description="Singer bookmark columns for incremental replication"),
        ] = Field(default_factory=list)

    class SingerRecordMessage(FlextCliModels.ArbitraryTypesModel):
        """Canonical Singer RECORD message model."""

        type: Annotated[
            Literal["RECORD"],
            Field(default="RECORD", description="Singer message discriminator"),
        ] = "RECORD"
        stream: Annotated[str, Field(description="Singer stream name")]
        record: Annotated[
            t.FlatContainerMapping, Field(description="Singer record payload")
        ]
        time_extracted: Annotated[
            str | None,
            Field(
                default=None,
                description="ISO 8601 timestamp when the record was extracted",
            ),
        ] = None
        version: Annotated[
            int | None,
            Field(
                default=None,
                description="Stream version number for activate_version protocol",
            ),
        ] = None

    class SingerStateMessage(FlextCliModels.ArbitraryTypesModel):
        """Canonical Singer STATE message model."""

        type: Annotated[
            Literal["STATE"],
            Field(default="STATE", description="Singer message discriminator"),
        ] = "STATE"
        value: Annotated[
            t.MutableContainerMapping,
            Field(description="Singer state bookmark payload"),
        ] = Field(default_factory=dict)

    class SingerActivateVersionMessage(FlextCliModels.ArbitraryTypesModel):
        """Canonical Singer ACTIVATE_VERSION message model.

        Sent by a tap to signal that all records for a stream version
        have been emitted. The target should remove any records not
        matching this version.
        """

        type: Annotated[
            Literal["ACTIVATE_VERSION"],
            Field(
                default="ACTIVATE_VERSION", description="Singer message discriminator"
            ),
        ] = "ACTIVATE_VERSION"
        stream: Annotated[str, Field(description="Singer stream name")]
        version: Annotated[
            t.PositiveInt, Field(description="Stream version to activate")
        ]

    class SingerStateEntry(FlextCliModels.Entity):
        """Singer state entry for a stream bookmark.

        Tracks per-stream incremental sync bookmarks with validation
        ensuring bookmark_key and bookmark_value are both set or both None.
        """

        stream_name: Annotated[str, Field(description="Name of the stream")]
        bookmark_key: Annotated[
            str | None,
            Field(default=None, description="Bookmark field for incremental"),
        ] = None
        bookmark_value: Annotated[
            str | None, Field(default=None, description="Current bookmark value")
        ] = None

        @model_validator(mode="after")
        def validate_bookmark(self) -> Self:
            """Ensure bookmark_key and bookmark_value are both set or both None."""
            if (self.bookmark_key is None) != (self.bookmark_value is None):
                msg = "bookmark_key and bookmark_value must both be set or both be None"
                raise ValueError(msg)
            return self
