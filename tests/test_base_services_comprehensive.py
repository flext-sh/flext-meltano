# FACADE: test_base_services_comprehensive.py - Deprecated, use test_service_implementations_comprehensive.py
"""DEPRECATED: Use test_service_implementations_comprehensive.py instead.

This is a backward compatibility facade following CLAUDE.md Phase 3 strategy.
The original functionality has been moved to test_service_implementations_comprehensive.py
which follows PEP8 naming conventions.

Migration path:
- Update imports to use test_service_implementations_comprehensive
- This facade will be removed in future versions
"""

import warnings

from .test_service_implementations_comprehensive import *

warnings.warn(
    "test_base_services_comprehensive.py is deprecated, use test_service_implementations_comprehensive.py instead",
    DeprecationWarning,
    stacklevel=2,
)
