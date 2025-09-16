"""FLEXT Meltano Simple Executors - Simplified executor compatibility wrappers.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from flext_core import FlextResult

from flext_meltano.typings import FlextMeltanoTypes

if TYPE_CHECKING:
    from flext_meltano.executors import FlextMeltanoExecutor


class FlextMeltanoSimpleExecutor:
    """Simple Meltano executor for test compatibility following flext-core patterns."""

    def __init__(self, project_root: Path | None = None, **kwargs: object) -> None:
        """Initialize simple executor with compatibility parameters."""
        # Import here to avoid circular imports
        from flext_meltano.executors import FlextMeltanoExecutor  # noqa: PLC0415

        # Store kwargs for potential future use in compatibility scenarios
        self._compatibility_kwargs = kwargs
        # Explicitly use kwargs to avoid Ruff ARG002 warning
        _ = kwargs
        self._main_executor: FlextMeltanoExecutor = FlextMeltanoExecutor(
            project_root=project_root
        )
        self.project_root = self._main_executor.project_root
        self.meltano_adapter = self._main_executor.meltano_adapter
        self.logger = self._main_executor.logger

    def run_command(self, command: list[str]) -> FlextResult[object]:
        """Run command delegation to main executor."""
        result = self._main_executor.run_command(command)
        if result.is_success:
            return FlextResult[object].ok(result.unwrap())
        return FlextResult[object].fail(result.error or "Unknown error")

    def execute(
        self, command: str | None = None
    ) -> FlextResult[FlextMeltanoTypes.CLI.ProcessResult]:
        """Execute command through main executor for compatibility."""
        return self._main_executor.execute(command)

    def get_project_info(self, project_path: Path | None = None) -> FlextResult[object]:
        """Get project info through main executor for compatibility."""
        if project_path is None:
            project_path = self.project_root or Path.cwd()
        result = self._main_executor.get_project_info(project_path)
        if result.is_success:
            return FlextResult[object].ok(result.unwrap())
        return FlextResult[object].fail(result.error or "Unknown error")

    def run_pipeline(self, tap_name: str, target_name: str) -> FlextResult[object]:
        """Run pipeline delegation to main executor."""
        result = self._main_executor.run_pipeline(tap_name, target_name)
        if result.is_success:
            return FlextResult[object].ok(result.unwrap())
        return FlextResult[object].fail(result.error or "Unknown error")

    def list_plugins(self) -> FlextResult[object]:
        """List plugins delegation to main executor."""
        result = self._main_executor.list_plugins()
        if result.is_success:
            return FlextResult[object].ok(result.unwrap())
        return FlextResult[object].fail(result.error or "Unknown error")


class FlextMeltanoSimpleDbtExecutor:
    """Simple DBT executor for test compatibility following flext-core patterns."""

    def __init__(self) -> None:
        """Initialize simple DBT executor."""
        # Import here to avoid circular imports
        from flext_meltano.executors import FlextMeltanoExecutor  # noqa: PLC0415

        self._main_executor: FlextMeltanoExecutor = FlextMeltanoExecutor()
        self.project_root = self._main_executor.project_root
        self.meltano_adapter = self._main_executor.meltano_adapter
        self.logger = self._main_executor.logger


# BACKWARD COMPATIBILITY ALIASES
MeltanoExecutor = FlextMeltanoSimpleExecutor  # For backward compatibility with tests
SimpleMeltanoExecutor = FlextMeltanoSimpleExecutor
SimpleDbtExecutor = FlextMeltanoSimpleDbtExecutor


__all__ = [
    "FlextMeltanoSimpleDbtExecutor",
    "FlextMeltanoSimpleExecutor",
    "MeltanoExecutor",  # Backward compatibility
    "SimpleDbtExecutor",  # Backward compatibility
    "SimpleMeltanoExecutor",  # Backward compatibility
]
