# AUTO-GENERATED FILE — Regenerate with: make gen
"""Services package."""

from __future__ import annotations

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

_LAZY_IMPORTS = merge_lazy_imports(
    (".consumer_bases",),
    build_lazy_import_map(
        {
            ".abstractions": ("FlextMeltanoAbstractions",),
            ".adapter_extensions": (
                "FlextMeltanoDbtAdapter",
                "FlextMeltanoPipelineAdapter",
            ),
            ".adapters": ("FlextMeltanoAdapter",),
            ".bridge": ("FlextMeltanoBridge",),
            ".cli_managers": (
                "FlextMeltanoCommandRouter",
                "FlextMeltanoDbtManager",
                "FlextMeltanoPipelineManager",
                "FlextMeltanoPluginManager",
                "FlextMeltanoSingerManager",
                "FlextMeltanoStatusManager",
            ),
            ".dbt_project": ("FlextMeltanoDbtProjectMixin",),
            ".dbt_runner": ("FlextMeltanoDbtRunnerMixin",),
            ".executor": ("FlextMeltanoExecutor",),
            ".library_runner": ("FlextMeltanoLibraryRunner",),
            ".meltano_dbt_transformation": ("FlextMeltanoDbtTransformationRunner",),
            ".meltano_plugin_discovery": ("FlextMeltanoPluginDiscoveryMixin",),
            ".meltano_plugins": ("FlextMeltanoComponentService",),
            ".meltano_project_sdk": ("FlextMeltanoProjectManager",),
            ".project_service": ("FlextMeltanoProjectService",),
            ".services": ("FlextMeltanoService",),
            ".singer_catalog": ("FlextMeltanoSingerCatalogMixin",),
            ".singer_sdk": ("FlextMeltanoSingerTapAdapter",),
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
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
