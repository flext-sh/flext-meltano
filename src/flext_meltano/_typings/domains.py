"""FLEXT Meltano typings.

Domain-specific types (Dbt, Project, Bridge, CLI, ELT, Processing).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping

from flext_cli import t

from flext_meltano import c


class FlextMeltanoTypingsDomains:
    """Domain-specific type definitions for Meltano subsystems.

    All aliases are FLAT namespace with descriptive prefixes.
    No nested classes. No duplicates. No simple aliases to existing ``t.*``.
    """

    type NestedStrMapping = Mapping[str, t.StrMapping]
    type DbtManifestData = t.JsonMapping
    type DbtProject = t.JsonMapping

    PluginType = c.Meltano.PluginType

    type EnvironmentInput = c.Meltano.Environment | t.JsonMapping
    """Environment selector input: a named environment or a full environment
    configuration mapping."""
