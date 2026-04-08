# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.helpers as _tests_helpers
    from tests.constants import (
        TestsFlextMeltanoConstants,
        TestsFlextMeltanoConstants as c,
    )

    helpers = _tests_helpers
    import tests.integration as _tests_integration

    integration = _tests_integration
    import tests.models as _tests_models

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import TestsFlextMeltanoModels, TestsFlextMeltanoModels as m

    protocols = _tests_protocols
    import tests.typings as _tests_typings
    from tests.protocols import (
        TestsFlextMeltanoProtocols,
        TestsFlextMeltanoProtocols as p,
    )

    typings = _tests_typings
    import tests.unit as _tests_unit
    from tests.typings import TestsFlextMeltanoTypes, TestsFlextMeltanoTypes as t

    unit = _tests_unit
    import tests.utilities as _tests_utilities

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
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
