# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Typings package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .base import FlextMeltanoTypingsBase as FlextMeltanoTypingsBase
    from .domains import FlextMeltanoTypingsDomains as FlextMeltanoTypingsDomains
    from .singer import FlextMeltanoTypingsSinger as FlextMeltanoTypingsSinger

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".base": ("FlextMeltanoTypingsBase",),
    ".domains": ("FlextMeltanoTypingsDomains",),
    ".singer": ("FlextMeltanoTypingsSinger",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextMeltanoTypingsBase",
    "FlextMeltanoTypingsDomains",
    "FlextMeltanoTypingsSinger",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
