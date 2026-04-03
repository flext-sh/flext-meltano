# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Constants package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_meltano import base, config, enums
    from flext_meltano.base import FlextMeltanoConstantsBase
    from flext_meltano.config import FlextMeltanoConstantsConfig
    from flext_meltano.enums import FlextMeltanoConstantsEnums

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextMeltanoConstantsBase": "flext_meltano.base",
    "FlextMeltanoConstantsConfig": "flext_meltano.config",
    "FlextMeltanoConstantsEnums": "flext_meltano.enums",
    "base": "flext_meltano.base",
    "config": "flext_meltano.config",
    "enums": "flext_meltano.enums",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
