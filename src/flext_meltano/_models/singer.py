"""FLEXT Meltano models - Singer protocol message models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated, Self

from flext_cli import m

from flext_meltano import c, t
from flext_meltano._models.base import FlextMeltanoModelsBase


class FlextMeltanoModelsSinger:
    """Singer protocol message models."""

    class SingerSchemaMessage(m.ArbitraryTypesModel):
        """Canonical Singer SCHEMA message model."""

        # Why: mro-4p0t — accept StrEnum SSOT at call sites (flext-target-oracle-wms).
        type: Annotated[
            c.Meltano.SingerMessageType,
            m.Field(
                default=c.Meltano.SingerMessageType.SCHEMA,
                description="Singer message discriminator",
            ),
        ] = c.Meltano.SingerMessageType.SCHEMA
        stream: Annotated[t.NonEmptyStr, m.Field(description="Singer stream name")]
        schema_definition: Annotated[
            t.FlatContainerMapping,
            m.Field(
                alias="schema",
                serialization_alias="schema",
                validation_alias=t.AliasChoices("schema", "schema_definition"),
                description="Singer JSON schema payload",
            ),
        ]
        key_properties: Annotated[
            t.StrTuple,
            m.Field(description="Singer stream key properties"),
        ] = m.Field(
            default_factory=tuple[str, ...],
            description="Singer stream key properties",
        )
        bookmark_properties: Annotated[
            t.StrTuple,
            m.Field(description="Singer bookmark columns for incremental replication"),
        ] = m.Field(
            default_factory=tuple[str, ...],
            description="Singer bookmark columns for incremental replication",
        )
        intermediate_encodings: Annotated[
            t.StrTuple,
            m.Field(
                default_factory=tuple[str, ...],
                description="Singer intermediate encodings (e.g. 'utf8')",
            ),
        ] = m.Field(
            default_factory=tuple[str, ...],
            description="Singer intermediate encodings",
        )

    class SingerRecordMessage(m.ArbitraryTypesModel):
        """Canonical Singer RECORD message model."""

        type: Annotated[
            c.Meltano.SingerMessageType,
            m.Field(
                default=c.Meltano.SingerMessageType.RECORD,
                description="Singer message discriminator",
            ),
        ] = c.Meltano.SingerMessageType.RECORD
        stream: Annotated[str, m.Field(description="Singer stream name")]
        record: Annotated[
            t.FlatContainerMapping,
            m.Field(description="Singer record payload"),
        ]
        time_extracted: Annotated[
            str | None,
            m.Field(
                default=None,
                description="ISO 8601 timestamp when the record was extracted",
            ),
        ] = None
        version: Annotated[
            int | None,
            m.Field(
                default=None,
                description="Stream version number for activate_version protocol",
            ),
        ] = None

    class SingerStateMessage(m.ArbitraryTypesModel):
        """Canonical Singer STATE message model."""

        type: Annotated[
            c.Meltano.SingerMessageType,
            m.Field(
                default=c.Meltano.SingerMessageType.STATE,
                description="Singer message discriminator",
            ),
        ] = c.Meltano.SingerMessageType.STATE
        value: Annotated[
            t.MutableFlatContainerMapping,
            m.Field(description="Singer state bookmark payload"),
        ] = m.Field(
            default_factory=dict[str, t.JsonValue],
            description="Singer state bookmark payload",
        )

    class SingerActivateVersionMessage(m.ArbitraryTypesModel):
        """Canonical Singer ACTIVATE_VERSION message model.

        Sent by a tap to signal that all records for a stream version
        have been emitted. The target should remove any records not
        matching this version.
        """

        type: Annotated[
            c.Meltano.SingerMessageType,
            m.Field(
                default=c.Meltano.SingerMessageType.ACTIVATE_VERSION,
                description="Singer message discriminator",
            ),
        ] = c.Meltano.SingerMessageType.ACTIVATE_VERSION
        stream: Annotated[str, m.Field(description="Singer stream name")]
        version: Annotated[
            t.PositiveInt,
            m.Field(description="Stream version to activate"),
        ]

    class SingerStateEntry(FlextMeltanoModelsBase.EventedEntity):
        """Singer state entry for a stream bookmark.

        Tracks per-stream incremental sync bookmarks with validation
        ensuring bookmark_key and bookmark_value are both set or both None.
        """

        stream_name: Annotated[str, m.Field(description="Name of the stream")]
        bookmark_key: Annotated[
            str | None,
            m.Field(default=None, description="Bookmark field for incremental"),
        ] = None
        bookmark_value: Annotated[
            str | None,
            m.Field(default=None, description="Current bookmark value"),
        ] = None

        @m.model_validator(mode="after")
        def validate_bookmark(self) -> Self:
            """Ensure bookmark_key and bookmark_value are both set or both None.

            Returns:
                The resulting ``Self``.

            Raises:
                ValueError: If bookmark_key and bookmark_value must both be set or both
                    be None.
            """
            if (self.bookmark_key is None) != (self.bookmark_value is None):
                msg = "bookmark_key and bookmark_value must both be set or both be None"
                raise ValueError(msg)
            return self

    class StreamSpec(FlextMeltanoModelsBase.EventedEntity):
        """Declarative Singer stream specification."""

        name: Annotated[str, m.Field(description="Stream name")]
        json_schema: Annotated[
            t.FlatContainerMapping,
            m.Field(description="JSON schema for the stream"),
        ]
        primary_keys: Annotated[
            t.StrTuple,
            m.Field(description="Primary key properties"),
        ] = m.Field(
            default_factory=tuple[str, ...],
            description="Primary key properties",
        )
        replication_key: Annotated[
            str | None,
            m.Field(default=None, description="Incremental replication key"),
        ] = None

    class TapSpec(FlextMeltanoModelsBase.EventedEntity):
        """Declarative Singer tap specification."""

        tap_name: Annotated[str, m.Field(description="Tap name")]
        config_jsonschema: Annotated[
            t.FlatContainerMapping,
            m.Field(description="Tap config JSON schema"),
        ]
        streams: Annotated[
            tuple[FlextMeltanoModelsSinger.StreamSpec, ...],
            m.Field(description="Declared tap streams"),
        ]

    class FetchRequest(FlextMeltanoModelsBase.EventedEntity):
        """Record fetch request passed to a declarative tap fetcher."""

        stream_name: Annotated[str, m.Field(description="Stream name to fetch")]
        config: Annotated[
            t.JsonMapping,
            m.Field(description="Runtime tap configuration"),
        ] = m.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
            description="Runtime tap configuration",
        )

        @m.field_validator("config", mode="after")
        @classmethod
        def freeze_config(cls, value: t.JsonMapping) -> t.JsonMapping:
            """Expose runtime tap configuration as read-only.

            Returns:
                The resulting ``t.JsonMapping``.
            """
            return MappingProxyType(dict(value))

    class FetchResult(FlextMeltanoModelsBase.EventedEntity):
        """Record fetch result returned by a declarative tap fetcher."""

        records: Annotated[
            t.VariadicTuple[t.JsonMapping],
            m.Field(description="Fetched records"),
        ] = m.Field(
            default_factory=tuple[t.JsonMapping, ...],
            description="Fetched records",
        )
