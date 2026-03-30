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
    from tests.integration.test_docker_integration import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "TestDockerIntegration": "tests.integration.test_docker_integration",
    "psycopg2": "tests.integration.test_docker_integration",
    "redis": "tests.integration.test_docker_integration",
    "test_docker_integration": "tests.integration.test_docker_integration",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
