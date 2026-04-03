# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_meltano._utilities import config, project, runtime, singer, yaml
    from flext_meltano._utilities.config import FlextMeltanoUtilitiesConfig
    from flext_meltano._utilities.project import FlextMeltanoUtilitiesProject
    from flext_meltano._utilities.runtime import FlextMeltanoUtilitiesRuntime
    from flext_meltano._utilities.singer import (
        FlextMeltanoUtilitiesSinger,
        SingerTargetHandler,
    )
    from flext_meltano._utilities.yaml import FlextMeltanoUtilitiesYaml

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextMeltanoUtilitiesConfig": "flext_meltano._utilities.config",
    "FlextMeltanoUtilitiesProject": "flext_meltano._utilities.project",
    "FlextMeltanoUtilitiesRuntime": "flext_meltano._utilities.runtime",
    "FlextMeltanoUtilitiesSinger": "flext_meltano._utilities.singer",
    "FlextMeltanoUtilitiesYaml": "flext_meltano._utilities.yaml",
    "SingerTargetHandler": "flext_meltano._utilities.singer",
    "config": "flext_meltano._utilities.config",
    "project": "flext_meltano._utilities.project",
    "runtime": "flext_meltano._utilities.runtime",
    "singer": "flext_meltano._utilities.singer",
    "yaml": "flext_meltano._utilities.yaml",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
