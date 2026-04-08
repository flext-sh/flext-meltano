# AUTO-GENERATED FILE — Regenerate with: make gen
"""Services package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

_LAZY_IMPORTS = merge_lazy_imports(
    (".consumer_bases",),
    {
        "Context": ".singer_sdk",
        "FlextMeltanoAbstractions": ".abstractions",
        "FlextMeltanoAdapter": ".adapters",
        "FlextMeltanoBridge": ".bridge",
        "FlextMeltanoCommandRouter": ".cli_managers",
        "FlextMeltanoComponentService": ".meltano_plugins",
        "FlextMeltanoDbtAdapter": ".adapter_extensions",
        "FlextMeltanoDbtManager": ".cli_managers",
        "FlextMeltanoDbtProjectMixin": ".dbt_project",
        "FlextMeltanoDbtRunnerMixin": ".dbt_runner",
        "FlextMeltanoDbtTransformationRunner": ".meltano_dbt_transformation",
        "FlextMeltanoExecutor": ".executor",
        "FlextMeltanoLibraryRunner": ".library_runner",
        "FlextMeltanoPipelineAdapter": ".adapter_extensions",
        "FlextMeltanoPipelineManager": ".cli_managers",
        "FlextMeltanoPluginDiscoveryMixin": ".meltano_plugin_discovery",
        "FlextMeltanoPluginManager": ".cli_managers",
        "FlextMeltanoProjectManager": ".meltano_project_sdk",
        "FlextMeltanoProjectService": ".project_service",
        "FlextMeltanoService": ".services",
        "FlextMeltanoSingerCatalogMixin": ".singer_catalog",
        "FlextMeltanoSingerCliTranslator": ".singer_translator",
        "FlextMeltanoSingerManager": ".cli_managers",
        "FlextMeltanoSingerStateMixin": ".singer_state",
        "FlextMeltanoSingerTapAdapter": ".singer_sdk",
        "FlextMeltanoStatusManager": ".cli_managers",
        "FlextMeltanoTapAbstractions": ".singer_tap",
        "FlextMeltanoTapSourceMixin": ".singer_tap",
        "FlextMeltanoTargetAbstractions": ".singer_target",
        "FlextMeltanoValidators": ".validators",
        "Record": ".singer_sdk",
        "Sink": ".singer_sdk",
        "Stream": ".singer_sdk",
        "Tap": ".singer_sdk",
        "Target": ".singer_sdk",
    },
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
