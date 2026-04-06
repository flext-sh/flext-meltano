# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_meltano._utilities.runtime as _flext_meltano__utilities_runtime

    runtime = _flext_meltano__utilities_runtime
    import flext_meltano._utilities.singer as _flext_meltano__utilities_singer
    from flext_meltano._utilities.runtime import FlextMeltanoUtilitiesRuntime

    singer = _flext_meltano__utilities_singer
    from flext_meltano._utilities.singer import FlextMeltanoUtilitiesSinger
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

__all__ = [
    "FlextMeltanoUtilitiesRuntime",
    "FlextMeltanoUtilitiesSinger",
    "runtime",
    "singer",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
