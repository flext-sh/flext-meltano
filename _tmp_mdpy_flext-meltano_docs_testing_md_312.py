# from flext-meltano_docs/testing.md:312
from __future__ import annotations

# ✅ CORRECT - Proper mocking for isolation
from unittest.mock import patch
import pytest


@pytest.fixture
def mock_meltano_adapter():
    """Provide mocked Meltano adapter for testing."""
    with patch("flext_meltano.adapters.FlextMeltanoAdapter") as mock:
        mock.return_value.run_tap.return_value = r.ok({"status": "success"})
        yield mock


def test_service_with_meltano_integration(mock_meltano_adapter):
    """Test service integration with mocked Meltano operations."""
    service = FlextMeltanoService()

    result = service.execute_pipeline("tap-csv", "target-postgres")

    assert result.success
    mock_meltano_adapter.return_value.run_tap.assert_called_once()```
### **Fixture Best Practices**

