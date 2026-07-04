"""FLEXT Meltano models - Singer protocol message models."""

from __future__ import annotations

from typing import Annotated, ClassVar

from flext_cli import m, u
from flext_meltano.constants import FlextMeltanoConstants as c
from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoModelsSinger:
    """Singer protocol message models."""

    class SingerSchemaMessage(m.ArbitraryTypesModel):
        """Canonical Singer SCHEMA message model."""

        model_config: ClassVar[m.ConfigDict] = m.ConfigDict(populate_by_name=True)

        type: Annotated[
            c.Meltano.SingerMessageType,
            u.Field(
                default=c.Meltano.SingerMessageType.SCHEMA,
                description="Singer message discriminator",
            ),
        ] = c.Meltano.SingerMessageType.SCHEMA
        stream: Annotated[t.NonEmptyStr, u.Field(description="Singer stream name")]
        schema_definition: Annotated[
            t.JsonMapping,
            u.Field(
                alias=c.Meltano.SchemaKey.SCHEMA,
                serialization_alias=c.Meltano.SchemaKey.SCHEMA,
                validation_alias=c.Meltano.SchemaKey.SCHEMA,
                description="Singer JSON schema payload",
            ),
        ]
        key_properties: Annotated[
            t.StrSequence,
            u.Field(description="Singer stream key properties"),
        ] = u.Field(default_factory=tuple)
        bookmark_properties: Annotated[
            t.StrSequence,
            u.Field(description="Singer bookmark columns for incremental replication"),
        ] = u.Field(default_factory=tuple)

    class SingerRecordMessage(m.ArbitraryTypesModel):
        """Canonical Singer RECORD message model."""

        type: Annotated[
            c.Meltano.SingerMessageType,
            u.Field(
                default=c.Meltano.SingerMessageType.RECORD,
                description="Singer message discriminator",
            ),
        ] = c.Meltano.SingerMessageType.RECORD
        stream: Annotated[str, u.Field(description="Singer stream name")]
        record: Annotated[t.JsonMapping, u.Field(description="Singer record payload")]
        time_extracted: Annotated[
            str | None,
            u.Field(
                default=None,
                description="ISO 8601 timestamp when the record was extracted",
            ),
        ] = None
        version: Annotated[
            int | None,
            u.Field(
                default=None,
                description="Stream version number for activate_version protocol",
            ),
        ] = None

    class SingerStateMessage(m.ArbitraryTypesModel):
        """Canonical Singer STATE message model."""

        type: Annotated[
            c.Meltano.SingerMessageType,
            u.Field(
                default=c.Meltano.SingerMessageType.STATE,
                description="Singer message discriminator",
            ),
        ] = c.Meltano.SingerMessageType.STATE
        value: Annotated[
            t.MutableJsonMapping,
            u.Field(description="Singer state bookmark payload"),
        ] = u.Field(default_factory=dict)

    class SingerActivateVersionMessage(m.ArbitraryTypesModel):
        """Canonical Singer ACTIVATE_VERSION message model.

        Sent by a tap to signal that all records for a stream version
        have been emitted. The target should remove any records not
        matching this version.
        """

        type: Annotated[
            c.Meltano.SingerMessageType,
            u.Field(
                default=c.Meltano.SingerMessageType.ACTIVATE_VERSION,
                description="Singer message discriminator",
            ),
        ] = c.Meltano.SingerMessageType.ACTIVATE_VERSION
        stream: Annotated[str, u.Field(description="Singer stream name")]
        version: Annotated[
            t.PositiveInt,
            u.Field(description="Stream version to activate"),
        ]
