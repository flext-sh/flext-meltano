# AUTO-GENERATED FILE — canonical lazy tests facade. Regenerate with: make gen
"""Test package facade exposing the project test aliases lazily."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from tests.base import (
        TestsFlextMeltanoServiceBase as TestsFlextMeltanoServiceBase,
        s as s,
    )
    from tests.constants import (
        TestsFlextMeltanoConstants as TestsFlextMeltanoConstants,
        c as c,
    )
    from tests.models import TestsFlextMeltanoModels as TestsFlextMeltanoModels, m as m
    from tests.protocols import (
        TestsFlextMeltanoProtocols as TestsFlextMeltanoProtocols,
        p,
    )
    from tests.typings import TestsFlextMeltanoTypes as TestsFlextMeltanoTypes, t as t
    from tests.utilities import (
        TestsFlextMeltanoUtilities as TestsFlextMeltanoUtilities,
        u,
    )

_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".constants": ("TestsFlextMeltanoConstants", "c"),
        ".typings": ("TestsFlextMeltanoTypes", "t"),
        ".protocols": ("TestsFlextMeltanoProtocols", "p"),
        ".models": ("TestsFlextMeltanoModels", "m"),
        ".utilities": ("TestsFlextMeltanoUtilities", "u"),
        ".base": ("TestsFlextMeltanoServiceBase", "s"),
    },
)

install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
