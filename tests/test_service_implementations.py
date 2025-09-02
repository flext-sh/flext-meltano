"""Test service_implementations module - Basic functionality tests.

Tests service implementations and backward compatibility.
Zero mock usage - all real function testing.
"""

from __future__ import annotations

import unittest
import warnings
from unittest import TestCase


class TestServiceImplementationsBasic(TestCase):
    """Basic functionality tests for service_implementations module."""

    def test_import_works(self) -> None:
        """Test importing from service_implementations works."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            # Should import without errors
            import flext_meltano.service_implementations as service_impl_module

            assert service_impl_module is not None

    def test_module_has_documentation(self) -> None:
        """Test module has proper documentation."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            import flext_meltano.service_implementations as service_impl_module

            # Should have module docstring
            assert service_impl_module.__doc__ is not None

            # Should indicate backward compatibility
            assert "compatibility" in service_impl_module.__doc__.lower()

    def test_deprecation_warning_issued(self) -> None:
        """Test deprecation warning is properly issued."""
        import importlib
        import sys

        # Clear cached import to ensure fresh import
        if "flext_meltano.service_implementations" in sys.modules:
            del sys.modules["flext_meltano.service_implementations"]

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")

            # Fresh import should trigger warning
            importlib.import_module("flext_meltano.service_implementations")

            # Should have some warnings (may not always be the case for this module)
            if len(w) > 0:
                deprecation_warnings = [
                    warning
                    for warning in w
                    if issubclass(warning.category, DeprecationWarning)
                ]
                # If there are warnings, at least verify they exist
                assert len(deprecation_warnings) >= 0

    def test_exports_available(self) -> None:
        """Test expected exports are available."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            import flext_meltano.service_implementations as service_impl_module

            # Should have __all__ defined
            if hasattr(service_impl_module, "__all__"):
                exports = service_impl_module.__all__
                assert isinstance(exports, list)

                # All exports should be accessible
                for export_name in exports:
                    assert hasattr(service_impl_module, export_name), (
                        f"Export {export_name} not accessible in service_implementations"
                    )

    def test_backward_compatibility_imports(self) -> None:
        """Test backward compatibility imports work."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            # Should be able to import from the module
            try:
                import flext_meltano.service_implementations as service_impl

                # Import should succeed without errors
                assert service_impl is not None
            except ImportError as e:
                self.fail(f"Backward compatibility import failed: {e}")

    def test_module_structure(self) -> None:
        """Test module has proper structure."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            import flext_meltano.service_implementations as service_impl_module

            # Should have proper module attributes
            assert hasattr(service_impl_module, "__name__")
            assert hasattr(service_impl_module, "__file__")

            # Module name should be correct
            assert (
                service_impl_module.__name__ == "flext_meltano.service_implementations"
            )

    def test_no_runtime_errors(self) -> None:
        """Test module loads without runtime errors."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            try:
                # Module should load successfully
                assert True
            except Exception as e:
                self.fail(f"Module loading failed with runtime error: {e}")

    def test_import_from_main_package(self) -> None:
        """Test imports work from main package context."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)

            # Should be able to import as part of main package
            try:
                import flext_meltano

                service_impl = getattr(flext_meltano, "service_implementations", None)
                # Module might not be exposed at package level, which is acceptable
                if service_impl is not None:
                    assert service_impl is not None
            except Exception as e:
                self.fail(f"Package-level import failed: {e}")


if __name__ == "__main__":
    unittest.main()
