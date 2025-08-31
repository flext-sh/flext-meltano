"""FLEXT Meltano DBT Adapters - Backward compatibility module.

DEPRECATED: This module is deprecated. Use specific modules instead.

This module provides backward compatibility for legacy code that expects
dbt_adapters module. All functionality has been moved to appropriate modules
following flext-core single class per module patterns.

Migration Path:
    Old: from flext_meltano.dbt_adapters import FlextDbtAdapter
    New: from flext_meltano.adapters import FlextMeltanoAdapter

    Old: from flext_meltano.dbt_adapters import MeltanoDbtWrapper
    New: from flext_meltano.wrappers import FlextMeltanoWrapper.DbtWrapper

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

# Import from correct modules for backward compatibility
from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.wrappers import FlextMeltanoWrapper

# Legacy aliases for backward compatibility
FlextDbtAdapter = FlextMeltanoAdapter
MeltanoDbtWrapper = FlextMeltanoWrapper.DbtWrapper

# Issue deprecation warning
warnings.warn(
    "dbt_adapters module is deprecated. Use flext_meltano.adapters and flext_meltano.wrappers instead.",
    DeprecationWarning,
    stacklevel=2
)

# Export legacy names for backward compatibility
__all__ = [
    "FlextDbtAdapter",
    "FlextMeltanoAdapter",
    "FlextMeltanoWrapper",
    "MeltanoDbtWrapper",
]
