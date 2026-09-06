# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .test_cli_integration import TestsFlextMeltanoCliIntegration
    from .test_cli_small_managers import TestsFlextMeltanoCliSmallManagers
    from .test_constants import TestsFlextMeltanoConstantsUnit
    from .test_declarative_tap import TestsFlextMeltanoDeclarativeTap
    from .test_execution_result import TestsFlextMeltanoExecutionResult
    from .test_library_runner import TestsFlextMeltanoLibraryRunner
    from .test_models import TestsFlextMeltanoModelsUnit
    from .test_plugin_protocols import TestsFlextMeltanoPluginProtocols
    from .test_singer_cli_translator import TestsFlextMeltanoSingerCliTranslator
    from .test_singer_sdk_adapter import TestsFlextMeltanoSingerSdkAdapter
    from .test_singer_types import TestsFlextMeltanoSingerTypes
    from .test_target_abstractions import TestsFlextMeltanoTargetAbstractions
    from .test_typings import TestsFlextMeltanoTypingsUnit
    from .test_validators import TestsFlextMeltanoValidators
__all__: tuple[str, ...] = (
    "TestsFlextMeltanoCliIntegration",
    "TestsFlextMeltanoCliSmallManagers",
    "TestsFlextMeltanoConstantsUnit",
    "TestsFlextMeltanoDeclarativeTap",
    "TestsFlextMeltanoExecutionResult",
    "TestsFlextMeltanoLibraryRunner",
    "TestsFlextMeltanoModelsUnit",
    "TestsFlextMeltanoPluginProtocols",
    "TestsFlextMeltanoSingerCliTranslator",
    "TestsFlextMeltanoSingerSdkAdapter",
    "TestsFlextMeltanoSingerTypes",
    "TestsFlextMeltanoTargetAbstractions",
    "TestsFlextMeltanoTypingsUnit",
    "TestsFlextMeltanoValidators",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".test_cli_integration": ("TestsFlextMeltanoCliIntegration",),
            ".test_cli_small_managers": ("TestsFlextMeltanoCliSmallManagers",),
            ".test_constants": ("TestsFlextMeltanoConstantsUnit",),
            ".test_declarative_tap": ("TestsFlextMeltanoDeclarativeTap",),
            ".test_execution_result": ("TestsFlextMeltanoExecutionResult",),
            ".test_library_runner": ("TestsFlextMeltanoLibraryRunner",),
            ".test_models": ("TestsFlextMeltanoModelsUnit",),
            ".test_plugin_protocols": ("TestsFlextMeltanoPluginProtocols",),
            ".test_singer_cli_translator": ("TestsFlextMeltanoSingerCliTranslator",),
            ".test_singer_sdk_adapter": ("TestsFlextMeltanoSingerSdkAdapter",),
            ".test_singer_types": ("TestsFlextMeltanoSingerTypes",),
            ".test_target_abstractions": ("TestsFlextMeltanoTargetAbstractions",),
            ".test_typings": ("TestsFlextMeltanoTypingsUnit",),
            ".test_validators": ("TestsFlextMeltanoValidators",),
            "flext_tests": (
                "c",
                "d",
                "e",
                "h",
                "m",
                "p",
                "r",
                "s",
                "t",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "u",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
