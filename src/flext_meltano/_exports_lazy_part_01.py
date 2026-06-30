# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_MELTANO_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
    {
        "._constants.base": ("FlextMeltanoConstantsBase",),
        "._constants.enums": ("FlextMeltanoConstantsEnums",),
        "._constants.settings": ("FlextMeltanoConstantsSettings",),
        "._models.cli_params": ("FlextMeltanoModelsCliParams",),
        "._models.context": ("FlextMeltanoModelsContext",),
        "._models.core": ("FlextMeltanoModelsCore",),
        "._models.discovery": ("FlextMeltanoModelsDiscovery",),
        "._models.instances": ("FlextMeltanoModelsInstances",),
        "._models.instances_data": ("FlextMeltanoModelsInstancesData",),
        "._models.logging_config": ("FlextMeltanoModelsLogging",),
        "._models.payloads_data": ("FlextMeltanoModelsPayloadsData",),
        "._models.projects": ("FlextMeltanoModelsProjects",),
        "._models.results": ("FlextMeltanoModelsResults",),
        "._models.results_dbt": ("FlextMeltanoModelsResultsDbt",),
        "._models.results_pipeline": ("FlextMeltanoModelsResultsPipeline",),
        "._models.singer": ("FlextMeltanoModelsSinger",),
        ".api": ("FlextMeltano",),
        ".cli": ("FlextMeltanoCLI",),
        ".constants": ("FlextMeltanoConstants",),
        ".models": ("FlextMeltanoModels",),
        ".services.abstractions": ("FlextMeltanoAbstractions",),
        ".services.abstractions_base": ("FlextMeltanoAbstractionsBase",),
        ".services.adapters": ("FlextMeltanoAdapter",),
        ".services.bridge": ("FlextMeltanoBridge",),
        ".services.consumer_bases.dbt_service_base": ("FlextMeltanoDbtServiceBase",),
        ".services.dbt_project": ("FlextMeltanoDbtProjectMixin",),
        ".services.dbt_runner": ("FlextMeltanoDbtRunnerMixin",),
        ".services.executor": ("FlextMeltanoExecutor",),
        ".services.executor_base": ("FlextMeltanoExecutorBase",),
        ".services.library_runner": ("FlextMeltanoLibraryRunner",),
        ".services.meltano_plugins": ("FlextMeltanoComponentService",),
        ".services.singer_sdk": ("Context",),
    },
)

__all__: list[str] = ["FLEXT_MELTANO_LAZY_IMPORTS_PART_01"]
