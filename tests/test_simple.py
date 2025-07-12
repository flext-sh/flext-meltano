"""Simple tests for flext-meltano functionality.

Modern tests following flext-core standards.
"""

from __future__ import annotations

import pytest


# Test flext-meltano basic functionality
def test_flext_meltano_imports() -> None:
    """Test that flext-meltano can be imported."""
    try:
        import flext_meltano

        assert flext_meltano is not None
    except ImportError:
        pytest.skip("flext-meltano not available")


def test_flext_meltano_has_core_dependencies() -> None:
    """Test that flext-meltano can import from flext-core."""
    try:
        from flext_core import APIResponse
        from flext_core import ServiceResult

        assert ServiceResult is not None
        assert APIResponse is not None
    except ImportError:
        pytest.fail("flext-core dependencies not available")


def test_service_result_pattern() -> None:
    """Test ServiceResult pattern works correctly."""
    from flext_core import ServiceResult

    # Test success case
    success = ServiceResult.success({"test": "data"})
    assert success.is_success is True
    assert success.data == {"test": "data"}

    # Test failure case
    failure = ServiceResult.failure("Test error")
    assert failure.is_success is False
    assert failure.error == "Test error"


def test_api_response_pattern() -> None:
    """Test APIResponse pattern works correctly."""
    from flext_core import APIResponse

    response = APIResponse(
        success=True,
        message="Test successful",
    )

    assert response.success is True
    assert response.message == "Test successful"
    assert response.timestamp is not None


class TestFlextMeltanoIntegration:
    """Test flext-meltano integration patterns."""

    def test_project_manager_available(self) -> None:
        """Test that project manager can be imported."""
        try:
            from flext_meltano import MeltanoProjectManager

            assert MeltanoProjectManager is not None
        except ImportError:
            pytest.skip("MeltanoProjectManager not available")

    def test_unified_layer_available(self) -> None:
        """Test that unified anti-corruption layer can be imported."""
        try:
            from flext_meltano import UnifiedMeltanoAntiCorruptionLayer

            assert UnifiedMeltanoAntiCorruptionLayer is not None
        except ImportError:
            pytest.skip("UnifiedMeltanoAntiCorruptionLayer not available")
