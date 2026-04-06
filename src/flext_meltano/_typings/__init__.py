# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Typings package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_meltano._typings.base as _flext_meltano__typings_base

    base = _flext_meltano__typings_base
    import flext_meltano._typings.domains as _flext_meltano__typings_domains
    from flext_meltano._typings.base import FlextMeltanoTypingsBase

    domains = _flext_meltano__typings_domains
    import flext_meltano._typings.singer as _flext_meltano__typings_singer
    from flext_meltano._typings.domains import FlextMeltanoTypingsDomains

    singer = _flext_meltano__typings_singer
    from flext_meltano._typings.singer import FlextMeltanoTypingsSinger
_LAZY_IMPORTS = {
    "FlextMeltanoTypingsBase": (
        "flext_meltano._typings.base",
        "FlextMeltanoTypingsBase",
    ),
    "FlextMeltanoTypingsDomains": (
        "flext_meltano._typings.domains",
        "FlextMeltanoTypingsDomains",
    ),
    "FlextMeltanoTypingsSinger": (
        "flext_meltano._typings.singer",
        "FlextMeltanoTypingsSinger",
    ),
    "base": "flext_meltano._typings.base",
    "domains": "flext_meltano._typings.domains",
    "singer": "flext_meltano._typings.singer",
}

__all__ = [
    "FlextMeltanoTypingsBase",
    "FlextMeltanoTypingsDomains",
    "FlextMeltanoTypingsSinger",
    "base",
    "domains",
    "singer",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
