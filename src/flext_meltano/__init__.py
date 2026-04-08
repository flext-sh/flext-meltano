# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext meltano package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_meltano.__version__ import *

if _t.TYPE_CHECKING:
    import flext_meltano._constants as _flext_meltano__constants

    _constants = _flext_meltano__constants
    import flext_meltano._models as _flext_meltano__models
    from flext_meltano._constants import (
        FlextMeltanoConstantsBase,
        FlextMeltanoConstantsConfig,
        FlextMeltanoConstantsEnums,
    )

    _models = _flext_meltano__models
    import flext_meltano._protocols as _flext_meltano__protocols
    from flext_meltano._models import (
        FlextMeltanoModelsCliParams,
        FlextMeltanoModelsContext,
        FlextMeltanoModelsCore,
        FlextMeltanoModelsDiscovery,
        FlextMeltanoModelsInstances,
        FlextMeltanoModelsInstancesData,
        FlextMeltanoModelsLogging,
        FlextMeltanoModelsPayloads,
        FlextMeltanoModelsPayloadsData,
        FlextMeltanoModelsProjects,
        FlextMeltanoModelsProjectsPlugin,
        FlextMeltanoModelsResults,
        FlextMeltanoModelsResultsDbt,
        FlextMeltanoModelsResultsPipeline,
        FlextMeltanoModelsSinger,
        FlextMeltanoModelsSingerCatalog,
        FlextMeltanoModelsSingerSdk,
        FlextMeltanoModelsSources,
        FlextMeltanoModelsSourcesParams,
        FlextMeltanoModelsTransformations,
    )

    _protocols = _flext_meltano__protocols
    import flext_meltano._typings as _flext_meltano__typings
    from flext_meltano._protocols import (
        FlextMeltanoProtocolsBase,
        FlextMeltanoProtocolsPlugin,
        FlextMeltanoProtocolsProject,
        FlextMeltanoProtocolsServices,
        FlextMeltanoProtocolsSinger,
    )

    _typings = _flext_meltano__typings
    import flext_meltano._utilities as _flext_meltano__utilities
    from flext_meltano._typings import (
        FlextMeltanoTypingsBase,
        FlextMeltanoTypingsDomains,
        FlextMeltanoTypingsSinger,
    )

    _utilities = _flext_meltano__utilities
    import flext_meltano.api as _flext_meltano_api
    from flext_meltano._utilities import (
        FlextMeltanoUtilitiesRuntime,
        FlextMeltanoUtilitiesSinger,
    )

    api = _flext_meltano_api
    import flext_meltano.base as _flext_meltano_base
    from flext_meltano.api import FlextMeltano, meltano

    base = _flext_meltano_base
    import flext_meltano.cli as _flext_meltano_cli
    from flext_meltano.base import FlextMeltanoServiceBase, FlextMeltanoServiceBase as s

    cli = _flext_meltano_cli
    import flext_meltano.constants as _flext_meltano_constants
    from flext_meltano.cli import FlextMeltanoCLI

    constants = _flext_meltano_constants
    import flext_meltano.models as _flext_meltano_models
    from flext_meltano.constants import (
        FlextMeltanoConstants,
        FlextMeltanoConstants as c,
    )

    models = _flext_meltano_models
    import flext_meltano.protocols as _flext_meltano_protocols
    from flext_meltano.models import FlextMeltanoModels, FlextMeltanoModels as m

    protocols = _flext_meltano_protocols
    import flext_meltano.services as _flext_meltano_services
    from flext_meltano.protocols import (
        FlextMeltanoProtocols,
        FlextMeltanoProtocols as p,
    )

    services = _flext_meltano_services
    import flext_meltano.settings as _flext_meltano_settings
    from flext_meltano.services import (
        Context,
        FlextMeltanoAbstractions,
        FlextMeltanoAdapter,
        FlextMeltanoBridge,
        FlextMeltanoCommandRouter,
        FlextMeltanoComponentService,
        FlextMeltanoDbtAdapter,
        FlextMeltanoDbtManager,
        FlextMeltanoDbtProjectMixin,
        FlextMeltanoDbtRunnerMixin,
        FlextMeltanoDbtTransformationRunner,
        FlextMeltanoExecutor,
        FlextMeltanoLibraryRunner,
        FlextMeltanoPipelineAdapter,
        FlextMeltanoPipelineManager,
        FlextMeltanoPluginDiscoveryMixin,
        FlextMeltanoPluginManager,
        FlextMeltanoProjectManager,
        FlextMeltanoProjectService,
        FlextMeltanoService,
        FlextMeltanoSingerCatalogMixin,
        FlextMeltanoSingerCliTranslator,
        FlextMeltanoSingerManager,
        FlextMeltanoSingerStateMixin,
        FlextMeltanoSingerTapAdapter,
        FlextMeltanoStatusManager,
        FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin,
        FlextMeltanoTargetAbstractions,
        FlextMeltanoValidators,
        Record,
        Sink,
        Stream,
        Tap,
        Target,
    )
    from flext_meltano.services.consumer_bases import (
        FlextMeltanoDbtServiceBase,
        FlextMeltanoTapServiceBase,
        FlextMeltanoTargetServiceBase,
    )

    settings = _flext_meltano_settings
    import flext_meltano.typings as _flext_meltano_typings
    from flext_meltano.settings import FlextMeltanoSettings

    typings = _flext_meltano_typings
    import flext_meltano.utilities as _flext_meltano_utilities
    from flext_meltano.typings import FlextMeltanoTypes, FlextMeltanoTypes as t

    utilities = _flext_meltano_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_meltano.utilities import (
        FlextMeltanoUtilities,
        FlextMeltanoUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_meltano._constants",
        "flext_meltano._models",
        "flext_meltano._protocols",
        "flext_meltano._typings",
        "flext_meltano._utilities",
        "flext_meltano.services",
    ),
    {
        "FlextMeltano": ("flext_meltano.api", "FlextMeltano"),
        "FlextMeltanoCLI": ("flext_meltano.cli", "FlextMeltanoCLI"),
        "FlextMeltanoConstants": ("flext_meltano.constants", "FlextMeltanoConstants"),
        "FlextMeltanoModels": ("flext_meltano.models", "FlextMeltanoModels"),
        "FlextMeltanoProtocols": ("flext_meltano.protocols", "FlextMeltanoProtocols"),
        "FlextMeltanoServiceBase": ("flext_meltano.base", "FlextMeltanoServiceBase"),
        "FlextMeltanoSettings": ("flext_meltano.settings", "FlextMeltanoSettings"),
        "FlextMeltanoTypes": ("flext_meltano.typings", "FlextMeltanoTypes"),
        "FlextMeltanoUtilities": ("flext_meltano.utilities", "FlextMeltanoUtilities"),
        "__author__": ("flext_meltano.__version__", "__author__"),
        "__author_email__": ("flext_meltano.__version__", "__author_email__"),
        "__description__": ("flext_meltano.__version__", "__description__"),
        "__license__": ("flext_meltano.__version__", "__license__"),
        "__title__": ("flext_meltano.__version__", "__title__"),
        "__url__": ("flext_meltano.__version__", "__url__"),
        "__version__": ("flext_meltano.__version__", "__version__"),
        "__version_info__": ("flext_meltano.__version__", "__version_info__"),
        "_constants": "flext_meltano._constants",
        "_models": "flext_meltano._models",
        "_protocols": "flext_meltano._protocols",
        "_typings": "flext_meltano._typings",
        "_utilities": "flext_meltano._utilities",
        "api": "flext_meltano.api",
        "base": "flext_meltano.base",
        "c": ("flext_meltano.constants", "FlextMeltanoConstants"),
        "cli": "flext_meltano.cli",
        "constants": "flext_meltano.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_meltano.models", "FlextMeltanoModels"),
        "meltano": ("flext_meltano.api", "meltano"),
        "models": "flext_meltano.models",
        "p": ("flext_meltano.protocols", "FlextMeltanoProtocols"),
        "protocols": "flext_meltano.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_meltano.base", "FlextMeltanoServiceBase"),
        "services": "flext_meltano.services",
        "settings": "flext_meltano.settings",
        "t": ("flext_meltano.typings", "FlextMeltanoTypes"),
        "typings": "flext_meltano.typings",
        "u": ("flext_meltano.utilities", "FlextMeltanoUtilities"),
        "utilities": "flext_meltano.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("logger", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "Context",
    "FlextMeltano",
    "FlextMeltanoAbstractions",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCLI",
    "FlextMeltanoCommandRouter",
    "FlextMeltanoComponentService",
    "FlextMeltanoConstants",
    "FlextMeltanoConstantsBase",
    "FlextMeltanoConstantsConfig",
    "FlextMeltanoConstantsEnums",
    "FlextMeltanoDbtAdapter",
    "FlextMeltanoDbtManager",
    "FlextMeltanoDbtProjectMixin",
    "FlextMeltanoDbtRunnerMixin",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoDbtTransformationRunner",
    "FlextMeltanoExecutor",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoModels",
    "FlextMeltanoModelsCliParams",
    "FlextMeltanoModelsContext",
    "FlextMeltanoModelsCore",
    "FlextMeltanoModelsDiscovery",
    "FlextMeltanoModelsInstances",
    "FlextMeltanoModelsInstancesData",
    "FlextMeltanoModelsLogging",
    "FlextMeltanoModelsPayloads",
    "FlextMeltanoModelsPayloadsData",
    "FlextMeltanoModelsProjects",
    "FlextMeltanoModelsProjectsPlugin",
    "FlextMeltanoModelsResults",
    "FlextMeltanoModelsResultsDbt",
    "FlextMeltanoModelsResultsPipeline",
    "FlextMeltanoModelsSinger",
    "FlextMeltanoModelsSingerCatalog",
    "FlextMeltanoModelsSingerSdk",
    "FlextMeltanoModelsSources",
    "FlextMeltanoModelsSourcesParams",
    "FlextMeltanoModelsTransformations",
    "FlextMeltanoPipelineAdapter",
    "FlextMeltanoPipelineManager",
    "FlextMeltanoPluginDiscoveryMixin",
    "FlextMeltanoPluginManager",
    "FlextMeltanoProjectManager",
    "FlextMeltanoProjectService",
    "FlextMeltanoProtocols",
    "FlextMeltanoProtocolsBase",
    "FlextMeltanoProtocolsPlugin",
    "FlextMeltanoProtocolsProject",
    "FlextMeltanoProtocolsServices",
    "FlextMeltanoProtocolsSinger",
    "FlextMeltanoService",
    "FlextMeltanoServiceBase",
    "FlextMeltanoSettings",
    "FlextMeltanoSingerCatalogMixin",
    "FlextMeltanoSingerCliTranslator",
    "FlextMeltanoSingerManager",
    "FlextMeltanoSingerStateMixin",
    "FlextMeltanoSingerTapAdapter",
    "FlextMeltanoStatusManager",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTapSourceMixin",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTargetServiceBase",
    "FlextMeltanoTypes",
    "FlextMeltanoTypingsBase",
    "FlextMeltanoTypingsDomains",
    "FlextMeltanoTypingsSinger",
    "FlextMeltanoUtilities",
    "FlextMeltanoUtilitiesRuntime",
    "FlextMeltanoUtilitiesSinger",
    "FlextMeltanoValidators",
    "Record",
    "Sink",
    "Stream",
    "Tap",
    "Target",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "_constants",
    "_models",
    "_protocols",
    "_typings",
    "_utilities",
    "api",
    "base",
    "c",
    "cli",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "meltano",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
