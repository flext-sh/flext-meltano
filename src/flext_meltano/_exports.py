# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export registry."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, merge_lazy_imports

_LOCAL_LAZY_IMPORTS = build_lazy_import_map(
    {
        "._constants": ("_constants",),
        "._models": ("_models",),
        "._protocols": ("_protocols",),
        "._typings": ("_typings",),
        "._utilities": ("_utilities",),
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
        ".services": ("services",),
        ".services.abstractions": ("FlextMeltanoAbstractions",),
        ".services.abstractions_base": ("FlextMeltanoAbstractionsBase",),
        ".services.adapters": ("FlextMeltanoAdapter",),
        ".services.bridge": ("FlextMeltanoBridge",),
        ".services.consumer_bases.dbt_service_base": ("FlextMeltanoDbtServiceBase",),
        ".services.consumer_bases.tap_service_base": ("FlextMeltanoTapServiceBase",),
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
        ".settings": ("FlextMeltanoSettings",),
        ".typings": (
            "FlextMeltanoTypes",
            "t",
        ),
        ".utilities": (
            "FlextMeltanoUtilities",
            "u",
        ),
        "flext_core._root_typing_parts.facades": (
            "d",
            "e",
            "h",
            "r",
            "x",
        ),
    },
)

FLEXT_MELTANO_LAZY_IMPORTS = merge_lazy_imports(
    (".services",),
    _LOCAL_LAZY_IMPORTS,
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
    module_name="flext_meltano",
)

__all__: list[str] = ["FLEXT_MELTANO_LAZY_IMPORTS"]
