# AUTO-GENERATED FILE — Regenerate with: make gen
"""Constants package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._constants.base import (
        FlextMeltanoConstantsBase as FlextMeltanoConstantsBase,
    )
    from flext_meltano._constants.enums import (
        FlextMeltanoConstantsEnums as FlextMeltanoConstantsEnums,
    )
    from flext_meltano._constants.settings import (
        FlextMeltanoConstantsSettings as FlextMeltanoConstantsSettings,
    )
_LAZY_IMPORTS = build_lazy_import_map({
    ".base": ("FlextMeltanoConstantsBase",),
    ".enums": ("FlextMeltanoConstantsEnums",),
    ".settings": ("FlextMeltanoConstantsSettings",),
})


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
