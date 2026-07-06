# AUTO-GENERATED FILE — Regenerate with: make gen
"""Services package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if TYPE_CHECKING:
    from flext_meltano.services.abstractions import FlextMeltanoAbstractions
    from flext_meltano.services.abstractions_base import FlextMeltanoAbstractionsBase
    from flext_meltano.services.adapters import FlextMeltanoAdapter
    from flext_meltano.services.bridge import FlextMeltanoBridge
    from flext_meltano.services.consumer_bases.dbt_service_base import (
        FlextMeltanoDbtServiceBase,
    )
    from flext_meltano.services.consumer_bases.tap_service_base import (
        FlextMeltanoTapServiceBase,
    )
    from flext_meltano.services.consumer_bases.target_service_base import (
        FlextMeltanoTargetServiceBase,
    )
    from flext_meltano.services.dbt_project import FlextMeltanoDbtProjectMixin
    from flext_meltano.services.dbt_runner import FlextMeltanoDbtRunnerMixin
    from flext_meltano.services.executor import FlextMeltanoExecutor
    from flext_meltano.services.executor_base import FlextMeltanoExecutorBase
    from flext_meltano.services.library_runner import FlextMeltanoLibraryRunner
    from flext_meltano.services.meltano_plugin_discovery import (
        FlextMeltanoPluginDiscoveryMixin,
    )
    from flext_meltano.services.meltano_plugins import FlextMeltanoComponentService
    from flext_meltano.services.meltano_project_sdk import FlextMeltanoProjectManager
    from flext_meltano.services.project_service import FlextMeltanoProjectService
    from flext_meltano.services.services import FlextMeltanoService
    from flext_meltano.services.singer_catalog import FlextMeltanoSingerCatalogMixin
    from flext_meltano.services.singer_sdk import (
        FlextMeltanoSingerTapAdapter,
        Sink,
        Stream,
        Tap,
        Target,
    )
    from flext_meltano.services.singer_state import FlextMeltanoSingerStateMixin
    from flext_meltano.services.singer_tap import (
        FlextMeltanoTapAbstractions,
        FlextMeltanoTapSourceMixin,
    )
    from flext_meltano.services.singer_target import FlextMeltanoTargetAbstractions
    from flext_meltano.services.singer_translator import FlextMeltanoSingerCliTranslator
    from flext_meltano.services.validators import FlextMeltanoValidators
_LAZY_IMPORTS = merge_lazy_imports(
    (".consumer_bases",),
    build_lazy_import_map(
        {
            ".abstractions": ("FlextMeltanoAbstractions",),
            ".abstractions_base": ("FlextMeltanoAbstractionsBase",),
            ".adapters": ("FlextMeltanoAdapter",),
            ".bridge": ("FlextMeltanoBridge",),
            ".consumer_bases": ("consumer_bases",),
            ".consumer_bases.dbt_service_base": ("FlextMeltanoDbtServiceBase",),
            ".consumer_bases.tap_service_base": ("FlextMeltanoTapServiceBase",),
            ".consumer_bases.target_service_base": ("FlextMeltanoTargetServiceBase",),
            ".dbt_project": ("FlextMeltanoDbtProjectMixin",),
            ".dbt_runner": ("FlextMeltanoDbtRunnerMixin",),
            ".executor": ("FlextMeltanoExecutor",),
            ".executor_base": ("FlextMeltanoExecutorBase",),
            ".library_runner": ("FlextMeltanoLibraryRunner",),
            ".meltano_plugin_discovery": ("FlextMeltanoPluginDiscoveryMixin",),
            ".meltano_plugins": ("FlextMeltanoComponentService",),
            ".meltano_project_sdk": ("FlextMeltanoProjectManager",),
            ".project_service": ("FlextMeltanoProjectService",),
            ".services": ("FlextMeltanoService",),
            ".singer_catalog": ("FlextMeltanoSingerCatalogMixin",),
            ".singer_sdk": (
                "FlextMeltanoSingerTapAdapter",
                "Sink",
                "Stream",
                "Tap",
                "Target",
            ),
            ".singer_state": ("FlextMeltanoSingerStateMixin",),
            ".singer_tap": (
                "FlextMeltanoTapAbstractions",
                "FlextMeltanoTapSourceMixin",
            ),
            ".singer_target": ("FlextMeltanoTargetAbstractions",),
            ".singer_translator": ("FlextMeltanoSingerCliTranslator",),
            ".validators": ("FlextMeltanoValidators",),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
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


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
