"""ELT pipeline integration library for FLEXT.

Provides programmatic APIs for singer-sdk, meltano-sdk, and dbt-core integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_core import (
        FlextDecorators as d,
        FlextExceptions as e,
        FlextHandlers as h,
        r,
        s,
        x,
    )

    from flext_meltano.__version__ import __version__, __version_info__
    from flext_meltano.adapters import FlextMeltanoAdapter
    from flext_meltano.api import FlextMeltano
    from flext_meltano.bridge import FlextMeltanoBridge
    from flext_meltano.cli_managers import (
        FlextMeltanoPluginManager,
        FlextMeltanoSingerManager,
        FlextMeltanoStatusManager,
        _ManagerProtocol,
        _SingerManagerProtocol,
        _StatusManagerProtocol,
    )
    from flext_meltano.constants import (
        FlextMeltanoConstants,
        FlextMeltanoConstants as c,
    )
    from flext_meltano.dbt import (
        FlextMeltanoDbtProjectManager,
        FlextMeltanoDbtRunner,
        FlextMeltanoDbtService,
    )
    from flext_meltano.executor import FlextMeltanoExecutor
    from flext_meltano.file_managers import FlextMeltanoFileManagers
    from flext_meltano.library_runner import FlextMeltanoLibraryRunner
    from flext_meltano.meltano import (
        FlextMeltanoMeltanoService,
        FlextMeltanoProjectManager,
    )
    from flext_meltano.models import FlextMeltanoModels, FlextMeltanoModels as m
    from flext_meltano.protocols import (
        FlextMeltanoProtocols,
        FlextMeltanoProtocols as p,
    )
    from flext_meltano.services import FlextMeltanoService
    from flext_meltano.settings import FlextMeltanoSettings
    from flext_meltano.singer.catalog import FlextMeltanoCatalogManager
    from flext_meltano.singer.service import FlextMeltanoSingerService
    from flext_meltano.singer.state import FlextMeltanoStateManager
    from flext_meltano.singer.tap import (
        FlextMeltanoStream,
        FlextMeltanoTap,
        FlextMeltanoTapAbstractions,
    )
    from flext_meltano.singer.target import (
        FlextMeltanoTarget,
        FlextMeltanoTargetAbstractions,
    )
    from flext_meltano.typings import FlextMeltanoTypes, FlextMeltanoTypes as t
    from flext_meltano.utilities import (
        FlextMeltanoUtilities,
        FlextMeltanoUtilities as u,
    )
    from flext_meltano.validators import FlextMeltanoValidators
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextMeltano": ("flext_meltano.api", "FlextMeltano"),
    "FlextMeltanoAdapter": ("flext_meltano.adapters", "FlextMeltanoAdapter"),
    "FlextMeltanoBridge": ("flext_meltano.bridge", "FlextMeltanoBridge"),
    "FlextMeltanoCatalogManager": (
        "flext_meltano.singer.catalog",
        "FlextMeltanoCatalogManager",
    ),
    "FlextMeltanoConstants": ("flext_meltano.constants", "FlextMeltanoConstants"),
    "FlextMeltanoDbtProjectManager": (
        "flext_meltano.dbt",
        "FlextMeltanoDbtProjectManager",
    ),
    "FlextMeltanoDbtRunner": ("flext_meltano.dbt", "FlextMeltanoDbtRunner"),
    "FlextMeltanoDbtService": ("flext_meltano.dbt", "FlextMeltanoDbtService"),
    "FlextMeltanoExecutor": ("flext_meltano.executor", "FlextMeltanoExecutor"),
    "FlextMeltanoFileManagers": (
        "flext_meltano.file_managers",
        "FlextMeltanoFileManagers",
    ),
    "FlextMeltanoLibraryRunner": (
        "flext_meltano.library_runner",
        "FlextMeltanoLibraryRunner",
    ),
    "FlextMeltanoMeltanoService": (
        "flext_meltano.meltano",
        "FlextMeltanoMeltanoService",
    ),
    "FlextMeltanoModels": ("flext_meltano.models", "FlextMeltanoModels"),
    "FlextMeltanoPluginManager": (
        "flext_meltano.cli_managers",
        "FlextMeltanoPluginManager",
    ),
    "FlextMeltanoProjectManager": (
        "flext_meltano.meltano",
        "FlextMeltanoProjectManager",
    ),
    "FlextMeltanoProtocols": ("flext_meltano.protocols", "FlextMeltanoProtocols"),
    "FlextMeltanoService": ("flext_meltano.services", "FlextMeltanoService"),
    "FlextMeltanoSettings": ("flext_meltano.settings", "FlextMeltanoSettings"),
    "FlextMeltanoSingerManager": (
        "flext_meltano.cli_managers",
        "FlextMeltanoSingerManager",
    ),
    "FlextMeltanoSingerService": (
        "flext_meltano.singer.service",
        "FlextMeltanoSingerService",
    ),
    "FlextMeltanoStateManager": (
        "flext_meltano.singer.state",
        "FlextMeltanoStateManager",
    ),
    "FlextMeltanoStatusManager": (
        "flext_meltano.cli_managers",
        "FlextMeltanoStatusManager",
    ),
    "FlextMeltanoStream": ("flext_meltano.singer.tap", "FlextMeltanoStream"),
    "FlextMeltanoTap": ("flext_meltano.singer.tap", "FlextMeltanoTap"),
    "FlextMeltanoTapAbstractions": (
        "flext_meltano.singer.tap",
        "FlextMeltanoTapAbstractions",
    ),
    "FlextMeltanoTarget": ("flext_meltano.singer.target", "FlextMeltanoTarget"),
    "FlextMeltanoTargetAbstractions": (
        "flext_meltano.singer.target",
        "FlextMeltanoTargetAbstractions",
    ),
    "FlextMeltanoTypes": ("flext_meltano.typings", "FlextMeltanoTypes"),
    "FlextMeltanoUtilities": ("flext_meltano.utilities", "FlextMeltanoUtilities"),
    "FlextMeltanoValidators": ("flext_meltano.validators", "FlextMeltanoValidators"),
    "_ManagerProtocol": ("flext_meltano.cli_managers", "_ManagerProtocol"),
    "_SingerManagerProtocol": ("flext_meltano.cli_managers", "_SingerManagerProtocol"),
    "_StatusManagerProtocol": ("flext_meltano.cli_managers", "_StatusManagerProtocol"),
    "__version__": ("flext_meltano.__version__", "__version__"),
    "__version_info__": ("flext_meltano.__version__", "__version_info__"),
    "c": ("flext_meltano.constants", "FlextMeltanoConstants"),
    "d": ("flext_core", "FlextDecorators"),
    "e": ("flext_core", "FlextExceptions"),
    "h": ("flext_core", "FlextHandlers"),
    "m": ("flext_meltano.models", "FlextMeltanoModels"),
    "p": ("flext_meltano.protocols", "FlextMeltanoProtocols"),
    "r": ("flext_core", "r"),
    "s": ("flext_core", "s"),
    "t": ("flext_meltano.typings", "FlextMeltanoTypes"),
    "u": ("flext_meltano.utilities", "FlextMeltanoUtilities"),
    "x": ("flext_core", "x"),
}
__all__ = [
    "FlextMeltano",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCatalogManager",
    "FlextMeltanoConstants",
    "FlextMeltanoDbtProjectManager",
    "FlextMeltanoDbtRunner",
    "FlextMeltanoDbtService",
    "FlextMeltanoExecutor",
    "FlextMeltanoFileManagers",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoMeltanoService",
    "FlextMeltanoModels",
    "FlextMeltanoPluginManager",
    "FlextMeltanoProjectManager",
    "FlextMeltanoProtocols",
    "FlextMeltanoService",
    "FlextMeltanoSettings",
    "FlextMeltanoSingerManager",
    "FlextMeltanoSingerService",
    "FlextMeltanoStateManager",
    "FlextMeltanoStatusManager",
    "FlextMeltanoStream",
    "FlextMeltanoTap",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTarget",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "_ManagerProtocol",
    "_SingerManagerProtocol",
    "_StatusManagerProtocol",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
