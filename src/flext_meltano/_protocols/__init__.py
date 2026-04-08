# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Protocols package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextMeltanoProtocolsBase": (
        "flext_meltano._protocols.cli",
        "FlextMeltanoProtocolsBase",
    ),
    "FlextMeltanoProtocolsPlugin": (
        "flext_meltano._protocols.plugin",
        "FlextMeltanoProtocolsPlugin",
    ),
    "FlextMeltanoProtocolsProject": (
        "flext_meltano._protocols.project",
        "FlextMeltanoProtocolsProject",
    ),
    "FlextMeltanoProtocolsServices": (
        "flext_meltano._protocols.services",
        "FlextMeltanoProtocolsServices",
    ),
    "FlextMeltanoProtocolsSinger": (
        "flext_meltano._protocols.singer",
        "FlextMeltanoProtocolsSinger",
    ),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
