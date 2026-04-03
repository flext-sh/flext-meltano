# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Protocols package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_meltano._protocols.cli as _flext_meltano__protocols_cli

    cli = _flext_meltano__protocols_cli
    import flext_meltano._protocols.plugin as _flext_meltano__protocols_plugin

    plugin = _flext_meltano__protocols_plugin
    import flext_meltano._protocols.project as _flext_meltano__protocols_project

    project = _flext_meltano__protocols_project
    import flext_meltano._protocols.services as _flext_meltano__protocols_services

    services = _flext_meltano__protocols_services
    import flext_meltano._protocols.singer as _flext_meltano__protocols_singer

    singer = _flext_meltano__protocols_singer

    _ = (
        FlextMeltanoProtocolsBase,
        FlextMeltanoProtocolsPlugin,
        FlextMeltanoProtocolsProject,
        FlextMeltanoProtocolsServices,
        FlextMeltanoProtocolsSinger,
        cli,
        plugin,
        project,
        services,
        singer,
    )
_LAZY_IMPORTS = {
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

__all__ = [
    "FlextMeltanoProtocolsBase",
    "FlextMeltanoProtocolsPlugin",
    "FlextMeltanoProtocolsProject",
    "FlextMeltanoProtocolsServices",
    "FlextMeltanoProtocolsSinger",
    "cli",
    "plugin",
    "project",
    "services",
    "singer",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
