"""Advanced helpers redirection - All functionality moved to core.py.

This module redirects to the new core.py implementation with proper
FlextMeltano prefixes and real enterprise framework integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

# Import and re-export deprecated API for backwards compatibility
from flext_meltano.helpers.advanced_deprecated import (
    BatchProcessor,
    MeltanoProject,
    PipelineSpec,
    PluginSpec,
    batch_process_tables,
    setup_project,
)

__all__ = [
    "BatchProcessor",
    "MeltanoProject",
    "PipelineSpec",
    "PluginSpec",
    "batch_process_tables",
    "setup_project",
]
