"""FLEXT Meltano Project Validation Helpers.

Project validation utilities following Clean Architecture patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult

if TYPE_CHECKING:
    from pathlib import Path


def flext_meltano_validate_project(
    project_root: Path | None = None,
) -> FlextResult[dict[str, Any]]:
    """Validate Meltano project configuration and setup.

    Args:
        project_root: Meltano project root directory

    Returns:
        FlextResult with validation results

    """
    try:
        from pathlib import Path

        # Default to current directory if no project root specified
        root = project_root or Path.cwd()

        validation_results: dict[str, Any] = {
            "project_valid": True,
            "meltano_yml_exists": False,
            "plugins_installed": False,
            "issues": [],
        }

        # Check for meltano.yml file
        meltano_yml = root / "meltano.yml"
        if meltano_yml.exists():
            validation_results["meltano_yml_exists"] = True
        else:
            validation_results["project_valid"] = False
            validation_results["issues"].append(
                "meltano.yml file not found in project root",
            )

        # Check for .meltano directory (indicates initialized project)
        meltano_dir = root / ".meltano"
        if meltano_dir.exists():
            validation_results["plugins_installed"] = True
        else:
            validation_results["issues"].append(
                ".meltano directory not found - run 'meltano install'",
            )

        return FlextResult.ok(validation_results)

    except Exception as e:
        return FlextResult.fail(f"Project validation failed: {e}")
