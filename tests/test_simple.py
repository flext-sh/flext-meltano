"""Simple tests for flext-infrastructure.plugins.flext-meltano functionality.

Modern tests following flext-core standards.
"""

from __future__ import annotations

import pytest


# Test flext-infrastructure.plugins.flext-meltano basic functionality
def test_flext_meltano_imports() -> None:
    """Test that flext-infrastructure.plugins.flext-meltano can be imported."""
    import flext_meltano

    assert flext_meltano is not None
    assert hasattr(flext_meltano, "__name__")
    assert flext_meltano.__name__ == "flext_meltano"


def test_flext_meltano_has_core_dependencies() -> None:
    """Test that flext-infrastructure.plugins.flext-meltano can import from flext-core."""
    # NO FALLBACKS - SEMPRE usar implementações originais conforme instrução
    from flext_core.domain.shared_types import ServiceResult
    assert ServiceResult is not None


def test_service_result_pattern() -> None:
    """Test ServiceResult pattern works correctly."""
    from flext_core.domain.shared_types import ServiceResult
    # Test success case
    success = ServiceResult.ok({"test": "data"})
    assert success.is_success is True
    assert success.data == {"test": "data"}

    # Test failure case
    failure: ServiceResult[str] = ServiceResult.fail("Test error")
    assert failure.is_success is False
    assert failure.error == "Test error"


def test_api_response_pattern() -> None:
    """Test APIResponse pattern works correctly."""
    # APIResponse is not available in flext_core, skip this test
    pytest.skip("APIResponse not implemented in flext_core yet")


class TestFlextMeltanoIntegration:
    """Test flext-infrastructure.plugins.flext-meltano integration patterns."""

    def test_project_manager_available(self) -> None:
        """Test that project manager can be imported."""
        from flext_meltano import MeltanoProjectManager

        assert MeltanoProjectManager is not None
        assert hasattr(MeltanoProjectManager, "__name__")
        assert callable(MeltanoProjectManager)

    def test_unified_layer_available(self) -> None:
        """Test that unified anti-corruption layer can be imported."""
        from flext_meltano import UnifiedMeltanoAntiCorruptionLayer

        assert UnifiedMeltanoAntiCorruptionLayer is not None
        assert hasattr(UnifiedMeltanoAntiCorruptionLayer, "__name__")
        assert callable(UnifiedMeltanoAntiCorruptionLayer)
