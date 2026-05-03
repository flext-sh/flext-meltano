# AUTO-GENERATED FILE — Regenerate with: make gen
"""Models package."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".cli_params": ("FlextMeltanoModelsCliParams",),
        ".context": ("FlextMeltanoModelsContext",),
        ".core": ("FlextMeltanoModelsCore",),
        ".discovery": ("FlextMeltanoModelsDiscovery",),
        ".instances": ("FlextMeltanoModelsInstances",),
        ".instances_data": ("FlextMeltanoModelsInstancesData",),
        ".logging_config": ("FlextMeltanoModelsLogging",),
        ".payloads_data": ("FlextMeltanoModelsPayloadsData",),
        ".projects": ("FlextMeltanoModelsProjects",),
        ".results": ("FlextMeltanoModelsResults",),
        ".results_dbt": ("FlextMeltanoModelsResultsDbt",),
        ".results_pipeline": ("FlextMeltanoModelsResultsPipeline",),
        ".singer": ("FlextMeltanoModelsSinger",),
        ".singer_catalog": ("FlextMeltanoModelsSingerCatalog",),
        ".singer_sdk": ("FlextMeltanoModelsSingerSdk",),
        ".sources": ("FlextMeltanoModelsSources",),
        ".sources_params": ("FlextMeltanoModelsSourcesParams",),
        ".transformations": ("FlextMeltanoModelsTransformations",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
