# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano protocols submodules."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_meltano._protocols import cli, plugin, project, services, singer
    from flext_meltano._protocols.cli import FlextMeltanoProtocolsBase
    from flext_meltano._protocols.plugin import FlextMeltanoProtocolsPlugin
    from flext_meltano._protocols.project import FlextMeltanoProtocolsProject
    from flext_meltano._protocols.services import FlextMeltanoProtocolsServices
    from flext_meltano._protocols.singer import FlextMeltanoProtocolsSinger

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoProtocolsBase": [
        "flext_meltano._protocols.cli",
        "FlextMeltanoProtocolsBase",
    ],
    "FlextMeltanoProtocolsPlugin": [
        "flext_meltano._protocols.plugin",
        "FlextMeltanoProtocolsPlugin",
    ],
    "FlextMeltanoProtocolsProject": [
        "flext_meltano._protocols.project",
        "FlextMeltanoProtocolsProject",
    ],
    "FlextMeltanoProtocolsServices": [
        "flext_meltano._protocols.services",
        "FlextMeltanoProtocolsServices",
    ],
    "FlextMeltanoProtocolsSinger": [
        "flext_meltano._protocols.singer",
        "FlextMeltanoProtocolsSinger",
    ],
    "cli": ["flext_meltano._protocols.cli", ""],
    "plugin": ["flext_meltano._protocols.plugin", ""],
    "project": ["flext_meltano._protocols.project", ""],
    "services": ["flext_meltano._protocols.services", ""],
    "singer": ["flext_meltano._protocols.singer", ""],
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


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
