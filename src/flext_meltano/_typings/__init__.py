# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Typings package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
