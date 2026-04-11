# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_meltano.test_docker_integration import TestDockerIntegration
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".test_docker_integration": ("TestDockerIntegration",),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "TestDockerIntegration",
]
