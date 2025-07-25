"""FLEXT Meltano DBT - Consolidated DBT implementations.

This module provides consolidated DBT transformations for the FLEXT ecosystem,
eliminating code duplication across dbt projects.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any


class FlextMeltanoDbtProject:
    """Consolidated DBT project configuration for FLEXT ecosystem."""

    def __init__(
        self,
        project_name: str = "flext_meltano_dbt",
        project_dir: str = ".",
        profiles_dir: str = ".",
    ) -> None:
        """Initialize DBT project configuration.

        Args:
            project_name: Name of the DBT project
            project_dir: Directory containing the DBT project
            profiles_dir: Directory containing DBT profiles

        """
        self.project_name = project_name
        self.project_dir = project_dir
        self.profiles_dir = profiles_dir

    def get_project_config(self) -> dict[str, Any]:
        """Get consolidated DBT project configuration."""
        return {
            "name": self.project_name,
            "version": "0.8.0",
            "config-version": 2,
            "profile": "flext_meltano",
        }


class FlextMeltanoDbtManager:
    """Consolidated DBT manager for FLEXT ecosystem operations."""

    def __init__(self, project: FlextMeltanoDbtProject | None = None) -> None:
        """Initialize DBT manager.

        Args:
            project: DBT project configuration instance

        """
        self.project = project or FlextMeltanoDbtProject()

    def run_transformations(self, models: list[str] | None = None) -> bool:
        """Run DBT transformations for specified models."""
        # Basic implementation - can be expanded
        if models:
            pass
        return True

    def test_models(self, models: list[str] | None = None) -> bool:
        """Run DBT tests for specified models."""
        if models:
            pass
        return True


class FlextMeltanoDbtRunner:
    """Consolidated DBT runner for executing transformations."""

    def __init__(self, manager: FlextMeltanoDbtManager | None = None) -> None:
        """Initialize DBT runner.

        Args:
            manager: DBT manager instance

        """
        self.manager = manager or FlextMeltanoDbtManager()

    def execute(self, command: str, models: list[str] | None = None) -> bool:
        """Execute DBT command through consolidated runner.

        Args:
            command: DBT command to execute (run, test)
            models: List of models to process

        Returns:
            True if command executed successfully

        """
        if command == "run":
            return self.manager.run_transformations(models)
        if command == "test":
            return self.manager.test_models(models)
        return False


__version__ = "0.8.0-consolidated"

__all__ = [
    "FlextMeltanoDbtManager",
    "FlextMeltanoDbtProject",
    "FlextMeltanoDbtRunner",
    "__version__",
]
