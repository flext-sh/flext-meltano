"""Simple tests for flext-infrastructure.plugins.flext-meltano functionality.

Modern tests following flext-core standards.
"""

from __future__ import annotations

import pytest

import flext_meltano
from flext_meltano import (
    FlextMeltanoBridge,
    flext_meltano_execute_job,
    flext_meltano_run_command,
)
from flext_meltano.helpers.execution import FlextMeltanoResult


# Test flext-infrastructure.plugins.flext-meltano basic functionality
def test_flext_meltano_imports() -> None:
    """Test that flext-infrastructure.plugins.flext-meltano can be imported."""

    assert flext_meltano is not None
    assert hasattr(flext_meltano, "__name__")
    assert flext_meltano.__name__ == "flext_meltano"


def test_flext_meltano_has_isolated_result() -> None:
    """Test that flext-meltano has isolated result implementation."""
    # ISOLATED IMPLEMENTATION - No flext_core dependency

    assert FlextMeltanoResult is not None


def test_service_result_pattern() -> None:
    """Test FlextMeltanoResult pattern works correctly."""

    # Test success case
    success = FlextMeltanoResult.ok({"test": "data"})
    assert success.success is True
    assert success.data == {"test": "data"}

    # Test failure case
    failure: FlextMeltanoResult[str,] = FlextMeltanoResult.fail("Test error")
    assert failure.success is False
    assert failure.error == "Test error"


def test_api_response_pattern() -> None:
    """Test FlextAPIResponse pattern works correctly."""
    # FlextAPIResponse is not available in flext_core, skip this test
    pytest.skip("FlextAPIResponse not implemented in flext_core yet")


class TestFlextMeltanoIntegration:
    """Test flext-meltano isolated integration patterns."""

    def test_bridge_available(self) -> None:
        """Test that bridge can be imported."""

        assert FlextMeltanoBridge is not None
        assert hasattr(FlextMeltanoBridge, "__name__")
        assert callable(FlextMeltanoBridge)

    def test_execution_helpers_available(self) -> None:
        """Test that execution helpers can be imported."""

        assert flext_meltano_execute_job is not None
        assert flext_meltano_run_command is not None
        assert callable(flext_meltano_execute_job)
        assert callable(flext_meltano_run_command)
