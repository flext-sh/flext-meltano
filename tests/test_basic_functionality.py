"""Basic functionality test for flext-meltano."""

from __future__ import annotations

from flext_meltano import FlextMeltanoResult


class TestBasicFunctionality:
    """Test basic functionality without complex dependencies."""

    def test_flext_meltano_result_ok(self) -> None:
        """Test FlextMeltanoResult.ok() works correctly."""
        result = FlextMeltanoResult.ok({"test": "data"})

        assert result.success is True
        assert result.data == {"test": "data"}
        assert result.error == ""

    def test_flext_meltano_result_fail(self) -> None:
        """Test FlextMeltanoResult.fail() works correctly."""
        result = FlextMeltanoResult.fail("Test error")

        assert result.success is False
        assert result.data is None
        assert result.error == "Test error"

    def test_flext_meltano_result_init_direct(self) -> None:
        """Test FlextMeltanoResult direct initialization."""
        result = FlextMeltanoResult(success=True, data={"key": "value"}, error="")

        assert result.success is True
        assert result.data == {"key": "value"}
        assert result.error == ""
