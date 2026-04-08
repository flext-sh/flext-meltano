"""FLEXT Meltano typings - Singer protocol types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from flext_cli import t

from flext_meltano import FlextMeltanoModelsSingerSdk, c


class FlextMeltanoTypingsSinger:
    """Singer protocol type definitions.

    All aliases are FLAT namespace with ``Singer`` prefix.
    External library wrappers (singer_sdk.typing) are kept to prevent
    direct imports by consumer projects.
    """

    type SingerCatalogEntry = Mapping[
        str,
        str | Mapping[str, t.Scalar | None],
    ]
    type SingerStreamCatalog = Mapping[
        str,
        Sequence[FlextMeltanoTypingsSinger.SingerCatalogEntry],
    ]

    SingerReplicationMethod = c.Meltano.SingerReplicationMethod

    # Singer SDK typing wrappers stay behind the Meltano model boundary.
    SingerArrayType = FlextMeltanoModelsSingerSdk.SingerArrayType
    SingerBooleanType = FlextMeltanoModelsSingerSdk.SingerBooleanType
    SingerCustomType = FlextMeltanoModelsSingerSdk.SingerCustomType
    SingerDateTimeType = FlextMeltanoModelsSingerSdk.SingerDateTimeType
    SingerDateType = FlextMeltanoModelsSingerSdk.SingerDateType
    SingerDurationType = FlextMeltanoModelsSingerSdk.SingerDurationType
    SingerIntegerType = FlextMeltanoModelsSingerSdk.SingerIntegerType
    SingerNumberType = FlextMeltanoModelsSingerSdk.SingerNumberType
    SingerObjectType = FlextMeltanoModelsSingerSdk.SingerObjectType
    SingerPropertiesList = FlextMeltanoModelsSingerSdk.SingerPropertiesList
    SingerProperty = FlextMeltanoModelsSingerSdk.SingerProperty
    SingerStringType = FlextMeltanoModelsSingerSdk.SingerStringType
    SingerTimeType = FlextMeltanoModelsSingerSdk.SingerTimeType
