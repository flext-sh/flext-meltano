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
    from flext_meltano import config, project, runtime, singer, yaml
    from flext_meltano.config import FlextMeltanoUtilitiesConfig
    from flext_meltano.project import FlextMeltanoUtilitiesProject
    from flext_meltano.runtime import FlextMeltanoUtilitiesRuntime
    from flext_meltano.singer import FlextMeltanoUtilitiesSinger, SingerTargetHandler
    from flext_meltano.yaml import FlextMeltanoUtilitiesYaml

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextMeltanoUtilitiesConfig": "flext_meltano.config",
    "FlextMeltanoUtilitiesProject": "flext_meltano.project",
    "FlextMeltanoUtilitiesRuntime": "flext_meltano.runtime",
    "FlextMeltanoUtilitiesSinger": "flext_meltano.singer",
    "FlextMeltanoUtilitiesYaml": "flext_meltano.yaml",
    "SingerTargetHandler": "flext_meltano.singer",
    "config": "flext_meltano.config",
    "project": "flext_meltano.project",
    "runtime": "flext_meltano.runtime",
    "singer": "flext_meltano.singer",
    "yaml": "flext_meltano.yaml",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
