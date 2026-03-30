# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Integration tests for flext-meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from tests.integration import test_docker_integration
    from tests.integration.test_docker_integration import (
        TestDockerIntegration,
        psycopg2,
        redis,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "TestDockerIntegration": [
        "tests.integration.test_docker_integration",
        "TestDockerIntegration",
    ],
    "psycopg2": ["tests.integration.test_docker_integration", "psycopg2"],
    "redis": ["tests.integration.test_docker_integration", "redis"],
    "test_docker_integration": ["tests.integration.test_docker_integration", ""],
}

__all__ = [
    "TestDockerIntegration",
    "psycopg2",
    "redis",
    "test_docker_integration",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
