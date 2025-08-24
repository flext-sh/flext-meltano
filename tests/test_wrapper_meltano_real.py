# FACADE: test_wrapper_meltano_real.py - Deprecated, use test_meltano_adapter_real.py
"""DEPRECATED: Use test_meltano_adapter_real.py instead.

This is a backward compatibility facade following CLAUDE.md Phase 3 strategy.
The original functionality has been moved to test_meltano_adapter_real.py
which follows PEP8 naming conventions.

Migration path:
- Update imports to use test_meltano_adapter_real
- This facade will be removed in future versions
"""

import warnings

from .test_meltano_adapter_real import *  # noqa: F403,F401

warnings.warn(
    "test_wrapper_meltano_real.py is deprecated, use test_meltano_adapter_real.py instead",
    DeprecationWarning,
    stacklevel=2,
)
