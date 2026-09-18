# from flext-meltano/docs/guides/phase_4_implementation_plan.md:483
from __future__ import annotations


def test_operation_returns_flext_result():
    """Test that operations return r instances."""
    service = FlextMeltanoService()

    result = service.discover_plugins()

    assert isinstance(result, r)
    assert result.success or result.failure


def test_operation_success_path():
    """Test successful operation execution."""
    service = FlextMeltanoService()

    result = service.discover_plugins()

    assert result.success
    plugins = result.unwrap()
    assert isinstance(plugins, list)


def test_operation_failure_path():
    """Test operation failure handling."""
    service = FlextMeltanoService()

    # Setup failure scenario
    result = service.run_invalid_operation()

    assert result.failure
    error = result.error_value
    assert isinstance(error, FlextMeltanoError)```
#### **Mock Integration Pattern**

