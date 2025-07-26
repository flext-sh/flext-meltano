"""Advanced helpers redirection - All functionality moved to core.py.

This module redirects to the new core.py implementation with proper
FlextMeltano prefixes and real enterprise framework integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

# Import and re-export from the main __init__ for backwards compatibility
from typing import Never

from flext_meltano import (
    BatchProcessor,
    MeltanoProject,
)


# Placeholder implementations for missing classes
class PipelineSpec:
    """Placeholder for legacy PipelineSpec."""


class PluginSpec:
    """Placeholder for legacy PluginSpec."""


def batch_process_tables(*args, **kwargs) -> Never:
    """Placeholder for legacy batch_process_tables."""
    msg = "batch_process_tables has been deprecated"
    raise NotImplementedError(msg)


def setup_project(*args, **kwargs) -> Never:
    """Placeholder for legacy setup_project."""
    msg = "setup_project has been deprecated"
    raise NotImplementedError(msg)


__all__ = [
    "BatchProcessor",
    "MeltanoProject",
    "PipelineSpec",
    "PluginSpec",
    "batch_process_tables",
    "setup_project",
]
