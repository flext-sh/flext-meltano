# AUTO-GENERATED FILE — Regenerate with: make gen
"""Unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.tests.unit.test_api import (
        TestsFlextMeltanoApi as TestsFlextMeltanoApi,
    )
    from flext_meltano.tests.unit.test_cli_integration import (
        TestsFlextMeltanoCliIntegration as TestsFlextMeltanoCliIntegration,
    )
    from flext_meltano.tests.unit.test_cli_small_managers import (
        TestsFlextMeltanoCliSmallManagers as TestsFlextMeltanoCliSmallManagers,
    )
    from flext_meltano.tests.unit.test_constants import (
        TestsFlextMeltanoConstantsUnit as TestsFlextMeltanoConstantsUnit,
    )
    from flext_meltano.tests.unit.test_execution_result import (
        TestsFlextMeltanoExecutionResult as TestsFlextMeltanoExecutionResult,
    )
    from flext_meltano.tests.unit.test_executors import (
        TestsFlextMeltanoExecutors as TestsFlextMeltanoExecutors,
    )
    from flext_meltano.tests.unit.test_library_runner import (
        TestsFlextMeltanoLibraryRunner as TestsFlextMeltanoLibraryRunner,
    )
    from flext_meltano.tests.unit.test_models import (
        TestsFlextMeltanoModelsUnit as TestsFlextMeltanoModelsUnit,
    )
    from flext_meltano.tests.unit.test_plugin_protocols import (
        TestsFlextMeltanoPluginProtocols as TestsFlextMeltanoPluginProtocols,
    )
    from flext_meltano.tests.unit.test_services import (
        TestsFlextMeltanoServices as TestsFlextMeltanoServices,
    )
    from flext_meltano.tests.unit.test_singer_cli_translator import (
        TestsFlextMeltanoSingerCliTranslator as TestsFlextMeltanoSingerCliTranslator,
    )
    from flext_meltano.tests.unit.test_singer_sdk_adapter import (
        TestsFlextMeltanoSingerSdkAdapter as TestsFlextMeltanoSingerSdkAdapter,
    )
    from flext_meltano.tests.unit.test_singer_types import (
        TestsFlextMeltanoSingerTypes as TestsFlextMeltanoSingerTypes,
    )
    from flext_meltano.tests.unit.test_tap_abstractions import (
        TestsFlextMeltanoTapAbstractions as TestsFlextMeltanoTapAbstractions,
    )
    from flext_meltano.tests.unit.test_target_abstractions import (
        TestsFlextMeltanoTargetAbstractions as TestsFlextMeltanoTargetAbstractions,
    )
    from flext_meltano.tests.unit.test_typings import (
        TestsFlextMeltanoTypingsUnit as TestsFlextMeltanoTypingsUnit,
    )
    from flext_meltano.tests.unit.test_validators import (
        TestsFlextMeltanoValidators as TestsFlextMeltanoValidators,
    )
    from flext_meltano.tests.unit.tests_pipeline_cli_managers import (
        TestFlextMeltanoPipelineCliManagers as TestFlextMeltanoPipelineCliManagers,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".fixtures": ("fixtures",),
        ".test_api": ("TestsFlextMeltanoApi",),
        ".test_cli_integration": ("TestsFlextMeltanoCliIntegration",),
        ".test_cli_small_managers": ("TestsFlextMeltanoCliSmallManagers",),
        ".test_constants": ("TestsFlextMeltanoConstantsUnit",),
        ".test_execution_result": ("TestsFlextMeltanoExecutionResult",),
        ".test_executors": ("TestsFlextMeltanoExecutors",),
        ".test_library_runner": ("TestsFlextMeltanoLibraryRunner",),
        ".test_models": ("TestsFlextMeltanoModelsUnit",),
        ".test_plugin_protocols": ("TestsFlextMeltanoPluginProtocols",),
        ".test_services": ("TestsFlextMeltanoServices",),
        ".test_singer_cli_translator": ("TestsFlextMeltanoSingerCliTranslator",),
        ".test_singer_sdk_adapter": ("TestsFlextMeltanoSingerSdkAdapter",),
        ".test_singer_types": ("TestsFlextMeltanoSingerTypes",),
        ".test_tap_abstractions": ("TestsFlextMeltanoTapAbstractions",),
        ".test_target_abstractions": ("TestsFlextMeltanoTargetAbstractions",),
        ".test_typings": ("TestsFlextMeltanoTypingsUnit",),
        ".test_validators": ("TestsFlextMeltanoValidators",),
        ".tests_pipeline_cli_managers": ("TestFlextMeltanoPipelineCliManagers",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
