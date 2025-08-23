"""Base Plugins - Plugin interfaces para projetos flext-*.

FUNÇÃO 3: Base plugin interfaces
- FlextTapPlugin: Interface para flext-tap-* projects
- FlextTargetPlugin: Interface para flext-target-* projects
- FlextDbtPlugin: Interface para flext-dbt-* projects
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

# Removed typing.Any - using specific types
from flext_core import FlextResult


class FlextTapPlugin(ABC):
    """Interface base para plugins flext-tap-*."""

    @abstractmethod
    def extract_data(self, config: dict[str, object]) -> FlextResult[list[dict[str, object]]]:
        """Extract data using tap-specific logic."""


class FlextTargetPlugin(ABC):
    """Interface base para plugins flext-target-*."""

    @abstractmethod
    def load_data(
        self, data: list[dict[str, object]], config: dict[str, object]
    ) -> FlextResult[bool]:
        """Load data using target-specific logic."""


class FlextDbtPlugin(ABC):
    """Interface base para plugins flext-dbt-*."""

    @abstractmethod
    def run_models(
        self, project_dir: Path, models: list[str] | None = None
    ) -> FlextResult[dict[str, object]]:
        """Run DBT models with plugin-specific logic."""


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = ["FlextDbtPlugin", "FlextTapPlugin", "FlextTargetPlugin"]
