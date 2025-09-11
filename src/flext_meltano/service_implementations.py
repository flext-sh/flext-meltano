"""FLEXT Meltano Service Implementations - Backward compatibility module.

DEPRECATED: This module is deprecated. Use flext_meltano.services instead.

This module provides backward compatibility for legacy code that expects
service_implementations module. All functionality has been moved to services.py
following flext-core single class per module patterns.

Migration Path:
    Old: from flext_meltano.service_implementations import FlextMeltanoTapService
    New: from flext_meltano.services import FlextMeltanoService

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings

# Create legacy class aliases using partial with service_type
from functools import partial

from flext_meltano.services import FlextMeltanoService


def _create_service_with_type(
    service_type: str, name: str, **kwargs: object
) -> FlextMeltanoService:
    """Create service with specific type."""
    return FlextMeltanoService(
        service_type=service_type, **{f"{service_type}_name": name}, **kwargs
    )


# Legacy compatibility classes
FlextMeltanoTapService = partial(_create_service_with_type, "tap")
FlextMeltanoTargetService = partial(_create_service_with_type, "target")
FlextMeltanoDbtService = partial(_create_service_with_type, "dbt")

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
