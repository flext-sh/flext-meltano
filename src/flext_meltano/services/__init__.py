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
            ".abstractions_base": ("FlextMeltanoAbstractionsBase",),
            ".adapter_extensions": (
                "FlextMeltanoDbtAdapter",
                "FlextMeltanoPipelineAdapter",
            ),
            ".adapters": ("FlextMeltanoAdapter",),
            ".bridge": ("FlextMeltanoBridge",),
            ".cli_managers": (
                "FlextMeltanoCommandRouter",
                "FlextMeltanoSingerManager",
            ),
            ".cli_small_managers": (
                "FlextMeltanoDbtManager",
                "FlextMeltanoPluginManager",
                "FlextMeltanoStatusManager",
            ),
            ".consumer_bases.dbt_service_base": ("FlextMeltanoDbtServiceBase",),
            ".consumer_bases.tap_service_base": ("FlextMeltanoTapServiceBase",),
            ".consumer_bases.target_service_base": ("FlextMeltanoTargetServiceBase",),
            ".dbt_project": ("FlextMeltanoDbtProjectMixin",),
            ".dbt_runner": ("FlextMeltanoDbtRunnerMixin",),
            ".executor": ("FlextMeltanoExecutor",),
            ".executor_base": ("FlextMeltanoExecutorBase",),
            ".library_runner": ("FlextMeltanoLibraryRunner",),
            ".meltano_dbt_transformation": ("FlextMeltanoDbtTransformationRunner",),
            ".meltano_plugin_discovery": ("FlextMeltanoPluginDiscoveryMixin",),
            ".meltano_plugins": ("FlextMeltanoComponentService",),
            ".meltano_project_sdk": ("FlextMeltanoProjectManager",),
            ".pipeline_lifecycle": ("FlextMeltanoPipelineLifecycleOperations",),
            ".pipeline_mgr": ("FlextMeltanoPipelineManager",),
            ".pipeline_ops": (
                "FlextMeltanoPipelineCrudOperations",
                "FlextMeltanoPipelinePaths",
            ),
            ".project_service": ("FlextMeltanoProjectService",),
            ".services": ("FlextMeltanoService",),
            ".singer_catalog": ("FlextMeltanoSingerCatalogMixin",),
            ".singer_sdk": (
                "Context",
                "FlextMeltanoSingerTapAdapter",
                "Record",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
