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
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_meltano.meltano import (
        pipelines,
        plugin_discovery,
        plugins,
        project,
        runner,
        service,
    )
    from flext_meltano.meltano.pipelines import FlextMeltanoOrchestrationService
    from flext_meltano.meltano.plugin_discovery import FlextMeltanoPluginDiscoveryMixin
    from flext_meltano.meltano.plugins import FlextMeltanoComponentService
    from flext_meltano.meltano.project import FlextMeltanoProjectManager
    from flext_meltano.meltano.runner import (
        FlextMeltanoDbtTransformationRunner,
        FlextMeltanoLibraryRunner,
    )
    from flext_meltano.meltano.service import FlextMeltanoMeltanoService

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextMeltanoComponentService": "flext_meltano.meltano.plugins",
    "FlextMeltanoDbtTransformationRunner": "flext_meltano.meltano.runner",
    "FlextMeltanoLibraryRunner": "flext_meltano.meltano.runner",
    "FlextMeltanoMeltanoService": "flext_meltano.meltano.service",
    "FlextMeltanoOrchestrationService": "flext_meltano.meltano.pipelines",
    "FlextMeltanoPluginDiscoveryMixin": "flext_meltano.meltano.plugin_discovery",
    "FlextMeltanoProjectManager": "flext_meltano.meltano.project",
    "pipelines": "flext_meltano.meltano.pipelines",
    "plugin_discovery": "flext_meltano.meltano.plugin_discovery",
    "plugins": "flext_meltano.meltano.plugins",
    "project": "flext_meltano.meltano.project",
    "runner": "flext_meltano.meltano.runner",
    "service": "flext_meltano.meltano.service",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
