# AUTO-GENERATED FILE — Regenerate with: make gen
"""Integration package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.tests.integration.test_docker_integration import (
        TestsFlextMeltanoDockerIntegration as TestsFlextMeltanoDockerIntegration,
    )
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_docker_integration": ("TestsFlextMeltanoDockerIntegration",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
