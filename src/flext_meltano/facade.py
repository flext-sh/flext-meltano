"""FLEXT Meltano Main Facade - Single Entry Point (Flext[Area][Module] pattern).

**Architecture Compliance**: Main facade class FlextMeltano following Flext[Area][Module] pattern
**NO IMPLEMENTATION**: This class only delegates to other specialized classes
**ZERO Duplication**: Pure delegation pattern - no actual implementation
**SOLID Principles**: Single point of access to all Meltano functionality

Main entry point providing access to all Meltano functionality through delegation only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Import all specialized classes for delegation
from .adapters import FlextMeltanoAdapters
from .config import FlextMeltanoConfig
from .executors import FlextMeltanoExecutors
from .utilities import FlextMeltanoUtilities

# =============================================================================
# MAIN FACADE CLASS - NO IMPLEMENTATION, ONLY DELEGATION
# =============================================================================


class FlextMeltano:
    """Main facade class for all FLEXT Meltano functionality (Flext[Area][Module] pattern).

    **ORCHESTRATION ONLY**: This class only orchestrates specialized classes.
    No implementation - delegates all functionality to specialized classes:

    - FlextMeltanoConfig: Configuration management
    - FlextMeltanoUtilities: Utility functions
    - FlextMeltanoAdapters: External service adapters
    - FlextMeltanoExecutors: Execution engines

    SOLID Principles:
    - Single Responsibility: Single entry point for all functionality
    - Open/Closed: Extensible through underlying specialized classes
    - Dependency Inversion: Delegates to abstractions, never implements
    """

    def __init__(self) -> None:
        """Initialize facade with orchestrated components."""
        # Orchestrate specialized classes (FLEXT pattern)
        self._config = FlextMeltanoConfig
        self._utilities = FlextMeltanoUtilities
        self._adapters = FlextMeltanoAdapters
        self._executors = FlextMeltanoExecutors

    # =================================================================
    # ORCHESTRATION METHODS - NO IMPLEMENTATION, ONLY DELEGATION
    # =================================================================

    @property
    def config(self) -> type[FlextMeltanoConfig]:
        """Access configuration management."""
        return self._config

    @property
    def utilities(self) -> type[FlextMeltanoUtilities]:
        """Access utility functions."""
        return self._utilities

    @property
    def adapters(self) -> type[FlextMeltanoAdapters]:
        """Access external service adapters."""
        return self._adapters

    @property
    def executors(self) -> type[FlextMeltanoExecutors]:
        """Access execution engines."""
        return self._executors

    # =================================================================
    # CONVENIENCE ALIASES - BACKWARD COMPATIBILITY
    # =================================================================

    # Class attributes for backward compatibility
    Config = FlextMeltanoConfig
    Utilities = FlextMeltanoUtilities
    Adapters = FlextMeltanoAdapters
    Executors = FlextMeltanoExecutors


# =============================================================================
# MODULE-LEVEL ALIASES FOR BACKWARD COMPATIBILITY
# =============================================================================

# Export specialized classes for direct usage
MeltanoConfig = FlextMeltanoConfig
MeltanoUtilities = FlextMeltanoUtilities
MeltanoAdapters = FlextMeltanoAdapters
MeltanoExecutors = FlextMeltanoExecutors


__all__ = [
    # Main facade class (entry point)
    "FlextMeltano",

    # Specialized classes (direct access)
    "MeltanoAdapters",
    "MeltanoConfig",
    "MeltanoExecutors",
    "MeltanoUtilities",
]
