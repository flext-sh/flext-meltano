# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano constants submodules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._constants import base as base, config as config, enums as enums
    from flext_meltano._constants.base import (
        FlextMeltanoConstantsBase as FlextMeltanoConstantsBase,
    )
    from flext_meltano._constants.config import (
        FlextMeltanoConstantsConfig as FlextMeltanoConstantsConfig,
    )
    from flext_meltano._constants.enums import (
        FlextMeltanoConstantsEnums as FlextMeltanoConstantsEnums,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoConstantsBase": [
        "flext_meltano._constants.base",
        "FlextMeltanoConstantsBase",
    ],
    "FlextMeltanoConstantsConfig": [
        "flext_meltano._constants.config",
        "FlextMeltanoConstantsConfig",
    ],
    "FlextMeltanoConstantsEnums": [
        "flext_meltano._constants.enums",
        "FlextMeltanoConstantsEnums",
    ],
    "base": ["flext_meltano._constants.base", ""],
    "config": ["flext_meltano._constants.config", ""],
    "enums": ["flext_meltano._constants.enums", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextMeltanoConstantsBase",
    "FlextMeltanoConstantsConfig",
    "FlextMeltanoConstantsEnums",
    "base",
    "config",
    "enums",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
