# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests import (
        conftest,
        constants,
        helpers,
        integration,
        models,
        protocols,
        typings,
        unit,
        utilities,
    )
    from tests.constants import (
        TestsFlextMeltanoConstants,
        TestsFlextMeltanoConstants as c,
    )
    from tests.models import TestsFlextMeltanoModels, TestsFlextMeltanoModels as m
    from tests.protocols import (
        TestsFlextMeltanoProtocols,
        TestsFlextMeltanoProtocols as p,
    )
    from tests.typings import TestsFlextMeltanoTypes, TestsFlextMeltanoTypes as t
    from tests.utilities import (
        TestsFlextMeltanoUtilities,
        TestsFlextMeltanoUtilities as u,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "tests.helpers",
        "tests.integration",
        "tests.unit",
    ),
    {
        "TestsFlextMeltanoConstants": ("tests.constants", "TestsFlextMeltanoConstants"),
        "TestsFlextMeltanoModels": ("tests.models", "TestsFlextMeltanoModels"),
        "TestsFlextMeltanoProtocols": ("tests.protocols", "TestsFlextMeltanoProtocols"),
        "TestsFlextMeltanoTypes": ("tests.typings", "TestsFlextMeltanoTypes"),
        "TestsFlextMeltanoUtilities": ("tests.utilities", "TestsFlextMeltanoUtilities"),
        "c": ("tests.constants", "TestsFlextMeltanoConstants"),
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "helpers": "tests.helpers",
        "integration": "tests.integration",
        "m": ("tests.models", "TestsFlextMeltanoModels"),
        "models": "tests.models",
        "p": ("tests.protocols", "TestsFlextMeltanoProtocols"),
        "protocols": "tests.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "t": ("tests.typings", "TestsFlextMeltanoTypes"),
        "typings": "tests.typings",
        "u": ("tests.utilities", "TestsFlextMeltanoUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("logger", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

__all__ = [
    "TestsFlextMeltanoConstants",
    "TestsFlextMeltanoModels",
    "TestsFlextMeltanoProtocols",
    "TestsFlextMeltanoTypes",
    "TestsFlextMeltanoUtilities",
    "c",
    "conftest",
    "constants",
    "d",
    "e",
    "h",
    "helpers",
    "integration",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "t",
    "typings",
    "u",
    "unit",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
