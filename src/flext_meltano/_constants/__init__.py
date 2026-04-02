# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano constants submodules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_meltano._constants import base, config, enums
    from flext_meltano._constants.base import FlextMeltanoConstantsBase
    from flext_meltano._constants.config import FlextMeltanoConstantsConfig
    from flext_meltano._constants.enums import FlextMeltanoConstantsEnums

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextMeltanoConstantsBase": "flext_meltano._constants.base",
    "FlextMeltanoConstantsConfig": "flext_meltano._constants.config",
    "FlextMeltanoConstantsEnums": "flext_meltano._constants.enums",
    "base": "flext_meltano._constants.base",
    "config": "flext_meltano._constants.config",
    "enums": "flext_meltano._constants.enums",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
