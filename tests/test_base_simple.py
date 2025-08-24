# FACADE: test_base_simple.py - Deprecated, use test_service_simple.py
"""DEPRECATED: Use test_service_simple.py instead.

This is a backward compatibility facade following CLAUDE.md Phase 3 strategy.
The original functionality has been moved to test_service_simple.py which follows
PEP8 naming conventions.

Migration path:
- Update imports to use test_service_simple
- This facade will be removed in future versions
"""

import warnings

from .test_service_simple import *  # noqa: F403,F401

warnings.warn(
    "test_base_simple.py is deprecated, use test_service_simple.py instead",
    DeprecationWarning,
    stacklevel=2,
)
