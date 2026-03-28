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
    """Singer protocol type definitions."""

    class Singer:
        """Singer protocol complex types namespace."""

        type CatalogEntry = Mapping[
            str,
            str | Mapping[str, FlextCliTypes.Scalar | None],
        ]
        type StreamSchema = Mapping[str, Mapping[str, FlextCliTypes.Scalar | None]]
        type TapConfig = Mapping[
            str,
            Mapping[str, FlextCliTypes.ContainerValue] | None,
        ]
        type TargetConfig = Mapping[
            str,
            Mapping[str, FlextCliTypes.ContainerValue] | None,
        ]
        type MessageBatch = Sequence[Mapping[str, FlextCliTypes.Scalar | None]]
        type StreamCatalog = Mapping[
            str,
            Sequence[FlextMeltanoTypingsSinger.Singer.CatalogEntry],
        ]
        type Record = Mapping[str, FlextCliTypes.Scalar | None]
        type Schema = Mapping[str, FlextCliTypes.Scalar | None]
        type State = Mapping[str, FlextCliTypes.Scalar | None]
        ReplicationMethod = c.Meltano.Enums.ReplicationMethod
        SingerVersion = str  # "0.44.0" | "0.45.0" | ...

        class Typing:
            """Singer SDK typing utilities wrapper (Zero Tolerance for direct imports).

            This class provides access to all Singer SDK typing utilities through FLEXT
            domain separation pattern. ALL tap/target projects MUST use this instead of
            importing directly from singer_sdk.typing.

            Usage:
                from flext_meltano import FlextMeltanoTypes

                schema = FlextMeltanoTypes.Singer.Typing.PropertiesList(
                    FlextMeltanoTypes.Singer.Typing.Property("id", FlextMeltanoTypes.Singer.Typing.StringType),
                    FlextMeltanoTypes.Singer.Typing.Property("count", FlextMeltanoTypes.Singer.Typing.IntegerType),
                ).to_dict()
            """

            ArrayType = singer_sdk_typing.ArrayType
            BooleanType = singer_sdk_typing.BooleanType
            CustomType = singer_sdk_typing.CustomType
            DateTimeType = singer_sdk_typing.DateTimeType
            DateType = singer_sdk_typing.DateType
            DurationType = singer_sdk_typing.DurationType
            IntegerType = singer_sdk_typing.IntegerType
            NumberType = singer_sdk_typing.NumberType
            ObjectType = singer_sdk_typing.ObjectType
            PropertiesList = singer_sdk_typing.PropertiesList
            Property = singer_sdk_typing.Property
            StringType = singer_sdk_typing.StringType
            TimeType = singer_sdk_typing.TimeType
