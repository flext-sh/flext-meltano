"""DBT Orchestration Service - Data transformation execution.

This module provides DBT orchestration with deep SDK integration,
FLEXT ecosystem patterns, and railway-oriented programming.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import TypeVar, override

from flext_core import r, s

from flext_meltano.dbt.project import FlextMeltanoDbtProjectManager
from flext_meltano.dbt.runner import FlextMeltanoDbtRunner
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes

t = FlextMeltanoTypes
m = FlextMeltanoModels
_ResultT = TypeVar("_ResultT")


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
                f"Documentation generation failed: {e}",
            )

    def get_project_models(self) -> r[list[t.Meltano.Dbt.ModelConfiguration]]:
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
            return r[list[t.Meltano.Dbt.ModelConfiguration]].fail(
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
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Failed to load DBT project", error=str(e))
            return r[m.Meltano.DbtProjectInfo].fail(f"Failed to load DBT project: {e}")

    def run_models(
        self,
        models: list[str] | None = None,
        **kwargs: t.Scalar,
    ) -> r[m.Meltano.DbtRunResult]:
        """Run DBT models.

        Args:
        models: Optional list of specific models to run
        **kwargs: Additional dbt run arguments

        Returns:
        r containing run result

        """

        def execute_operation() -> r[m.Meltano.DbtRunResult]:
            return self.runner.run_models(models, **kwargs)

        def log_success(result: m.Meltano.DbtRunResult) -> None:
            self.logger.info("DBT run completed", models_run=result.models_run)

        return self._run_dbt_operation(
            operation_name="models",
            failure_label="run",
            models=models,
            operation=execute_operation,
            success_logger=log_success,
        )

    def run_tests(
        self,
        models: list[str] | None = None,
        **kwargs: t.Scalar,
    ) -> r[m.Meltano.DbtTestResult]:
        """Run DBT tests.

        Args:
        models: Optional list of specific models to test
        **kwargs: Additional dbt test arguments

        Returns:
        r containing test result

        """

        def execute_operation() -> r[m.Meltano.DbtTestResult]:
            return self.runner.run_tests(models, **kwargs)

        def log_success(result: m.Meltano.DbtTestResult) -> None:
            self.logger.info("DBT tests completed", tests_run=result.tests_run)

        return self._run_dbt_operation(
            operation_name="tests",
            failure_label="tests",
            models=models,
            operation=execute_operation,
            success_logger=log_success,
        )

    def _run_dbt_operation(
        self,
        operation_name: str,
        failure_label: str,
        models: list[str] | None,
        operation: Callable[[], r[_ResultT]],
        success_logger: Callable[[_ResultT], None],
    ) -> r[_ResultT]:
        try:
            self.logger.info("Running DBT %s", operation_name, models=str(models or []))
            result = operation()
            if result.is_success:
                success_logger(result.value)
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
            self.logger.exception("DBT %s failed", failure_label, error=str(e))
            return r[_ResultT].fail(f"DBT {failure_label} failed: {e}")


__all__ = ["FlextMeltanoDbtService"]
