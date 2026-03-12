"""DBT Orchestration Service - Data transformation execution.

This module provides DBT orchestration with deep SDK integration,
FLEXT ecosystem patterns, and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_core import r, s

from flext_meltano import FlextMeltanoModels, FlextMeltanoTypes
from flext_meltano.dbt.project import FlextMeltanoDbtProjectManager
from flext_meltano.dbt.runner import FlextMeltanoDbtRunner

t = FlextMeltanoTypes
m = FlextMeltanoModels


class FlextMeltanoDbtService(s[str]):
    """Orchestrates DBT transformations with deep SDK integration.

    Provides complete DBT orchestration including:
    - Project lifecycle management
    - Manifest and model discovery
    - Model execution and testing
    - Documentation generation
    - Error handling with r[T]

    This service integrates directly with dbt-core, providing a
    programmatic API for complete transformation operations.

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
        msg = "DBT service initialized"
        return r[str].ok(msg)

    def generate_docs(self, **kwargs: t.Scalar) -> r[t.Meltano.ExecutionResultDict]:
        """Generate DBT documentation.

        Args:
        **kwargs: Additional dbt docs arguments

        Returns:
        r containing documentation result

        """
        try:
            self.logger.info("Generating DBT documentation")
            result = self.runner.docs_generate(**kwargs)
            if result.is_success:
                self.logger.info("DBT documentation generated")
            return result
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("DBT documentation generation failed", error=str(e))
            return r[t.Meltano.ExecutionResultDict].fail(
                f"Documentation generation failed: {e}"
            )

    def get_project_models(self) -> r[list[t.Meltano.DbtModelDict]]:
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
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to get models", error=str(e))
            return r[list[t.Meltano.DbtModelDict]].fail(f"Failed to get models: {e}")

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
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to load DBT project", error=str(e))
            return r[m.Meltano.DbtProjectInfo].fail(f"Failed to load DBT project: {e}")

    def run_models(
        self, models: list[str] | None = None, **kwargs: t.Scalar
    ) -> r[m.Meltano.DbtRunResult]:
        """Run DBT models.

        Args:
        models: Optional list of specific models to run
        **kwargs: Additional dbt run arguments

        Returns:
        r containing run result

        """
        try:
            self.logger.info("Running DBT models", models=models)
            result = self.runner.run_models(models, **kwargs)
            if result.is_success:
                run_result = result.value
                self.logger.info("DBT run completed", models_run=run_result.models_run)
            return result
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("DBT run failed", error=str(e))
            return r[m.Meltano.DbtRunResult].fail(f"DBT run failed: {e}")

    def run_tests(
        self, models: list[str] | None = None, **kwargs: t.Scalar
    ) -> r[m.Meltano.DbtTestResult]:
        """Run DBT tests.

        Args:
        models: Optional list of specific models to test
        **kwargs: Additional dbt test arguments

        Returns:
        r containing test result

        """
        try:
            self.logger.info("Running DBT tests", models=models)
            result = self.runner.run_tests(models, **kwargs)
            if result.is_success:
                test_result = result.value
                self.logger.info("DBT tests completed", tests_run=test_result.tests_run)
            return result
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("DBT tests failed", error=str(e))
            return r[m.Meltano.DbtTestResult].fail(f"DBT tests failed: {e}")


__all__ = ["FlextMeltanoDbtService"]
