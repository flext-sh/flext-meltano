"""FLEXT Meltano typings - Domain-specific types (Dbt, Project, Bridge, CLI, ELT, Processing).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import (
    Mapping,
)

from flext_cli import t

from flext_meltano import c


class FlextMeltanoTypingsDomains:
    """Domain-specific type definitions for Meltano subsystems."""

    type NestedStrMapping = Mapping[str, t.StrMapping]
    type EnvironmentInput = c.Meltano.Environment | c.Meltano.EnvironmentAlias
    type ServicePayload = t.JsonMapping
    type DbtManifestData = t.JsonMapping
    type DbtProject = t.JsonMapping
