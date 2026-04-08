# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextMeltanoUtilitiesRuntime": (
        "flext_meltano._utilities.runtime",
        "FlextMeltanoUtilitiesRuntime",
    ),
    "FlextMeltanoUtilitiesSinger": (
        "flext_meltano._utilities.singer",
        "FlextMeltanoUtilitiesSinger",
    ),
    "runtime": "flext_meltano._utilities.runtime",
    "singer": "flext_meltano._utilities.singer",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
