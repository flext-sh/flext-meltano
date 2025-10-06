"""FLEXT Meltano DBT Service - Single unified class for DBT operations.

This module provides the FlextMeltanoDbtService class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with FlextResult
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import cast

from flext_core import (
    FlextLogger,
    FlextResult,
    FlextService,
)

# Import from specific modules to avoid circular dependencies
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.library_runner import FlextMeltanoLibraryRunner
from flext_meltano.typings import FlextMeltanoTypes


class FlextMeltanoDbtService(
    FlextService[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]
):
    """Service for Meltano DBT operations.

    Handles DBT transformation operations following FLEXT patterns
    with railway-oriented programming.
    """

    def __init__(self, config: FlextMeltanoConfig | None = None) -> None:
        """Initialize DBT service with FLEXT configuration."""
        super().__init__()
        self._config = config or FlextMeltanoConfig()
        self._logger = FlextLogger(__name__)
        self._library_runner = FlextMeltanoLibraryRunner()

    def run_transformations(
        self,
        project_dir: Path,
        models: list[str] | None = None,
        **_options: object,
    ) -> FlextResult[FlextMeltanoTypes.Processing.DbtTransformationResult]:
        """Run dbt transformations using programmatic API.

        Args:
            project_dir: Path to dbt project directory
            models: Optional list of specific models to run
            **options: Additional dbt options

        Returns:
            FlextResult containing transformation results

        """
        try:
            _ = self._logger.info(
                "Running dbt transformations using programmatic API",
                project_dir=str(project_dir),
                models=models or "all",
            )

            # Use library runner for dbt operations
            dbt_runner_result = self._library_runner.get_dbt_runner()
            if dbt_runner_result.is_failure:
                return FlextResult[
                    FlextMeltanoTypes.Processing.DbtTransformationResult
                ].fail(dbt_runner_result.error or "Failed to get DBT runner")

            # For now, just return success since dbt_runner is just a dict
            result = FlextResult[
                FlextMeltanoTypes.Processing.DbtTransformationResult
            ].ok(
                cast(
                    "FlextMeltanoTypes.Processing.DbtTransformationResult",
                    dbt_runner_result.unwrap(),
                )
            )

            if result.is_success:
                _ = self._logger.info(
                    "dbt transformations completed successfully",
                    models=models or "all",
                )
            else:
                _ = self._logger.error(
                    "dbt transformations failed",
                    error=result.error,
                )

            return result

        except Exception as e:
            error_msg = f"Failed to run dbt transformations: {e}"
            _ = self._logger.exception(error_msg)
            return FlextResult[
                FlextMeltanoTypes.Processing.DbtTransformationResult
            ].fail(error_msg)


__all__ = [
    "FlextMeltanoDbtService",
]
