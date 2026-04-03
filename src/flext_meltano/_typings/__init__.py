# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Typings package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_meltano._typings import base, domains, singer
    from flext_meltano._typings.base import FlextMeltanoTypingsBase
    from flext_meltano._typings.domains import FlextMeltanoTypingsDomains
    from flext_meltano._typings.singer import FlextMeltanoTypingsSinger

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextMeltanoTypingsBase": "flext_meltano._typings.base",
    "FlextMeltanoTypingsDomains": "flext_meltano._typings.domains",
    "FlextMeltanoTypingsSinger": "flext_meltano._typings.singer",
    "base": "flext_meltano._typings.base",
    "domains": "flext_meltano._typings.domains",
    "singer": "flext_meltano._typings.singer",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
