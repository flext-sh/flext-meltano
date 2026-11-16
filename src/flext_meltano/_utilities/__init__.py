# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._utilities.base import FlextMeltanoUtilitiesBase
    from flext_meltano._utilities.runtime import FlextMeltanoUtilitiesRuntime
    from flext_meltano._utilities.singer import FlextMeltanoUtilitiesSinger


__all__: tuple[str, ...] = (
    "FlextMeltanoUtilitiesBase",
    "FlextMeltanoUtilitiesRuntime",
    "FlextMeltanoUtilitiesSinger",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextMeltanoUtilitiesBase": ".base",
        "FlextMeltanoUtilitiesRuntime": ".runtime",
        "FlextMeltanoUtilitiesSinger": ".singer",
    },
    public_exports=__all__,
    deferred_members={
        "FlextMeltanoUtilitiesRuntime": (
            "_normalized_parts",
            "normalize_runtime_command",
            "normalize_plugin_group",
            "requests_help",
            "resolve_project_root",
            "normalize_environment_name",
            "build_dbt_runtime_command",
            "build_discovered_project_plugin",
            "discover_project_plugins",
            "build_plugin_discovery_item",
        ),
        "FlextMeltanoUtilitiesSinger": (
            "process_stdin",
            "_process_stdin_line",
            "_dispatch_singer_message",
            "_handle_schema_message",
            "_handle_record_message",
            "_handle_state_message",
            "build_catalog_entry",
        ),
    },
)
