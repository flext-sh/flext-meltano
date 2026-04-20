"""FLEXT Meltano typings - Singer protocol types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)

from flext_cli import t

from flext_meltano import c


class FlextMeltanoTypingsSinger:
    """Singer protocol type definitions.

    Singer contracts belong to ``t.Meltano`` and must avoid compatibility
    wrappers that mirror model-layer objects.
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
