"""Compatibility module for flext-tests - imports from flext-core.

This module provides compatibility imports from flext-core flext_tests
to maintain backwards compatibility with existing test code.
"""

from __future__ import annotations

from flext_tests import tm, u

# Backward compatibility aliases
FlextTestsMatchers = tm
FlextTestsUtilities = u

__all__ = [
    "FlextTestsMatchers",
    "FlextTestsUtilities",
    "tm",
    "u",
]
