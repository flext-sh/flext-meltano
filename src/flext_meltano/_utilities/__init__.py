# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_meltano._utilities.config as _flext_meltano__utilities_config

    config = _flext_meltano__utilities_config
    import flext_meltano._utilities.project as _flext_meltano__utilities_project
    from flext_meltano._utilities.config import FlextMeltanoUtilitiesConfig

    project = _flext_meltano__utilities_project
    import flext_meltano._utilities.runtime as _flext_meltano__utilities_runtime
    from flext_meltano._utilities.project import FlextMeltanoUtilitiesProject

    runtime = _flext_meltano__utilities_runtime
    import flext_meltano._utilities.singer as _flext_meltano__utilities_singer
    from flext_meltano._utilities.runtime import FlextMeltanoUtilitiesRuntime

    singer = _flext_meltano__utilities_singer
    from flext_meltano._utilities.singer import (
        FlextMeltanoUtilitiesSinger,
        SingerTargetHandler,
    )
_LAZY_IMPORTS = {
    "FlextMeltanoUtilitiesConfig": "flext_meltano._utilities.config",
    "FlextMeltanoUtilitiesProject": "flext_meltano._utilities.project",
    "FlextMeltanoUtilitiesRuntime": "flext_meltano._utilities.runtime",
    "FlextMeltanoUtilitiesSinger": "flext_meltano._utilities.singer",
    "SingerTargetHandler": "flext_meltano._utilities.singer",
    "config": "flext_meltano._utilities.config",
    "project": "flext_meltano._utilities.project",
    "runtime": "flext_meltano._utilities.runtime",
    "singer": "flext_meltano._utilities.singer",
}

__all__ = [
    "FlextMeltanoUtilitiesConfig",
    "FlextMeltanoUtilitiesProject",
    "FlextMeltanoUtilitiesRuntime",
    "FlextMeltanoUtilitiesSinger",
    "SingerTargetHandler",
    "config",
    "project",
    "runtime",
    "singer",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
