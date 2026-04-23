"""FLEXT Meltano typings - Domain-specific types (Dbt, Project, Bridge, CLI, ELT, Processing).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Callable,
    Mapping,
    Sequence,
)

from flext_cli import t
from flext_core import r

from flext_meltano import c


class FlextMeltanoTypingsDomains:
    """Domain-specific type definitions for Meltano subsystems.

    All aliases are FLAT namespace with descriptive prefixes.
    No nested classes. No duplicates. No simple aliases to existing ``t.*``.
    """

    type NestedStrMapping = Mapping[str, t.StrMapping]
    type EnvironmentInput = c.Meltano.Environment | c.Meltano.EnvironmentAlias
    type ProjectEnvironmentNames = Sequence[c.Meltano.ProjectEnvironment]
    type ServicePayload = t.JsonMapping
    type DbtManifestData = t.JsonMapping
    type DbtProject = t.JsonMapping
    type PublicFactory[TService] = Callable[..., r[TService]]
