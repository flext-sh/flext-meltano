"""DBT Orchestration Service - Data transformation execution.

This module provides DBT orchestration with deep SDK integration,
FLEXT ecosystem patterns, and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextResult, FlextService

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.dbt.project import FlextMeltanoDbtProjectManager
from flext_meltano.dbt.runner import FlextMeltanoDbtRunner
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases for simplified usage
# u is already imported from flext_core
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels
p = FlextMeltanoProtocols


class FlextMeltanoDbtService(FlextService):
    """Orchestrates DBT transformations with deep SDK integration.

    Provides complete DBT orchestration including:
    - Project lifecycle management
    - Manifest and model discovery
    - Model execution and testing
    - Documentation generation
    - Error handling with FlextResult[T]

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

    def load_project(
        self,
        root: Path,
    ) -> FlextResult[FlextMeltanoDbtProjectManager.ProjectInfo]:
        """Load a DBT project.

        Args:
        root: Root directory of DBT project

        Returns:
        FlextResult containing project information

        """
        try:
            self.logger.info("Loading DBT project", root=str(root))
            result = self.project_manager.load_project(root)
            if result.is_success:
                self.runner.project_root = root
                self.logger.info("DBT project loaded")
            return result
        except Exception as e:
            self.logger.exception("Failed to load DBT project", error=str(e))
            return FlextResult[FlextMeltanoDbtProjectManager.ProjectInfo].fail(
                f"Failed to load DBT project: {e}",
            )

    def get_project_models(
        self,
    ) -> FlextResult[list[dict[str, object]]]:
        """Get all models from the project.

        Returns:
        FlextResult containing list of models

        """
        try:
            self.logger.info("Retrieving DBT models")
            result = self.project_manager.get_models()
            if result.is_success:
                models = result.unwrap()
                self.logger.info("DBT models retrieved", count=len(models))
            return result
        except Exception as e:
            self.logger.exception("Failed to get models", error=str(e))
            return FlextResult[list[dict[str, object]]].fail(
                f"Failed to get models: {e}",
            )

    def run_models(
        self,
        models: list[str] | None = None,
        **kwargs: object,
    ) -> FlextResult[FlextMeltanoDbtRunner.RunResult]:
        """Run DBT models.

        Args:
        models: Optional list of specific models to run
        **kwargs: Additional dbt run arguments

        Returns:
        FlextResult containing run result

        """
        try:
            self.logger.info("Running DBT models", models=models)
            result = self.runner.run_models(models, **kwargs)
            if result.is_success:
                run_result = result.unwrap()
                self.logger.info(
                    "DBT run completed",
                    models_run=run_result.models_run,
                )
            return result
        except Exception as e:
            self.logger.exception("DBT run failed", error=str(e))
            return FlextResult[FlextMeltanoDbtRunner.RunResult].fail(
                f"DBT run failed: {e}",
            )

    def run_tests(
        self,
        models: list[str] | None = None,
        **kwargs: object,
    ) -> FlextResult[FlextMeltanoDbtRunner.TestResult]:
        """Run DBT tests.

        Args:
        models: Optional list of specific models to test
        **kwargs: Additional dbt test arguments

        Returns:
        FlextResult containing test result

        """
        try:
            self.logger.info("Running DBT tests", models=models)
            result = self.runner.run_tests(models, **kwargs)
            if result.is_success:
                test_result = result.unwrap()
                self.logger.info(
                    "DBT tests completed",
                    tests_run=test_result.tests_run,
                )
            return result
        except Exception as e:
            self.logger.exception("DBT tests failed", error=str(e))
            return FlextResult[FlextMeltanoDbtRunner.TestResult].fail(
                f"DBT tests failed: {e}",
            )

    def generate_docs(self, **kwargs: object) -> FlextResult[dict[str, object]]:
        """Generate DBT documentation.

        Args:
        **kwargs: Additional dbt docs arguments

        Returns:
        FlextResult containing documentation result

        """
        try:
            self.logger.info("Generating DBT documentation")
            result = self.runner.docs_generate(**kwargs)
            if result.is_success:
                self.logger.info("DBT documentation generated")
            return result
        except Exception as e:
            self.logger.exception("DBT documentation generation failed", error=str(e))
            return FlextResult[dict[str, object]].fail(
                f"Documentation generation failed: {e}",
            )

    @staticmethod
    def execute() -> FlextResult[str]:
        """Execute (implements Domain.Service pattern)."""
        msg = "DBT service initialized"
        return FlextResult[str].ok(msg)


__all__ = [
    "FlextMeltanoDbtService",
]
