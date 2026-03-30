# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Meltano Integration for FLEXT Ecosystem.

This module provides deep integration with meltano-sdk for project management,
plugin operations, and pipeline orchestration with FLEXT ecosystem patterns
and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.meltano import (
        pipelines as pipelines,
        plugin_discovery as plugin_discovery,
        plugins as plugins,
        project as project,
        runner as runner,
        service as service,
    )
    from flext_meltano.meltano.pipelines import (
        FlextMeltanoOrchestrationService as FlextMeltanoOrchestrationService,
    )
    from flext_meltano.meltano.plugin_discovery import (
        FlextMeltanoPluginDiscoveryMixin as FlextMeltanoPluginDiscoveryMixin,
    )
    from flext_meltano.meltano.plugins import (
        FlextMeltanoComponentService as FlextMeltanoComponentService,
    )
    from flext_meltano.meltano.project import (
        FlextMeltanoProjectManager as FlextMeltanoProjectManager,
    )
    from flext_meltano.meltano.runner import (
        FlextMeltanoDbtTransformationRunner as FlextMeltanoDbtTransformationRunner,
        FlextMeltanoLibraryRunner as FlextMeltanoLibraryRunner,
    )
    from flext_meltano.meltano.service import (
        FlextMeltanoMeltanoService as FlextMeltanoMeltanoService,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoComponentService": [
        "flext_meltano.meltano.plugins",
        "FlextMeltanoComponentService",
    ],
    "FlextMeltanoDbtTransformationRunner": [
        "flext_meltano.meltano.runner",
        "FlextMeltanoDbtTransformationRunner",
    ],
    "FlextMeltanoLibraryRunner": [
        "flext_meltano.meltano.runner",
        "FlextMeltanoLibraryRunner",
    ],
    "FlextMeltanoMeltanoService": [
        "flext_meltano.meltano.service",
        "FlextMeltanoMeltanoService",
    ],
    "FlextMeltanoOrchestrationService": [
        "flext_meltano.meltano.pipelines",
        "FlextMeltanoOrchestrationService",
    ],
    "FlextMeltanoPluginDiscoveryMixin": [
        "flext_meltano.meltano.plugin_discovery",
        "FlextMeltanoPluginDiscoveryMixin",
    ],
    "FlextMeltanoProjectManager": [
        "flext_meltano.meltano.project",
        "FlextMeltanoProjectManager",
    ],
    "pipelines": ["flext_meltano.meltano.pipelines", ""],
    "plugin_discovery": ["flext_meltano.meltano.plugin_discovery", ""],
    "plugins": ["flext_meltano.meltano.plugins", ""],
    "project": ["flext_meltano.meltano.project", ""],
    "runner": ["flext_meltano.meltano.runner", ""],
    "service": ["flext_meltano.meltano.service", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextMeltanoComponentService",
    "FlextMeltanoDbtTransformationRunner",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoMeltanoService",
    "FlextMeltanoOrchestrationService",
    "FlextMeltanoPluginDiscoveryMixin",
    "FlextMeltanoProjectManager",
    "pipelines",
    "plugin_discovery",
    "plugins",
    "project",
    "runner",
    "service",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
