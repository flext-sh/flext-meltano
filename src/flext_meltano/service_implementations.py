"""FLEXT Meltano Service Implementations - Backward compatibility module.

DEPRECATED: This module is deprecated. Use flext_meltano.services instead.

This module provides backward compatibility for legacy code that expects
service_implementations module. All functionality has been moved to services.py
following flext-core single class per module patterns.

Migration Path:
    Old: from flext_meltano.service_implementations import FlextMeltanoTapService
    New: from flext_meltano.services import FlextMeltanoService
         # Access tap service as: FlextMeltanoService.TapService

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

from flext_meltano.services import (
    FlextMeltanoService,
)

# Create legacy class aliases
FlextMeltanoTapService = FlextMeltanoService.TapService
FlextMeltanoTargetService = FlextMeltanoService.TargetService
FlextMeltanoDbtService = FlextMeltanoService.DbtService

# Issue deprecation warning
warnings.warn(
    "service_implementations module is deprecated. Use flext_meltano.services instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Export legacy names for backward compatibility
__all__ = [
    "FlextMeltanoDbtService",
    "FlextMeltanoService",
    "FlextMeltanoTapService",
    "FlextMeltanoTargetService",
]
