# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Flext meltano package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_cli import d, e, h, r, s, x
    from flext_core import FlextTypes

    from flext_meltano import dbt, meltano, singer
    from flext_meltano.__version__ import (
        __all__,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_meltano.abstractions import FlextMeltanoAbstractions
    from flext_meltano.adapters import FlextMeltanoAdapter
    from flext_meltano.api import FlextMeltano
    from flext_meltano.bridge import FlextMeltanoBridge
    from flext_meltano.cli import FlextMeltanoCLI, main
    from flext_meltano.cli_managers import (
        FlextMeltanoCommandRouter,
        FlextMeltanoDbtManager,
        FlextMeltanoPipelineManager,
        FlextMeltanoPluginManager,
        FlextMeltanoSingerManager,
        FlextMeltanoStatusManager,
    )
    from flext_meltano.constants import (
        FlextMeltanoConstants,
        FlextMeltanoConstants as c,
    )
    from flext_meltano.dbt.project import FlextMeltanoDbtProjectManager
    from flext_meltano.dbt.runner import FlextMeltanoDbtRunner
    from flext_meltano.dbt.service import FlextMeltanoDbtService
    from flext_meltano.executor import FlextMeltanoExecutor
    from flext_meltano.file_managers import FlextMeltanoFileManagers
    from flext_meltano.library_runner import FlextMeltanoLibraryRunner
    from flext_meltano.meltano.pipelines import FlextMeltanoOrchestrationService
    from flext_meltano.meltano.plugins import FlextMeltanoComponentService
    from flext_meltano.meltano.project import FlextMeltanoProjectManager
    from flext_meltano.meltano.runner import FlextMeltanoDbtTransformationRunner
    from flext_meltano.meltano.service import FlextMeltanoMeltanoService
    from flext_meltano.models import FlextMeltanoModels, FlextMeltanoModels as m
    from flext_meltano.project_service import FlextMeltanoProjectService
    from flext_meltano.protocols import (
        FlextMeltanoProtocols,
        FlextMeltanoProtocols as p,
    )
    from flext_meltano.services import FlextMeltanoService
    from flext_meltano.settings import FlextMeltanoSettings
    from flext_meltano.singer.catalog import FlextMeltanoCatalogManager
    from flext_meltano.singer.service import FlextMeltanoSingerService
    from flext_meltano.singer.state import FlextMeltanoStateManager
    from flext_meltano.singer.tap import FlextMeltanoTapAbstractions
    from flext_meltano.singer.target import FlextMeltanoTargetAbstractions
    from flext_meltano.singer.translator import FlextMeltanoSingerCliTranslator
    from flext_meltano.typings import FlextMeltanoTypes, FlextMeltanoTypes as t
    from flext_meltano.utilities import (
        FlextMeltanoUtilities,
        FlextMeltanoUtilities as u,
    )
    from flext_meltano.validators import FlextMeltanoValidators

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltano": ["flext_meltano.api", "FlextMeltano"],
    "FlextMeltanoAbstractions": ["flext_meltano.abstractions", "FlextMeltanoAbstractions"],
    "FlextMeltanoAdapter": ["flext_meltano.adapters", "FlextMeltanoAdapter"],
    "FlextMeltanoBridge": ["flext_meltano.bridge", "FlextMeltanoBridge"],
    "FlextMeltanoCLI": ["flext_meltano.cli", "FlextMeltanoCLI"],
    "FlextMeltanoCatalogManager": ["flext_meltano.singer.catalog", "FlextMeltanoCatalogManager"],
    "FlextMeltanoCommandRouter": ["flext_meltano.cli_managers", "FlextMeltanoCommandRouter"],
    "FlextMeltanoComponentService": ["flext_meltano.meltano.plugins", "FlextMeltanoComponentService"],
    "FlextMeltanoConstants": ["flext_meltano.constants", "FlextMeltanoConstants"],
    "FlextMeltanoDbtManager": ["flext_meltano.cli_managers", "FlextMeltanoDbtManager"],
    "FlextMeltanoDbtProjectManager": ["flext_meltano.dbt.project", "FlextMeltanoDbtProjectManager"],
    "FlextMeltanoDbtRunner": ["flext_meltano.dbt.runner", "FlextMeltanoDbtRunner"],
    "FlextMeltanoDbtService": ["flext_meltano.dbt.service", "FlextMeltanoDbtService"],
    "FlextMeltanoDbtTransformationRunner": ["flext_meltano.meltano.runner", "FlextMeltanoDbtTransformationRunner"],
    "FlextMeltanoExecutor": ["flext_meltano.executor", "FlextMeltanoExecutor"],
    "FlextMeltanoFileManagers": ["flext_meltano.file_managers", "FlextMeltanoFileManagers"],
    "FlextMeltanoLibraryRunner": ["flext_meltano.library_runner", "FlextMeltanoLibraryRunner"],
    "FlextMeltanoMeltanoService": ["flext_meltano.meltano.service", "FlextMeltanoMeltanoService"],
    "FlextMeltanoModels": ["flext_meltano.models", "FlextMeltanoModels"],
    "FlextMeltanoOrchestrationService": ["flext_meltano.meltano.pipelines", "FlextMeltanoOrchestrationService"],
    "FlextMeltanoPipelineManager": ["flext_meltano.cli_managers", "FlextMeltanoPipelineManager"],
    "FlextMeltanoPluginManager": ["flext_meltano.cli_managers", "FlextMeltanoPluginManager"],
    "FlextMeltanoProjectManager": ["flext_meltano.meltano.project", "FlextMeltanoProjectManager"],
    "FlextMeltanoProjectService": ["flext_meltano.project_service", "FlextMeltanoProjectService"],
    "FlextMeltanoProtocols": ["flext_meltano.protocols", "FlextMeltanoProtocols"],
    "FlextMeltanoService": ["flext_meltano.services", "FlextMeltanoService"],
    "FlextMeltanoSettings": ["flext_meltano.settings", "FlextMeltanoSettings"],
    "FlextMeltanoSingerCliTranslator": ["flext_meltano.singer.translator", "FlextMeltanoSingerCliTranslator"],
    "FlextMeltanoSingerManager": ["flext_meltano.cli_managers", "FlextMeltanoSingerManager"],
    "FlextMeltanoSingerService": ["flext_meltano.singer.service", "FlextMeltanoSingerService"],
    "FlextMeltanoStateManager": ["flext_meltano.singer.state", "FlextMeltanoStateManager"],
    "FlextMeltanoStatusManager": ["flext_meltano.cli_managers", "FlextMeltanoStatusManager"],
    "FlextMeltanoTapAbstractions": ["flext_meltano.singer.tap", "FlextMeltanoTapAbstractions"],
    "FlextMeltanoTargetAbstractions": ["flext_meltano.singer.target", "FlextMeltanoTargetAbstractions"],
    "FlextMeltanoTypes": ["flext_meltano.typings", "FlextMeltanoTypes"],
    "FlextMeltanoUtilities": ["flext_meltano.utilities", "FlextMeltanoUtilities"],
    "FlextMeltanoValidators": ["flext_meltano.validators", "FlextMeltanoValidators"],
    "__all__": ["flext_meltano.__version__", "__all__"],
    "__author__": ["flext_meltano.__version__", "__author__"],
    "__author_email__": ["flext_meltano.__version__", "__author_email__"],
    "__description__": ["flext_meltano.__version__", "__description__"],
    "__license__": ["flext_meltano.__version__", "__license__"],
    "__title__": ["flext_meltano.__version__", "__title__"],
    "__url__": ["flext_meltano.__version__", "__url__"],
    "__version__": ["flext_meltano.__version__", "__version__"],
    "__version_info__": ["flext_meltano.__version__", "__version_info__"],
    "c": ["flext_meltano.constants", "FlextMeltanoConstants"],
    "d": ["flext_cli", "d"],
    "dbt": ["flext_meltano.dbt", ""],
    "e": ["flext_cli", "e"],
    "h": ["flext_cli", "h"],
    "m": ["flext_meltano.models", "FlextMeltanoModels"],
    "main": ["flext_meltano.cli", "main"],
    "meltano": ["flext_meltano.meltano", ""],
    "p": ["flext_meltano.protocols", "FlextMeltanoProtocols"],
    "r": ["flext_cli", "r"],
    "s": ["flext_cli", "s"],
    "singer": ["flext_meltano.singer", ""],
    "t": ["flext_meltano.typings", "FlextMeltanoTypes"],
    "u": ["flext_meltano.utilities", "FlextMeltanoUtilities"],
    "x": ["flext_cli", "x"],
}

__all__ = [
    "FlextMeltano",
    "FlextMeltanoAbstractions",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCLI",
    "FlextMeltanoCatalogManager",
    "FlextMeltanoCommandRouter",
    "FlextMeltanoComponentService",
    "FlextMeltanoConstants",
    "FlextMeltanoDbtManager",
    "FlextMeltanoDbtProjectManager",
    "FlextMeltanoDbtRunner",
    "FlextMeltanoDbtService",
    "FlextMeltanoDbtTransformationRunner",
    "FlextMeltanoExecutor",
    "FlextMeltanoFileManagers",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoMeltanoService",
    "FlextMeltanoModels",
    "FlextMeltanoOrchestrationService",
    "FlextMeltanoPipelineManager",
    "FlextMeltanoPluginManager",
    "FlextMeltanoProjectManager",
    "FlextMeltanoProjectService",
    "FlextMeltanoProtocols",
    "FlextMeltanoService",
    "FlextMeltanoSettings",
    "FlextMeltanoSingerCliTranslator",
    "FlextMeltanoSingerManager",
    "FlextMeltanoSingerService",
    "FlextMeltanoStateManager",
    "FlextMeltanoStatusManager",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "__all__",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "dbt",
    "e",
    "h",
    "m",
    "main",
    "meltano",
    "p",
    "r",
    "s",
    "singer",
    "t",
    "u",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
