# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Constants package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_meltano._constants.base as _flext_meltano__constants_base

    base = _flext_meltano__constants_base
    import flext_meltano._constants.config as _flext_meltano__constants_config
    from flext_meltano._constants.base import FlextMeltanoConstantsBase

    config = _flext_meltano__constants_config
    import flext_meltano._constants.enums as _flext_meltano__constants_enums
    from flext_meltano._constants.config import FlextMeltanoConstantsConfig

    enums = _flext_meltano__constants_enums
    from flext_meltano._constants.enums import FlextMeltanoConstantsEnums
_LAZY_IMPORTS = {
    "FlextMeltanoConstantsBase": (
        "flext_meltano._constants.base",
        "FlextMeltanoConstantsBase",
    ),
    "FlextMeltanoConstantsConfig": (
        "flext_meltano._constants.config",
        "FlextMeltanoConstantsConfig",
    ),
    "FlextMeltanoConstantsEnums": (
        "flext_meltano._constants.enums",
        "FlextMeltanoConstantsEnums",
    ),
    "base": "flext_meltano._constants.base",
    "config": "flext_meltano._constants.config",
    "enums": "flext_meltano._constants.enums",
}

__all__ = [
    "FlextMeltanoConstantsBase",
    "FlextMeltanoConstantsConfig",
    "FlextMeltanoConstantsEnums",
    "base",
    "config",
    "enums",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
