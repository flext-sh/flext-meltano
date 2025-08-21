"""Base Plugins - Plugin interfaces para projetos flext-*.

FUNÇÃO 3: Base plugin interfaces
- FlextTapPlugin: Interface para flext-tap-* projects
- FlextTargetPlugin: Interface para flext-target-* projects
- FlextDbtPlugin: Interface para flext-dbt-* projects
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from flext_core import FlextPlugin, FlextResult


class FlextTapPlugin(FlextPlugin, ABC):
    """Interface base para plugins flext-tap-*."""

    @abstractmethod
    def extract_data(self, config: dict[str, Any]) -> FlextResult[list[dict[str, Any]]]:
        """Extract data using tap-specific logic."""


class FlextTargetPlugin(FlextPlugin, ABC):
    """Interface base para plugins flext-target-*."""

    @abstractmethod
    def load_data(
        self, data: list[dict[str, Any]], config: dict[str, Any]
    ) -> FlextResult[bool]:
        """Load data using target-specific logic."""


class FlextDbtPlugin(FlextPlugin, ABC):
    """Interface base para plugins flext-dbt-*."""

    @abstractmethod
    def run_models(
        self, project_dir: Path, models: list[str] | None = None
    ) -> FlextResult[dict[str, Any]]:
        """Run DBT models with plugin-specific logic."""


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = ["FlextTapPlugin", "FlextTargetPlugin", "FlextDbtPlugin"]
