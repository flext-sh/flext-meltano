# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano protocols submodules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_meltano._protocols import cli, plugin, project, services, singer
    from flext_meltano._protocols.cli import FlextMeltanoProtocolsBase
    from flext_meltano._protocols.plugin import FlextMeltanoProtocolsPlugin
    from flext_meltano._protocols.project import FlextMeltanoProtocolsProject
    from flext_meltano._protocols.services import FlextMeltanoProtocolsServices
    from flext_meltano._protocols.singer import FlextMeltanoProtocolsSinger

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextMeltanoProtocolsBase": "flext_meltano._protocols.cli",
    "FlextMeltanoProtocolsPlugin": "flext_meltano._protocols.plugin",
    "FlextMeltanoProtocolsProject": "flext_meltano._protocols.project",
    "FlextMeltanoProtocolsServices": "flext_meltano._protocols.services",
    "FlextMeltanoProtocolsSinger": "flext_meltano._protocols.singer",
    "cli": "flext_meltano._protocols.cli",
    "plugin": "flext_meltano._protocols.plugin",
    "project": "flext_meltano._protocols.project",
    "services": "flext_meltano._protocols.services",
    "singer": "flext_meltano._protocols.singer",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
