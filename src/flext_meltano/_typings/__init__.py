# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano typings submodules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_meltano._typings.base import *
    from flext_meltano._typings.domains import *
    from flext_meltano._typings.singer import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextMeltanoTypingsBase": "flext_meltano._typings.base",
    "FlextMeltanoTypingsDomains": "flext_meltano._typings.domains",
    "FlextMeltanoTypingsSinger": "flext_meltano._typings.singer",
    "base": "flext_meltano._typings.base",
    "domains": "flext_meltano._typings.domains",
    "singer": "flext_meltano._typings.singer",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
