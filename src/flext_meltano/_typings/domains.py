"""FLEXT Meltano typings.

Domain-specific types (Dbt, Project, Bridge, CLI, ELT, Processing).

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

from collections.abc import Mapping

from flext_cli import t


class FlextMeltanoTypingsDomains:
    """Domain-specific type definitions for Meltano subsystems.

    All aliases are FLAT namespace with descriptive prefixes.
    No nested classes. No duplicates. No simple aliases to existing ``t.*``.
    """

    type NestedStrMapping = Mapping[str, Mapping[str, str]]
    type DbtProject = t.JsonMapping


__all__: list[str] = ["FlextMeltanoTypingsDomains"]
