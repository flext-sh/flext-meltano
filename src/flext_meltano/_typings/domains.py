"""FLEXT Meltano typings - Domain-specific types (Dbt, Project, Bridge, CLI, ELT, Processing).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping

from flext_cli import FlextCliTypes


class FlextMeltanoTypingsDomains:
    """Domain-specific type definitions for Meltano subsystems.

    All aliases are FLAT namespace with descriptive prefixes.
    No nested classes. No duplicates. No simple aliases to existing ``t.*``.
    """

    type NestedStrMapping = Mapping[str, FlextCliTypes.StrMapping]
    type DbtManifestData = Mapping[
        str,
        Mapping[str, FlextCliTypes.ContainerValue] | None,
    ]
    type DbtProject = Mapping[str, str | bool | FlextCliTypes.StrSequence]
