"""FLEXT Meltano typings - Domain-specific types (Dbt, Project, Bridge, CLI, ELT, Processing).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Callable,
    Mapping,
)
from typing import Literal

from flext_cli import t
from flext_core import r


class FlextMeltanoTypingsDomains:
    """Domain-specific type definitions for Meltano subsystems.

    All aliases are FLAT namespace with descriptive prefixes.
    No nested classes. No duplicates. No simple aliases to existing ``t.*``.
    """

    type NestedStrMapping = Mapping[str, t.StrMapping]
    type DbtManifestData = Mapping[
        str,
        Mapping[str, t.Container] | None,
    ]
    type DbtProject = Mapping[str, str | bool | t.StrSequence]
    type PublicFactory[TService] = Callable[..., r[TService]]
    type PublicFactoryName = Literal["Tap", "Target", "Dbt"]
