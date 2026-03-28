"""DBT Orchestration Service - Data transformation execution.

This module provides DBT orchestration with FLEXT ecosystem
patterns and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import override

from flext_core import r, s

from flext_meltano import (
    FlextMeltanoDbtProjectManager,
    FlextMeltanoDbtRunner,
    m,
    t,
)


class FlextMeltanoDbtService(s[str]):
    """Orchestrates DBT transformations.

    Provides project lifecycle management, manifest/model discovery,
    and delegates execution to FlextMeltanoDbtRunner.

    Attributes:
    project_manager: Manages DBT projects
    runner: Executes DBT commands

    """

    def __init__(self) -> None:
        """Initialize DBT orchestration service."""
        super().__init__()
        self.project_manager = FlextMeltanoDbtProjectManager()
        self.runner = FlextMeltanoDbtRunner()

    @override
    def execute(self) -> r[str]:
        """Execute (implements Service pattern)."""
        return r[str].ok("DBT service initialized")

    def generate_docs(self, **kwargs: t.Scalar) -> None:
        """Generate DBT documentation.

        Raises:
        NotImplementedError: Delegates to runner which is not yet implemented.

        """
        self.runner.docs_generate(**kwargs)

    def get_project_models(self) -> r[Sequence[t.Meltano.Dbt.ModelConfiguration]]:
        """Get all models from the project.

        Returns:
        r containing list of models

        """
        try:
            self.logger.info("Retrieving DBT models")
            result = self.project_manager.get_models()
            if result.is_success:
                models = result.value
                self.logger.info("DBT models retrieved", count=len(models))
            return result
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
        ) as e:
            self.logger.exception("Failed to get models", error=str(e))
            return r[Sequence[t.Meltano.Dbt.ModelConfiguration]].fail(
                f"Failed to get models: {e}",
            )

    def load_project(self, root: Path) -> r[m.Meltano.DbtProjectInfo]:
        """Load a DBT project.

        Args:
        root: Root directory of DBT project

        Returns:
        r containing project information

        """
        try:
            self.logger.info("Loading DBT project", root=str(root))
            result = self.project_manager.load_project(root)
            if result.is_success:
                self.runner.project_root = root
                self.logger.info("DBT project loaded")
            return result
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
        ) as e:
            self.logger.exception("Failed to load DBT project", error=str(e))
            return r[m.Meltano.DbtProjectInfo].fail(f"Failed to load DBT project: {e}")

    def run_models(
        self,
        models: t.StrSequence | None = None,
        **kwargs: t.Scalar,
    ) -> None:
        """Run DBT models.

        Raises:
        NotImplementedError: Delegates to runner which is not yet implemented.

        """
        self.runner.run_models(models, **kwargs)

    def run_tests(
        self,
        models: t.StrSequence | None = None,
        **kwargs: t.Scalar,
    ) -> None:
        """Run DBT tests.

        Raises:
        NotImplementedError: Delegates to runner which is not yet implemented.

        """
        self.runner.run_tests(models, **kwargs)


__all__ = ["FlextMeltanoDbtService"]
