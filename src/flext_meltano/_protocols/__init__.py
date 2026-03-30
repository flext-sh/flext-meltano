# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano protocols submodules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._protocols import (
        cli as cli,
        plugin as plugin,
        project as project,
        services as services,
        singer as singer,
    )
    from flext_meltano._protocols.cli import (
        FlextMeltanoProtocolsBase as FlextMeltanoProtocolsBase,
    )
    from flext_meltano._protocols.plugin import (
        FlextMeltanoProtocolsPlugin as FlextMeltanoProtocolsPlugin,
    )
    from flext_meltano._protocols.project import (
        FlextMeltanoProtocolsProject as FlextMeltanoProtocolsProject,
    )
    from flext_meltano._protocols.services import (
        FlextMeltanoProtocolsServices as FlextMeltanoProtocolsServices,
    )
    from flext_meltano._protocols.singer import (
        FlextMeltanoProtocolsSinger as FlextMeltanoProtocolsSinger,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoProtocolsBase": [
        "flext_meltano._protocols.cli",
        "FlextMeltanoProtocolsBase",
    ],
    "FlextMeltanoProtocolsPlugin": [
        "flext_meltano._protocols.plugin",
        "FlextMeltanoProtocolsPlugin",
    ],
    "FlextMeltanoProtocolsProject": [
        "flext_meltano._protocols.project",
        "FlextMeltanoProtocolsProject",
    ],
    "FlextMeltanoProtocolsServices": [
        "flext_meltano._protocols.services",
        "FlextMeltanoProtocolsServices",
    ],
    "FlextMeltanoProtocolsSinger": [
        "flext_meltano._protocols.singer",
        "FlextMeltanoProtocolsSinger",
    ],
    "cli": ["flext_meltano._protocols.cli", ""],
    "plugin": ["flext_meltano._protocols.plugin", ""],
    "project": ["flext_meltano._protocols.project", ""],
    "services": ["flext_meltano._protocols.services", ""],
    "singer": ["flext_meltano._protocols.singer", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextMeltanoProtocolsBase",
    "FlextMeltanoProtocolsPlugin",
    "FlextMeltanoProtocolsProject",
    "FlextMeltanoProtocolsServices",
    "FlextMeltanoProtocolsSinger",
    "cli",
    "plugin",
    "project",
    "services",
    "singer",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
