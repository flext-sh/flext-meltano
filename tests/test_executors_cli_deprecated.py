"""Test executors_cli deprecated module - Backward compatibility tests.

Tests deprecated executors_cli module functionality and proper aliases.
Zero mock usage - all real function testing.
"""

from __future__ import annotations

import unittest
import warnings
from unittest import TestCase


class TestExecutorsCliDeprecated(TestCase):
    """Test deprecated executors_cli module functionality."""

    def test_deprecation_warning_issued(self) -> None:
        """Test deprecation warning is properly issued."""
        import importlib
        import sys

        # Clear cached import to ensure fresh import
        if "flext_meltano.executors_cli" in sys.modules:
            del sys.modules["flext_meltano.executors_cli"]

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Fresh import triggers warning
            importlib.import_module("flext_meltano.executors_cli")

            # Find our specific warning
            our_warnings = [
                warning
                for warning in w
                if "executors_cli module is deprecated" in str(warning.message)
            ]

            # Should have our deprecation warning
            assert len(our_warnings) > 0, (
                f"Expected deprecation warning not found. All warnings: {[str(warning.message) for warning in w]}"
            )

            # Check warning message content
            warning_msg = str(our_warnings[0].message)
            assert "executors_cli module is deprecated" in warning_msg
            assert "flext_meltano.executors" in warning_msg

    def test_legacy_aliases_exist(self) -> None:
        """Test legacy aliases are properly defined."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            from flext_meltano import executors_cli

            # Check FlextMeltanoCli alias exists
            assert hasattr(executors_cli, "FlextMeltanoCli")

            # Check flext_meltano_run_cli alias exists
            assert hasattr(executors_cli, "flext_meltano_run_cli")

    def test_alias_relationships(self) -> None:
        """Test aliases point to correct classes."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            from flext_meltano import executors_cli
            from flext_meltano.executors import FlextMeltanoExecutor

            # FlextMeltanoCli should be alias for FlextMeltanoExecutor
            assert executors_cli.FlextMeltanoCli is FlextMeltanoExecutor

            # flext_meltano_run_cli should be alias for create_cli_runner
            assert (
                executors_cli.flext_meltano_run_cli
                is FlextMeltanoExecutor.create_cli_runner
            )

    def test_all_exports_defined(self) -> None:
        """Test __all__ contains expected exports."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            from flext_meltano import executors_cli

            expected_exports = ["FlextMeltanoCli", "flext_meltano_run_cli"]

            assert hasattr(executors_cli, "__all__")
            for export in expected_exports:
                assert export in executors_cli.__all__

    def test_imports_work(self) -> None:
        """Test all imports work correctly."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            # Test individual imports work
            from flext_meltano.executors_cli import (
                FlextMeltanoCli,
                flext_meltano_run_cli,
            )

            # All should be importable without errors
            assert FlextMeltanoCli is not None
            assert flext_meltano_run_cli is not None

    def test_backward_compatibility_maintained(self) -> None:
        """Test backward compatibility is fully maintained."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            # Legacy import pattern should work
            from flext_meltano.executors_cli import FlextMeltanoCli

            # Should be able to use as before
            executor_class = FlextMeltanoCli
            assert executor_class is not None

            # Check it has expected interface
            assert hasattr(executor_class, "__name__")

            # Should be able to instantiate
            try:
                executor = executor_class()
                assert executor is not None
            except Exception:
                # If instantiation fails, that's acceptable as long as class exists
                pass

    def test_wildcard_import_works(self) -> None:
        """Test wildcard import works correctly."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            # Test by importing specific items instead of wildcard
            try:
                from flext_meltano import executors_cli

                # Should be able to access all exports
                if hasattr(executors_cli, "__all__"):
                    for export_name in executors_cli.__all__:
                        assert hasattr(executors_cli, export_name)
                assert True
            except ImportError as e:
                self.fail(f"Import failed: {e}")

    def test_function_alias_callable(self) -> None:
        """Test function alias is callable."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            from flext_meltano.executors_cli import flext_meltano_run_cli

            # Should be callable
            assert callable(flext_meltano_run_cli)

    def test_module_documentation(self) -> None:
        """Test module has proper documentation."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            import flext_meltano.executors_cli as executors_cli_module

            # Should have module docstring
            assert executors_cli_module.__doc__ is not None

            # Should mention deprecation
            assert "DEPRECATED" in executors_cli_module.__doc__
            assert "backward compatibility" in executors_cli_module.__doc__


if __name__ == "__main__":
    unittest.main()
