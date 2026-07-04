"""FLEXT Meltano pytest bootstrap."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.utilities import u

if TYPE_CHECKING:
    from collections.abc import Generator

pytest_plugins = ["tests.unit.fixtures"]


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
