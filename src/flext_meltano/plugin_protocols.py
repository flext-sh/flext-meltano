"""Meltano Plugin Protocols - Single class following Flext[Area][Module] pattern.

✅ ARCHITECTURAL COMPLIANCE: Single main class FlextMeltanoProtocols
FUNCTION 3: Plugin protocol definitions aggregated into single facade class
Following user requirements: "apenas uma classe Flext[Area][Modulo]"

The main class FlextMeltanoProtocols serves as the facade providing access to all
plugin protocol definitions through internal nested classes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from flext_core import (
    FlextProtocols,
    FlextResult,
)


class FlextMeltanoProtocols:
    """Single main class providing all Meltano plugin protocols (Flext[Area][Module] pattern).

    Following FLEXT architectural standards: Single class per module that provides all functionality
    as nested classes or aliases. This class serves as the facade for all plugin protocol definitions
    used throughout the Meltano ecosystem.

    Design Pattern:
    - Main class provides access to all plugin protocols
    - Internal nested protocol classes maintain functionality
    - Everything is accessible through the main FlextMeltanoProtocols interface
    - Maintains backward compatibility through class attributes
    """

    @runtime_checkable
    class TapPlugin(FlextProtocols.Extensions.Plugin, Protocol):
        """Protocol for flext-tap-* plugins using flext-core patterns."""

        def extract_data(
            self, config: dict[str, object]
        ) -> FlextResult[list[dict[str, object]]]:
            """Extract data using tap-specific logic."""
            ...

    @runtime_checkable
    class TargetPlugin(FlextProtocols.Extensions.Plugin, Protocol):
        """Protocol for flext-target-* plugins using flext-core patterns."""

        def load_data(
            self, data: list[dict[str, object]], config: dict[str, object]
        ) -> FlextResult[bool]:
            """Load data using target-specific logic."""
            ...

    @runtime_checkable
    class DbtPlugin(FlextProtocols.Extensions.Plugin, Protocol):
        """Protocol for flext-dbt-* plugins using flext-core patterns."""

        def run_models(
            self, project_dir: Path, models: list[str] | None = None
        ) -> FlextResult[dict[str, object]]:
            """Run DBT models with plugin-specific logic."""
            ...

    # Aliases for backward compatibility
    FlextTapPlugin = TapPlugin
    FlextTargetPlugin = TargetPlugin
    FlextDbtPlugin = DbtPlugin


# =============================================================================
# BACKWARD COMPATIBILITY ALIASES
# =============================================================================

# Maintain existing API for backward compatibility
_protocols = FlextMeltanoProtocols()
FlextTapPlugin = FlextMeltanoProtocols.TapPlugin
FlextTargetPlugin = FlextMeltanoProtocols.TargetPlugin
FlextDbtPlugin = FlextMeltanoProtocols.DbtPlugin

# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "FlextDbtPlugin",  # Backward compatibility
    "FlextMeltanoProtocols",  # Main class
    "FlextTapPlugin",  # Backward compatibility
    "FlextTargetPlugin",  # Backward compatibility
]
