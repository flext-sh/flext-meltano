# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Protocols package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .cli import FlextMeltanoProtocolsBase
    from .plugin import FlextMeltanoProtocolsPlugin
    from .project import FlextMeltanoProtocolsProject
    from .services import FlextMeltanoProtocolsServices
    from .singer import FlextMeltanoProtocolsSinger
__all__: tuple[str, ...] = (
    "FlextMeltanoProtocolsBase",
    "FlextMeltanoProtocolsPlugin",
    "FlextMeltanoProtocolsProject",
    "FlextMeltanoProtocolsServices",
    "FlextMeltanoProtocolsSinger",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".cli": ("FlextMeltanoProtocolsBase",),
            ".plugin": ("FlextMeltanoProtocolsPlugin",),
            ".project": ("FlextMeltanoProtocolsProject",),
            ".services": ("FlextMeltanoProtocolsServices",),
            ".singer": ("FlextMeltanoProtocolsSinger",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
