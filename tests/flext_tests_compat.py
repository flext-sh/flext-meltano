"""Compatibility module for flext-tests - imports from flext-core.

This module provides compatibility imports from flext-core flext_tests
to maintain backwards compatibility with existing test code.
"""

from __future__ import annotations

from flext_tests.matchers import FlextTestsMatchers
from flext_tests.utilities import FlextTestsUtilities

__all__ = [
    "FlextTestsMatchers",
    "FlextTestsUtilities",
]
