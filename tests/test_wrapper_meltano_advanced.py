# FACADE: test_wrapper_meltano_advanced.py - Deprecated, use test_meltano_adapter_advanced.py
"""DEPRECATED: Use test_meltano_adapter_advanced.py instead.

This is a backward compatibility facade following CLAUDE.md Phase 3 strategy.
The original functionality has been moved to test_meltano_adapter_advanced.py
which follows PEP8 naming conventions.

Migration path:
- Update imports to use test_meltano_adapter_advanced
- This facade will be removed in future versions
"""

import warnings

from .test_meltano_adapter_advanced import *

warnings.warn(
    "test_wrapper_meltano_advanced.py is deprecated, use test_meltano_adapter_advanced.py instead",
    DeprecationWarning,
    stacklevel=2,
)
