# AUTO-GENERATED FILE — Regenerate with: make gen
"""Typings package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._typings.base import FlextMeltanoTypingsBase
    from flext_meltano._typings.domains import FlextMeltanoTypingsDomains
    from flext_meltano._typings.singer import FlextMeltanoTypingsSinger
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".base": ("FlextMeltanoTypingsBase",),
        ".domains": ("FlextMeltanoTypingsDomains",),
        ".singer": ("FlextMeltanoTypingsSinger",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
