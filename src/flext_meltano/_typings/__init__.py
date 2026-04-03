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
    from flext_meltano import base, domains, singer
    from flext_meltano.base import FlextMeltanoTypingsBase
    from flext_meltano.domains import FlextMeltanoTypingsDomains
    from flext_meltano.singer import FlextMeltanoTypingsSinger

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextMeltanoTypingsBase": "flext_meltano.base",
    "FlextMeltanoTypingsDomains": "flext_meltano.domains",
    "FlextMeltanoTypingsSinger": "flext_meltano.singer",
    "base": "flext_meltano.base",
    "domains": "flext_meltano.domains",
    "singer": "flext_meltano.singer",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
