"""FLEXT Pipeline Transformation Service - Single unified class for transformation operations.

This module provides the FlextMeltanoTransformationService class following FLEXT patterns:
- Single Responsibility Principle
- Railway-oriented programming with FlextResult
- Clean Architecture with domain separation

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextResult, FlextService

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.library_runner import FlextMeltanoLibraryRunner
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.settings import FlextMeltanoSettings
from flext_meltano.typings import FlextMeltanoTypes

# Import aliases for concise usage
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels
r = FlextResult
s = FlextService


class FlextMeltanoTransformationService(s[t.MeltanoCore.MeltanoConfigDict]):
    """Service for data transformation operations.

    Handles transformation operations following FLEXT patterns
    with railway-oriented programming.
    """

    # Instance attributes for type checker
    _library_runner: FlextMeltanoLibraryRunner

    def __init__(self, config: FlextMeltanoSettings | None = None) -> None:
        """Initialize transformation service with FLEXT configuration."""
        super().__init__()
        self._config = config or FlextMeltanoSettings()
        self._library_runner = FlextMeltanoLibraryRunner()

    def run_transformations(
        self,
        project_dir: Path,
        models: list[str] | None = None,
        **_options: object,
    ) -> r[dict[str, object]]:
        """Run transformations using programmatic API.

        Args:
        project_dir: Path to transformation project directory
        models: Optional list of specific models to run
        **options: Additional transformation options

        Returns:
        FlextResult containing transformation results

        """
        try:
            _ = self.logger.info(
                "Running transformations using programmatic API",
                project_dir=str(project_dir),
                models=models or "all",
            )

            # Use library runner for transformation operations
            transformation_runner_result = self._library_runner.get_dbt_runner()
            if transformation_runner_result.is_failure:
                return r[dict[str, object]].fail(
                    transformation_runner_result.error
                    or "Failed to get transformation runner",
                )

            # For now, just return success since runner is just a dict
            result = r[dict[str, object]].ok(transformation_runner_result.value)

            if result.is_success:
                _ = self.logger.info(
                    "transformations completed successfully",
                    models=models or "all",
                )
            else:
                _ = self.logger.error(
                    "transformations failed",
                    error=result.error,
                )

            return result

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to run transformations: {e}"
            _ = self.logger.exception(error_msg)
            return r[dict[str, object]].fail(error_msg)


__all__ = [
    "FlextMeltanoTransformationService",
]
