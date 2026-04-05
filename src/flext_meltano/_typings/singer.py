"""FLEXT Meltano typings - Singer protocol types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

import singer_sdk.typing as singer_sdk_typing
from flext_cli import FlextCliTypes

from flext_meltano import c


class FlextMeltanoTypingsSinger:
    """Singer protocol type definitions.

    All aliases are FLAT namespace with ``Singer`` prefix.
    External library wrappers (singer_sdk.typing) are kept to prevent
    direct imports by consumer projects.
    """

    type SingerCatalogEntry = Mapping[
        str,
        str | Mapping[str, FlextCliTypes.Scalar | None],
    ]
    type SingerStreamCatalog = Mapping[
        str,
        Sequence[FlextMeltanoTypingsSinger.SingerCatalogEntry],
    ]

    SingerReplicationMethod = c.Meltano.SingerReplicationMethod

    # Singer SDK typing wrappers — prevents direct ``singer_sdk.typing`` imports
    SingerArrayType = singer_sdk_typing.ArrayType
    SingerBooleanType = singer_sdk_typing.BooleanType
    SingerCustomType = singer_sdk_typing.CustomType
    SingerDateTimeType = singer_sdk_typing.DateTimeType
    SingerDateType = singer_sdk_typing.DateType
    SingerDurationType = singer_sdk_typing.DurationType
    SingerIntegerType = singer_sdk_typing.IntegerType
    SingerNumberType = singer_sdk_typing.NumberType
    SingerObjectType = singer_sdk_typing.ObjectType
    SingerPropertiesList = singer_sdk_typing.PropertiesList
    SingerProperty = singer_sdk_typing.Property
    SingerStringType = singer_sdk_typing.StringType
    SingerTimeType = singer_sdk_typing.TimeType
