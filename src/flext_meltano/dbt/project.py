"""FlextMeltano dbt Project Management.

dbt project management components following Clean Architecture patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult

if TYPE_CHECKING:
    from pathlib import Path


class FlextMeltanoDbtProject:
    """dbt project management for Meltano integration."""

    def __init__(self, project_path: Path) -> None:
        """Initialize dbt project manager."""
        self.project_path = project_path

    def validate_project(self) -> FlextResult[dict[str, Any]]:
        """Validate dbt project configuration."""
        try:
            dbt_project_file = self.project_path / "dbt_project.yml"
            if not dbt_project_file.exists():
                return FlextResult.fail("dbt_project.yml not found")

            return FlextResult.ok(
                {
                    "valid": True,
                    "project_path": str(self.project_path),
                    "config_file": str(dbt_project_file),
                },
            )

        except (OSError, ValueError) as e:
            return FlextResult.fail(f"Failed to validate dbt project: {e}")

    def get_models(self) -> FlextResult[list[str]]:
        """Get list of dbt models in the project."""
        try:
            models_path = self.project_path / "models"
            if not models_path.exists():
                return FlextResult.ok([])

            models = [sql_file.stem for sql_file in models_path.rglob("*.sql")]

            return FlextResult.ok(models)

        except (OSError, ValueError) as e:
            return FlextResult.fail(f"Failed to get dbt models: {e}")
