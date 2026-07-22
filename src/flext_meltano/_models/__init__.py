# AUTO-GENERATED FILE — Regenerate with: make gen
"""Models package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._models.cli_inputs import (
        FlextMeltanoModelsCliInputs as FlextMeltanoModelsCliInputs,
    )
    from flext_meltano._models.cli_params import (
        FlextMeltanoModelsCliParams as FlextMeltanoModelsCliParams,
    )
    from flext_meltano._models.context import (
        FlextMeltanoModelsContext as FlextMeltanoModelsContext,
    )
    from flext_meltano._models.core import (
        FlextMeltanoModelsCore as FlextMeltanoModelsCore,
    )
    from flext_meltano._models.discovery import (
        FlextMeltanoModelsDiscovery as FlextMeltanoModelsDiscovery,
    )
    from flext_meltano._models.instances import (
        FlextMeltanoModelsInstances as FlextMeltanoModelsInstances,
    )
    from flext_meltano._models.instances_data import (
        FlextMeltanoModelsInstancesData as FlextMeltanoModelsInstancesData,
    )
    from flext_meltano._models.logging_config import (
        FlextMeltanoModelsLogging as FlextMeltanoModelsLogging,
    )
    from flext_meltano._models.payloads_data import (
        FlextMeltanoModelsPayloadsData as FlextMeltanoModelsPayloadsData,
    )
    from flext_meltano._models.projects import (
        FlextMeltanoModelsProjects as FlextMeltanoModelsProjects,
    )
    from flext_meltano._models.results import (
        FlextMeltanoModelsResults as FlextMeltanoModelsResults,
    )
    from flext_meltano._models.results_dbt import (
        FlextMeltanoModelsResultsDbt as FlextMeltanoModelsResultsDbt,
    )
    from flext_meltano._models.results_pipeline import (
        FlextMeltanoModelsResultsPipeline as FlextMeltanoModelsResultsPipeline,
    )
    from flext_meltano._models.singer import (
        FlextMeltanoModelsSinger as FlextMeltanoModelsSinger,
    )
    from flext_meltano._models.singer_catalog import (
        FlextMeltanoModelsSingerCatalog as FlextMeltanoModelsSingerCatalog,
    )
    from flext_meltano._models.singer_sdk import (
        FlextMeltanoModelsSingerSdk as FlextMeltanoModelsSingerSdk,
    )
    from flext_meltano._models.sources import (
        FlextMeltanoModelsSources as FlextMeltanoModelsSources,
    )
    from flext_meltano._models.sources_params import (
        FlextMeltanoModelsSourcesParams as FlextMeltanoModelsSourcesParams,
    )
    from flext_meltano._models.transformations import (
        FlextMeltanoModelsTransformations as FlextMeltanoModelsTransformations,
    )
_LAZY_IMPORTS = build_lazy_import_map({
    ".cli_inputs": ("FlextMeltanoModelsCliInputs",),
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
})


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
