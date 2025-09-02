"""FLEXT Meltano Adapters - Backward compatibility module.

DEPRECATED: This module is deprecated. Use specific modules instead.

This module provides backward compatibility for legacy code that expects
meltano_adapters module. All functionality has been moved to appropriate modules
following flext-core single class per module patterns.

Migration Path:
    Old: from flext_meltano.meltano_adapters import FlextMeltanoAdapter
    New: from flext_meltano.adapters import FlextMeltanoAdapter

    Old: from flext_meltano.meltano_adapters import MeltanoBridge
    New: from flext_meltano.executors_bridge import FlextMeltanoBridge

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

# Import from correct modules for backward compatibility
from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.executors_bridge import FlextMeltanoBridge

# Legacy aliases for backward compatibility
MeltanoBridge = FlextMeltanoBridge

# Issue deprecation warning
warnings.warn(
    "meltano_adapters module is deprecated. Use flext_meltano.adapters and flext_meltano.executors_bridge instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Export legacy names for backward compatibility
__all__ = [
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "MeltanoBridge",
]
