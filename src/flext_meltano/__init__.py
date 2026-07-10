# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
from flext_meltano.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import d as d, e as e, h as h, r as r, x as x
    from flext_meltano.api import FlextMeltano as FlextMeltano, meltano as meltano
    from flext_meltano.base import (
        FlextMeltanoServiceBase as FlextMeltanoServiceBase,
        s as s,
    )
    from flext_meltano.cli import FlextMeltanoCli as FlextMeltanoCli, main as main
    from flext_meltano.constants import (
        FlextMeltanoConstants as FlextMeltanoConstants,
        c as c,
    )
    from flext_meltano.models import FlextMeltanoModels as FlextMeltanoModels, m as m
    from flext_meltano.protocols import (
        FlextMeltanoProtocols as FlextMeltanoProtocols,
        p as p,
    )
    from flext_meltano.services.abstractions import (
        FlextMeltanoAbstractions as FlextMeltanoAbstractions,
    )
    from flext_meltano.services.abstractions_base import (
        FlextMeltanoAbstractionsBase as FlextMeltanoAbstractionsBase,
    )
    from flext_meltano.services.adapters import (
        FlextMeltanoAdapter as FlextMeltanoAdapter,
    )
    from flext_meltano.services.bridge import FlextMeltanoBridge as FlextMeltanoBridge
    from flext_meltano.services.consumer_bases.dbt_service_base import (
        FlextMeltanoDbtServiceBase as FlextMeltanoDbtServiceBase,
    )
    from flext_meltano.services.consumer_bases.tap_service_base import (
        FlextMeltanoTapServiceBase as FlextMeltanoTapServiceBase,
    )
    from flext_meltano.services.consumer_bases.target_service_base import (
        FlextMeltanoTargetServiceBase as FlextMeltanoTargetServiceBase,
    )
    from flext_meltano.services.dbt_project import (
        FlextMeltanoDbtProjectMixin as FlextMeltanoDbtProjectMixin,
    )
    from flext_meltano.services.dbt_runner import (
        FlextMeltanoDbtRunnerMixin as FlextMeltanoDbtRunnerMixin,
    )
    from flext_meltano.services.executor import (
        FlextMeltanoExecutor as FlextMeltanoExecutor,
    )
    from flext_meltano.services.executor_base import (
        FlextMeltanoExecutorBase as FlextMeltanoExecutorBase,
    )
    from flext_meltano.services.library_runner import (
        FlextMeltanoLibraryRunner as FlextMeltanoLibraryRunner,
    )
    from flext_meltano.services.meltano_plugin_discovery import (
        FlextMeltanoPluginDiscoveryMixin as FlextMeltanoPluginDiscoveryMixin,
    )
    from flext_meltano.services.meltano_plugins import (
        FlextMeltanoComponentService as FlextMeltanoComponentService,
    )
    from flext_meltano.services.meltano_project_sdk import (
        FlextMeltanoProjectManager as FlextMeltanoProjectManager,
    )
    from flext_meltano.services.project_service import (
        FlextMeltanoProjectService as FlextMeltanoProjectService,
    )
    from flext_meltano.services.services import (
        FlextMeltanoService as FlextMeltanoService,
    )
    from flext_meltano.services.singer_catalog import (
        FlextMeltanoSingerCatalogMixin as FlextMeltanoSingerCatalogMixin,
    )
    from flext_meltano.services.singer_sdk import (
        FlextMeltanoSingerTapAdapter as FlextMeltanoSingerTapAdapter,
        Sink as Sink,
        Stream as Stream,
        Tap as Tap,
        Target as Target,
    )
    from flext_meltano.services.singer_state import (
        FlextMeltanoSingerStateMixin as FlextMeltanoSingerStateMixin,
    )
    from flext_meltano.services.singer_tap import (
        FlextMeltanoTapAbstractions as FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin as FlextMeltanoTapSourceMixin,
    )
    from flext_meltano.services.singer_target import (
        FlextMeltanoTargetAbstractions as FlextMeltanoTargetAbstractions,
    )
    from flext_meltano.services.singer_translator import (
        FlextMeltanoSingerCliTranslator as FlextMeltanoSingerCliTranslator,
    )
    from flext_meltano.services.validators import (
        FlextMeltanoValidators as FlextMeltanoValidators,
    )
    from flext_meltano.typings import FlextMeltanoTypes as FlextMeltanoTypes, t as t
    from flext_meltano.utilities import (
        FlextMeltanoUtilities as FlextMeltanoUtilities,
        u as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (".services",),
    build_lazy_import_map(
        {
            "._settings": ("FlextMeltanoSettings", "settings"),
            ".api": (
                "FlextMeltano",
                "meltano",
            ),
            ".base": (
                "FlextMeltanoServiceBase",
                "s",
            ),
            ".cli": (
                "FlextMeltanoCli",
                "main",
            ),
            ".constants": (
                "FlextMeltanoConstants",
                "c",
            ),
            ".models": (
                "FlextMeltanoModels",
                "m",
            ),
            ".protocols": (
                "FlextMeltanoProtocols",
                "p",
            ),
            ".services.abstractions": ("FlextMeltanoAbstractions",),
            ".services.abstractions_base": ("FlextMeltanoAbstractionsBase",),
            ".services.adapters": ("FlextMeltanoAdapter",),
            ".services.bridge": ("FlextMeltanoBridge",),
            ".services.consumer_bases.dbt_service_base": (
                "FlextMeltanoDbtServiceBase",
            ),
            ".services.consumer_bases.tap_service_base": (
                "FlextMeltanoTapServiceBase",
            ),
            ".services.consumer_bases.target_service_base": (
                "FlextMeltanoTargetServiceBase",
            ),
            ".services.dbt_project": ("FlextMeltanoDbtProjectMixin",),
            ".services.dbt_runner": ("FlextMeltanoDbtRunnerMixin",),
            ".services.executor": ("FlextMeltanoExecutor",),
            ".services.executor_base": ("FlextMeltanoExecutorBase",),
            ".services.library_runner": ("FlextMeltanoLibraryRunner",),
            ".services.meltano_plugin_discovery": ("FlextMeltanoPluginDiscoveryMixin",),
            ".services.meltano_plugins": ("FlextMeltanoComponentService",),
            ".services.meltano_project_sdk": ("FlextMeltanoProjectManager",),
            ".services.project_service": ("FlextMeltanoProjectService",),
            ".services.services": ("FlextMeltanoService",),
            ".services.singer_catalog": ("FlextMeltanoSingerCatalogMixin",),
            ".services.singer_sdk": (
                "FlextMeltanoSingerTapAdapter",
                "Sink",
                "Stream",
                "Tap",
                "Target",
            ),
            ".services.singer_state": ("FlextMeltanoSingerStateMixin",),
            ".services.singer_tap": (
                "FlextMeltanoTapAbstractions",
                "FlextMeltanoTapSourceMixin",
            ),
            ".services.singer_target": ("FlextMeltanoTargetAbstractions",),
            ".services.singer_translator": ("FlextMeltanoSingerCliTranslator",),
            ".services.validators": ("FlextMeltanoValidators",),
            ".typings": (
                "FlextMeltanoTypes",
                "t",
            ),
            ".utilities": (
                "FlextMeltanoUtilities",
                "u",
            ),
            "flext_cli": (
                "d",
                "e",
                "h",
                "r",
                "x",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "consumer_bases",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


__all__: tuple[str, ...] = (
    "FlextMeltanoSettings",
    "settings",
    "FlextMeltano",
    "FlextMeltanoAbstractions",
    "FlextMeltanoAbstractionsBase",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCli",
    "FlextMeltanoComponentService",
    "FlextMeltanoConstants",
    "FlextMeltanoDbtProjectMixin",
    "FlextMeltanoDbtRunnerMixin",
    "FlextMeltanoDbtServiceBase",
    "FlextMeltanoExecutor",
    "FlextMeltanoExecutorBase",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoModels",
    "FlextMeltanoPluginDiscoveryMixin",
    "FlextMeltanoProjectManager",
    "FlextMeltanoProjectService",
    "FlextMeltanoProtocols",
    "FlextMeltanoService",
    "FlextMeltanoServiceBase",
    "FlextMeltanoSingerCatalogMixin",
    "FlextMeltanoSingerCliTranslator",
    "FlextMeltanoSingerStateMixin",
    "FlextMeltanoSingerTapAdapter",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTapServiceBase",
    "FlextMeltanoTapSourceMixin",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTargetServiceBase",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
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
    "c",
    "d",
    "e",
    "h",
    "m",
    "main",
    "meltano",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
