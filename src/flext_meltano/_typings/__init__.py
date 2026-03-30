# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano typings submodules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._typings import (
        base as base,
        domains as domains,
        singer as singer,
    )
    from flext_meltano._typings.base import (
        FlextMeltanoTypingsBase as FlextMeltanoTypingsBase,
    )
    from flext_meltano._typings.domains import (
        FlextMeltanoTypingsDomains as FlextMeltanoTypingsDomains,
    )
    from flext_meltano._typings.singer import (
        FlextMeltanoTypingsSinger as FlextMeltanoTypingsSinger,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoTypingsBase": [
        "flext_meltano._typings.base",
        "FlextMeltanoTypingsBase",
    ],
    "FlextMeltanoTypingsDomains": [
        "flext_meltano._typings.domains",
        "FlextMeltanoTypingsDomains",
    ],
    "FlextMeltanoTypingsSinger": [
        "flext_meltano._typings.singer",
        "FlextMeltanoTypingsSinger",
    ],
    "base": ["flext_meltano._typings.base", ""],
    "domains": ["flext_meltano._typings.domains", ""],
    "singer": ["flext_meltano._typings.singer", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextMeltanoTypingsBase",
    "FlextMeltanoTypingsDomains",
    "FlextMeltanoTypingsSinger",
    "base",
    "domains",
    "singer",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
