# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_MELTANO_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        ".api": ("FlextMeltano",),
        ".base": ("FlextMeltanoServiceBase",),
        ".cli": ("FlextMeltanoCli",),
        ".constants": ("FlextMeltanoConstants",),
        ".models": ("FlextMeltanoModels",),
        ".protocols": ("FlextMeltanoProtocols",),
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
        ".services.singer_sdk": ("FlextMeltanoSingerTapAdapter",),
        ".services.singer_state": ("FlextMeltanoSingerStateMixin",),
        ".services.singer_tap": (
            "FlextMeltanoTapAbstractions",
            "FlextMeltanoTapSourceMixin",
        ),
        ".services.singer_target": ("FlextMeltanoTargetAbstractions",),
        ".services.singer_translator": ("FlextMeltanoSingerCliTranslator",),
        ".settings": ("FlextMeltanoSettings",),
        ".typings": ("FlextMeltanoTypes",),
    },
)

__all__: list[str] = ["FLEXT_MELTANO_LAZY_IMPORTS_PART_01"]
