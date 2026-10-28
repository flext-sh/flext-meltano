"""FLEXT Meltano typings - Singer protocol types.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

import singer_sdk.singerlib as singer_sdk_singerlib


class FlextMeltanoTypingsSinger:
    """Singer protocol type definitions.

    All aliases are FLAT namespace with ``Singer`` prefix. The Singer SDK
    typing wrappers live once on ``m.Meltano`` (flext-meltano owns singer_sdk).
    """

    # Singer SDK wire-format schema. ``t.Meltano.SingerSchema`` is the PEP 695
    # alias for type positions; the tap-facing runtime class for ``isinstance``
    # and schema construction is ``m.Meltano.SingerSchema`` (flext-meltano owns
    # singer_sdk).
    type SingerSchema = singer_sdk_singerlib.Schema


__all__: list[str] = ["FlextMeltanoTypingsSinger"]
