# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano utilities submodules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_meltano._utilities.config import *
    from flext_meltano._utilities.project import *
    from flext_meltano._utilities.singer import *
    from flext_meltano._utilities.yaml import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextMeltanoUtilitiesConfig": "flext_meltano._utilities.config",
    "FlextMeltanoUtilitiesProject": "flext_meltano._utilities.project",
    "FlextMeltanoUtilitiesSinger": "flext_meltano._utilities.singer",
    "FlextMeltanoUtilitiesYaml": "flext_meltano._utilities.yaml",
    "SingerTargetHandler": "flext_meltano._utilities.singer",
    "config": "flext_meltano._utilities.config",
    "project": "flext_meltano._utilities.project",
    "singer": "flext_meltano._utilities.singer",
    "yaml": "flext_meltano._utilities.yaml",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
