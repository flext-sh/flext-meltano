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
    # 🚨 ARCHITECTURAL COMPLIANCE: Using módulo raiz imports
    from flext_meltano.infrastructure.di_container import FlextResult

    assert FlextResult is not None


def test_service_result_pattern() -> None:
    """Test FlextResult pattern works correctly."""
    from flext_meltano.infrastructure.di_container import FlextResult

    # Test success case
    success = FlextResult.ok({"test": "data"})
    assert success.success is True
    assert success.data == {"test": "data"}

    # Test failure case
    failure: FlextResult[str] = FlextResult.fail("Test error")
    assert failure.success is False
    assert failure.error == "Test error"


def test_api_response_pattern() -> None:
    """Test FlextAPIResponse pattern works correctly."""
    # FlextAPIResponse is not available in flext_core, skip this test
    pytest.skip("FlextAPIResponse not implemented in flext_core yet")


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
