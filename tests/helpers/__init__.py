# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Test helpers for flext-meltano tests.

Provides reusable test utilities and helpers for all test modules.
Consolidates typings, models, and protocols in unified classes.

Uses standardized short names (m, t, p, u) for easy access in tests.
Helpers extend main classes and use same short names in place of base classes.

NOTE: Constants have been moved to tests/constants.py - import from tests.constants instead.
NOTE: Models have been consolidated to tests/models.py - import from tests.models instead.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from tests.helpers import docker_test_manager
    from tests.helpers.docker_test_manager import (
        ContainerManager,
        Tk,
        docker_manager,
        docker_services,
    )

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "ContainerManager": "tests.helpers.docker_test_manager",
    "Tk": "tests.helpers.docker_test_manager",
    "docker_manager": "tests.helpers.docker_test_manager",
    "docker_services": "tests.helpers.docker_test_manager",
    "docker_test_manager": "tests.helpers.docker_test_manager",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
