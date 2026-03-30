# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Integration tests for flext-meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.integration import test_docker_integration as test_docker_integration
    from tests.integration.test_docker_integration import (
        TestDockerIntegration as TestDockerIntegration,
        psycopg2 as psycopg2,
        redis as redis,
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

_EXPORTS: Sequence[str] = [
    "TestDockerIntegration",
    "psycopg2",
    "redis",
    "test_docker_integration",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
