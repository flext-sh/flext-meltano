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
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_meltano.dbt import project, runner, service
    from flext_meltano.dbt.project import FlextMeltanoDbtProjectManager
    from flext_meltano.dbt.runner import FlextMeltanoDbtRunner
    from flext_meltano.dbt.service import FlextMeltanoDbtService

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextMeltanoDbtProjectManager": "flext_meltano.dbt.project",
    "FlextMeltanoDbtRunner": "flext_meltano.dbt.runner",
    "FlextMeltanoDbtService": "flext_meltano.dbt.service",
    "project": "flext_meltano.dbt.project",
    "runner": "flext_meltano.dbt.runner",
    "service": "flext_meltano.dbt.service",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
