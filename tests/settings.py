"""Runtime settings for flext-meltano tests.

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

from flext_tests import FlextTestsSettings

from flext_meltano import FlextMeltanoSettings


class TestsFlextMeltanoSettings(FlextMeltanoSettings, FlextTestsSettings):
    """Meltano settings extended with the shared test namespace."""


__all__: list[str] = ["TestsFlextMeltanoSettings"]
