# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano utilities submodules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._utilities import (
        config as config,
        project as project,
        singer as singer,
        yaml as yaml,
    )
    from flext_meltano._utilities.config import (
        FlextMeltanoUtilitiesConfig as FlextMeltanoUtilitiesConfig,
    )
    from flext_meltano._utilities.project import (
        FlextMeltanoUtilitiesProject as FlextMeltanoUtilitiesProject,
    )
    from flext_meltano._utilities.singer import (
        FlextMeltanoUtilitiesSinger as FlextMeltanoUtilitiesSinger,
        SingerTargetHandler as SingerTargetHandler,
    )
    from flext_meltano._utilities.yaml import (
        FlextMeltanoUtilitiesYaml as FlextMeltanoUtilitiesYaml,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoUtilitiesConfig": [
        "flext_meltano._utilities.config",
        "FlextMeltanoUtilitiesConfig",
    ],
    "FlextMeltanoUtilitiesProject": [
        "flext_meltano._utilities.project",
        "FlextMeltanoUtilitiesProject",
    ],
    "FlextMeltanoUtilitiesSinger": [
        "flext_meltano._utilities.singer",
        "FlextMeltanoUtilitiesSinger",
    ],
    "FlextMeltanoUtilitiesYaml": [
        "flext_meltano._utilities.yaml",
        "FlextMeltanoUtilitiesYaml",
    ],
    "SingerTargetHandler": ["flext_meltano._utilities.singer", "SingerTargetHandler"],
    "config": ["flext_meltano._utilities.config", ""],
    "project": ["flext_meltano._utilities.project", ""],
    "singer": ["flext_meltano._utilities.singer", ""],
    "yaml": ["flext_meltano._utilities.yaml", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextMeltanoUtilitiesConfig",
    "FlextMeltanoUtilitiesProject",
    "FlextMeltanoUtilitiesSinger",
    "FlextMeltanoUtilitiesYaml",
    "SingerTargetHandler",
    "config",
    "project",
    "singer",
    "yaml",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
