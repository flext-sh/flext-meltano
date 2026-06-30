# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_MELTANO_LAZY_IMPORTS_PART_02 = build_lazy_import_map(
    {
        "._models.singer_catalog": ("FlextMeltanoModelsSingerCatalog",),
        "._models.singer_sdk": ("FlextMeltanoModelsSingerSdk",),
        "._models.sources": ("FlextMeltanoModelsSources",),
        "._models.sources_params": ("FlextMeltanoModelsSourcesParams",),
        "._models.transformations": ("FlextMeltanoModelsTransformations",),
        "._protocols.cli": ("FlextMeltanoProtocolsBase",),
        "._protocols.plugin": ("FlextMeltanoProtocolsPlugin",),
        "._protocols.project": ("FlextMeltanoProtocolsProject",),
        "._protocols.services": ("FlextMeltanoProtocolsServices",),
        "._protocols.singer": ("FlextMeltanoProtocolsSinger",),
        "._typings.base": ("FlextMeltanoTypingsBase",),
        "._typings.domains": ("FlextMeltanoTypingsDomains",),
        "._typings.singer": ("FlextMeltanoTypingsSinger",),
        "._utilities.runtime": ("FlextMeltanoUtilitiesRuntime",),
        ".base": ("FlextMeltanoServiceBase",),
        ".protocols": ("FlextMeltanoProtocols",),
        ".services.consumer_bases.tap_service_base": ("FlextMeltanoTapServiceBase",),
        ".services.consumer_bases.target_service_base": (
            "FlextMeltanoTargetServiceBase",
        ),
        ".services.meltano_plugin_discovery": ("FlextMeltanoPluginDiscoveryMixin",),
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
        ".utilities": ("FlextMeltanoUtilities",),
    },
)

__all__: list[str] = ["FLEXT_MELTANO_LAZY_IMPORTS_PART_02"]
