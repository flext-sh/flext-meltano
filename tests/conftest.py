"""FLEXT Meltano pytest bootstrap.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests import c, u

if TYPE_CHECKING:
    from collections.abc import Generator

pytest_plugins = ["tests.unit.fixtures"]


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """Declare actual service fixtures without suppressing pure integration."""
    for item in items:
        if "docker_services" in item.fixturenames:
            item.add_marker(pytest.mark.docker)
        for fixture, port in (
            ("postgres_service", c.Meltano.Tests.POSTGRES_PORT),
            ("redis_service", c.Meltano.Tests.REDIS_PORT),
        ):
            if fixture in item.fixturenames:
                item.add_marker(pytest.mark.connectivity(host=c.Meltano.Tests.HOST, port=port))


@pytest.fixture
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
    with u.Tests.env_vars_context({
        "FLEXT_ENV": "test",
        "FLEXT_LOG_LEVEL": "DEBUG",
        "MELTANO_ENVIRONMENT": "test",
    }):
        yield


def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "meltano: Meltano-specific tests")
    config.addinivalue_line("markers", "singer: Singer protocol tests")
    config.addinivalue_line("markers", "pipeline: Pipeline execution tests")
    config.addinivalue_line("markers", "cli: CLI command tests")
    config.addinivalue_line("markers", "slow: Slow tests")
    config.addinivalue_line("markers", "docker: Docker-based tests")
