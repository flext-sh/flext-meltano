# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""DBT Transformations for FLEXT Meltano.

This module provides deep integration with dbt-core for project management,
model execution, and data transformation operations with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.dbt import (
        project as project,
        runner as runner,
        service as service,
    )
    from flext_meltano.dbt.project import (
        FlextMeltanoDbtProjectManager as FlextMeltanoDbtProjectManager,
    )
    from flext_meltano.dbt.runner import FlextMeltanoDbtRunner as FlextMeltanoDbtRunner
    from flext_meltano.dbt.service import (
        FlextMeltanoDbtService as FlextMeltanoDbtService,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoDbtProjectManager": [
        "flext_meltano.dbt.project",
        "FlextMeltanoDbtProjectManager",
    ],
    "FlextMeltanoDbtRunner": ["flext_meltano.dbt.runner", "FlextMeltanoDbtRunner"],
    "FlextMeltanoDbtService": ["flext_meltano.dbt.service", "FlextMeltanoDbtService"],
    "project": ["flext_meltano.dbt.project", ""],
    "runner": ["flext_meltano.dbt.runner", ""],
    "service": ["flext_meltano.dbt.service", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextMeltanoDbtProjectManager",
    "FlextMeltanoDbtRunner",
    "FlextMeltanoDbtService",
    "project",
    "runner",
    "service",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
