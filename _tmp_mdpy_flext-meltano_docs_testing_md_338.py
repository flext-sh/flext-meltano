# from flext-meltano_docs/testing.md:338
from __future__ import annotations


# ✅ CORRECT - Reusable test fixtures
@pytest.fixture
def sample_config():
    """Provide sample configuration for testing."""
    return FlextMeltanoSettings(
        project_root=Path("/tmp/test"),
        environment="test",
        plugins=[{"name": "tap-csv", "variant": "meltano"}],
    )


@pytest.fixture
def mock_plugin_service():
    """Provide mocked plugin service."""
    service = Mock(spec=FlextMeltanoPluginService)
    service.discover_plugins.return_value = r.ok([])
    return service```
______________________________________________________________________

## 📊 **TEST METRICS & MONITORING**

### **Coverage Dashboard Configuration**

