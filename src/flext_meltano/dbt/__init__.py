# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""DBT Transformations for FLEXT Meltano.

This module provides deep integration with dbt-core for project management,
model execution, and data transformation operations with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_meltano.dbt.project import FlextMeltanoDbtProjectManager
    from flext_meltano.dbt.runner import FlextMeltanoDbtRunner
    from flext_meltano.dbt.service import FlextMeltanoDbtService

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextMeltanoDbtProjectManager": (
        "flext_meltano.dbt.project",
        "FlextMeltanoDbtProjectManager",
    ),
    "FlextMeltanoDbtRunner": ("flext_meltano.dbt.runner", "FlextMeltanoDbtRunner"),
    "FlextMeltanoDbtService": ("flext_meltano.dbt.service", "FlextMeltanoDbtService"),
}

__all__ = [
    "FlextMeltanoDbtProjectManager",
    "FlextMeltanoDbtRunner",
    "FlextMeltanoDbtService",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
