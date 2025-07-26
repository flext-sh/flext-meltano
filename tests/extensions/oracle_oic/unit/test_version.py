"""Unit tests for flext-oracle-oic-ext version module."""

from __future__ import annotations

import flext_oracle_oic_ext.__version__ as version_module
from flext_oracle_oic_ext import __version__


def test_version_import() -> None:
    """Test that version can be imported successfully."""
    assert __version__ is not None


def test_version_module_functions() -> None:
    """Test version module functions - isolated from flext_core."""
    # Test version is a valid string format
    assert isinstance(__version__, str)
    assert len(__version__) > 0
    # Test version follows semantic versioning pattern
    parts = __version__.split(".")
    assert len(parts) >= 2  # At least major.minor


def test_version_attributes_exist() -> None:
    """Test that version attributes exist and have expected types."""

    # Test __version__ exists and is string
    assert hasattr(version_module, "__version__")
    assert isinstance(version_module.__version__, str)

    # Test __version_info__ exists and is tuple
    assert hasattr(version_module, "__version_info__")
    assert isinstance(version_module.__version_info__, tuple)
