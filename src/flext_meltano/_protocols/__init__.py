# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Protocols package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .cli import FlextMeltanoProtocolsBase as FlextMeltanoProtocolsBase
    from .plugin import FlextMeltanoProtocolsPlugin as FlextMeltanoProtocolsPlugin
    from .project import FlextMeltanoProtocolsProject as FlextMeltanoProtocolsProject
    from .services import FlextMeltanoProtocolsServices as FlextMeltanoProtocolsServices
    from .singer import FlextMeltanoProtocolsSinger as FlextMeltanoProtocolsSinger

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".cli": ("FlextMeltanoProtocolsBase",),
    ".plugin": ("FlextMeltanoProtocolsPlugin",),
    ".project": ("FlextMeltanoProtocolsProject",),
    ".services": ("FlextMeltanoProtocolsServices",),
    ".singer": ("FlextMeltanoProtocolsSinger",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextMeltanoProtocolsBase",
    "FlextMeltanoProtocolsPlugin",
    "FlextMeltanoProtocolsProject",
    "FlextMeltanoProtocolsServices",
    "FlextMeltanoProtocolsSinger",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
