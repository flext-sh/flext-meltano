"""DEPRECATED API module - Functionality moved to core.py.

This module is kept for backwards compatibility but all functionality
has been moved to core.py with proper FlextMeltano prefixes and real
integration with enterprise frameworks.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import warnings

# Re-export deprecated classes for backwards compatibility
from flext_meltano import (
    FlextMeltano,
    PipelineConfig,
    PipelineResult,
    async_run_pipeline,
    discover_catalog,
    run_pipeline,
    test_tap_connection,
)


def _deprecated_module_warning() -> None:
    """Issue deprecation warning for entire module."""
    warnings.warn(
        "flext_meltano.api module is deprecated. "
        "Use FlextMeltanoOrchestrationService from flext_meltano.core instead. "
        "All functionality has been moved to core.py with proper FlextMeltano prefixes.",
        DeprecationWarning,
        stacklevel=3,
    )

# Issue warning when module is imported
_deprecated_module_warning()

__all__ = [
    "FlextMeltano",
    "PipelineConfig",
    "PipelineResult",
    "async_run_pipeline",
    "discover_catalog",
    "run_pipeline",
    "test_tap_connection",
]
