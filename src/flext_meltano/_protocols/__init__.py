# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Protocols package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_meltano import cli, plugin, project, services, singer
    from flext_meltano.cli import FlextMeltanoProtocolsBase
    from flext_meltano.plugin import FlextMeltanoProtocolsPlugin
    from flext_meltano.project import FlextMeltanoProtocolsProject
    from flext_meltano.services import FlextMeltanoProtocolsServices
    from flext_meltano.singer import FlextMeltanoProtocolsSinger

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextMeltanoProtocolsBase": "flext_meltano.cli",
    "FlextMeltanoProtocolsPlugin": "flext_meltano.plugin",
    "FlextMeltanoProtocolsProject": "flext_meltano.project",
    "FlextMeltanoProtocolsServices": "flext_meltano.services",
    "FlextMeltanoProtocolsSinger": "flext_meltano.singer",
    "cli": "flext_meltano.cli",
    "plugin": "flext_meltano.plugin",
    "project": "flext_meltano.project",
    "services": "flext_meltano.services",
    "singer": "flext_meltano.singer",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
