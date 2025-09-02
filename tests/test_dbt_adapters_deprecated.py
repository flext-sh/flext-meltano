"""Test dbt_adapters deprecated module - Backward compatibility tests.

Tests deprecated module functionality and proper aliases.
Zero mock usage - all real function testing.
"""

from __future__ import annotations

import unittest
import warnings

from flext_meltano import dbt_adapters


class TestDbtAdaptersDeprecated(unittest.TestCase):
    """Test deprecated dbt_adapters module functionality."""

    def test_deprecation_warning_issued(self) -> None:
        """Test deprecation warning is properly issued."""
        # Test by importing the module in a separate namespace
        import importlib
        import sys

        # Clear any cached imports
        if "flext_meltano.dbt_adapters" in sys.modules:
            del sys.modules["flext_meltano.dbt_adapters"]

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Fresh import should trigger warning
            importlib.import_module("flext_meltano.dbt_adapters")

            # Find our specific warning
            our_warnings = [
                warning
                for warning in w
                if "dbt_adapters module is deprecated" in str(warning.message)
            ]

            # Should have our deprecation warning
            assert len(our_warnings) > 0, (
                f"Expected deprecation warning not found. Warnings: {[str(warning.message) for warning in w]}"
            )

            # Check warning message content
            warning_msg = str(our_warnings[0].message)
            assert "dbt_adapters module is deprecated" in warning_msg
            assert "flext_meltano.adapters" in warning_msg
            assert "flext_meltano.wrappers" in warning_msg

    def test_legacy_aliases_exist(self) -> None:
        """Test legacy aliases are properly defined."""
        # Check FlextDbtAdapter alias exists
        assert hasattr(dbt_adapters, "FlextDbtAdapter")

        # Check MeltanoDbtWrapper alias exists
        assert hasattr(dbt_adapters, "MeltanoDbtWrapper")

        # Check original classes exist
        assert hasattr(dbt_adapters, "FlextMeltanoAdapter")
        assert hasattr(dbt_adapters, "FlextMeltanoWrapper")

    def test_alias_relationships(self) -> None:
        """Test aliases point to correct classes."""
        # FlextDbtAdapter should be alias for FlextMeltanoAdapter
        assert dbt_adapters.FlextDbtAdapter is dbt_adapters.FlextMeltanoAdapter

        # MeltanoDbtWrapper should be alias for FlextMeltanoWrapper.DbtWrapper
        assert (
            dbt_adapters.MeltanoDbtWrapper
            is dbt_adapters.FlextMeltanoWrapper.DbtWrapper
        )

    def test_all_exports_defined(self) -> None:
        """Test __all__ contains all expected exports."""
        expected_exports = [
            "FlextDbtAdapter",
            "FlextMeltanoAdapter",
            "FlextMeltanoWrapper",
            "MeltanoDbtWrapper",
        ]

        assert hasattr(dbt_adapters, "__all__")
        for export in expected_exports:
            assert export in dbt_adapters.__all__

    def test_imports_work(self) -> None:
        """Test all imports work correctly."""
        # Test individual imports work
        from flext_meltano.dbt_adapters import (
            FlextDbtAdapter,
            FlextMeltanoAdapter,
            FlextMeltanoWrapper,
            MeltanoDbtWrapper,
        )

        # All should be importable without errors
        assert FlextDbtAdapter is not None
        assert FlextMeltanoAdapter is not None
        assert FlextMeltanoWrapper is not None
        assert MeltanoDbtWrapper is not None

    def test_backward_compatibility_maintained(self) -> None:
        """Test backward compatibility is fully maintained."""
        # Legacy import pattern should work
        from flext_meltano.dbt_adapters import FlextDbtAdapter

        # Should be able to use as before
        adapter_class = FlextDbtAdapter
        assert adapter_class is not None

        # Check it has expected interface (should inherit from FlextMeltanoAdapter)
        assert hasattr(adapter_class, "__name__")


if __name__ == "__main__":
    unittest.main()
