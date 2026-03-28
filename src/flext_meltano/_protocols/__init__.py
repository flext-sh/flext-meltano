"""FLEXT Meltano protocols submodules."""

from __future__ import annotations

from flext_meltano._protocols.plugin import FlextMeltanoProtocolsPlugin
from flext_meltano._protocols.project import FlextMeltanoProtocolsProject
from flext_meltano._protocols.services import FlextMeltanoProtocolsServices
from flext_meltano._protocols.singer import FlextMeltanoProtocolsSinger

__all__ = [
    "FlextMeltanoProtocolsPlugin",
    "FlextMeltanoProtocolsProject",
    "FlextMeltanoProtocolsServices",
    "FlextMeltanoProtocolsSinger",
]
