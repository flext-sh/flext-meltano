"""DEPRECATED advanced helpers module - Functionality moved to core.py.

This module is kept for backwards compatibility but all functionality
has been moved to core.py with proper FlextMeltano prefixes and real
integration with enterprise frameworks.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import warnings

# Re-export deprecated classes for backwards compatibility
from flext_meltano import (
    BatchProcessor,
    MeltanoProject,
    batch_process_tables,
    setup_project,
)


def _deprecated_module_warning() -> None:
    """Issue deprecation warning for entire module."""
    warnings.warn(
        "flext_meltano.helpers.advanced module is deprecated. "
        "Use FlextMeltanoOrchestrationService from flext_meltano.core instead. "
        "All functionality has been consolidated into core.py with proper enterprise patterns.",
        DeprecationWarning,
        stacklevel=3,
    )


# Issue warning when module is imported
_deprecated_module_warning()


# Deprecated dataclasses for specification
class PipelineSpec:
    """DEPRECATED: Use FlextMeltanoPipelineConfig instead."""

    def __init__(self, *_args: object, **_kwargs: object) -> None:
        """Initialize deprecated PipelineSpec class."""
        warnings.warn(
            "PipelineSpec is deprecated. Use FlextMeltanoPipelineConfig instead.",
            DeprecationWarning,
            stacklevel=2,
        )


class PluginSpec:
    """DEPRECATED: Use FlextMeltanoOrchestrationService instead."""

    def __init__(self, *_args: object, **_kwargs: object) -> None:
        """Initialize deprecated PluginSpec class."""
        warnings.warn(
            "PluginSpec is deprecated. Use FlextMeltanoOrchestrationService instead.",
            DeprecationWarning,
            stacklevel=2,
        )


__all__ = [
    "BatchProcessor",
    "MeltanoProject",
    "PipelineSpec",
    "PluginSpec",
    "batch_process_tables",
    "setup_project",
]
