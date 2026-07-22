# AUTO-GENERATED FILE — Regenerate with: make gen
"""Protocols package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
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
_LAZY_IMPORTS = build_lazy_import_map({
    ".cli": ("FlextMeltanoProtocolsBase",),
    ".plugin": ("FlextMeltanoProtocolsPlugin",),
    ".project": ("FlextMeltanoProtocolsProject",),
    ".services": ("FlextMeltanoProtocolsServices",),
    ".singer": ("FlextMeltanoProtocolsSinger",),
})


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
