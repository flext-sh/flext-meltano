"""FLEXT Meltano Executors CLI - Backward compatibility module.

This module provides backward compatibility for legacy code that expects
executors_cli module. All functionality has been moved to executors.py
following flext-core single class per module patterns.

Migration Path:
    Old: from flext_meltano.executors_cli import FlextMeltanoCli
    New: from flext_meltano.executors import FlextMeltanoExecutor

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

from flext_meltano.executors import FlextMeltanoExecutor

# Create backward compatibility aliases
FlextMeltanoCli = FlextMeltanoExecutor
flext_meltano_run_cli = FlextMeltanoExecutor.create_cli_runner

# Issue deprecation warning
warnings.warn(
    "executors_cli module is deprecated. Use flext_meltano.executors instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Export legacy names for backward compatibility
__all__ = [
    "FlextMeltanoCli",
    "flext_meltano_run_cli",
]
