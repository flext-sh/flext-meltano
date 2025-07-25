"""API redirection - All functionality moved to core.py.

This module redirects to the new core.py implementation with proper
FlextMeltano prefixes and real enterprise framework integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

# Import and re-export deprecated API for backwards compatibility
from flext_meltano.api_deprecated import (
    FlextMeltano,
    PipelineConfig,
    PipelineResult,
    async_run_pipeline,
    discover_catalog,
    run_pipeline,
    test_tap_connection,
)

__all__ = [
    "FlextMeltano",
    "PipelineConfig",
    "PipelineResult",
    "async_run_pipeline",
    "discover_catalog",
    "run_pipeline",
    "test_tap_connection",
]
