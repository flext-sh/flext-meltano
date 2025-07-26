"""Common utilities for flext-meltano.

Clean utilities using flext-core patterns.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_core import FlextCommonResult


def validate_file_path(path: str | Path | None) -> FlextCommonResult[Path]:
    """Validate file path.

    Args:
        path: File path to validate

    Returns:
        FlextCommonResult containing validated Path

    """
    if not path:
        return FlextCommonResult.fail("Path is required")

    try:
        path_obj = Path(path)
        if not path_obj.exists():
            return FlextCommonResult.fail(f"File does not exist: {path}")
        if not path_obj.is_file():
            return FlextCommonResult.fail(f"Path is not a file: {path}")
        return FlextCommonResult.ok(path_obj)
    except Exception as e:
        return FlextCommonResult.fail(f"Invalid file path: {e}")


def validate_directory_path(path: str | Path | None) -> FlextCommonResult[Path]:
    """Validate directory path.

    Args:
        path: Directory path to validate

    Returns:
        FlextCommonResult containing validated Path

    """
    if not path:
        return FlextCommonResult.fail("Path is required")

    try:
        path_obj = Path(path)
        if not path_obj.exists():
            return FlextCommonResult.fail(f"Directory does not exist: {path}")
        if not path_obj.is_dir():
            return FlextCommonResult.fail(f"Path is not a directory: {path}")
        return FlextCommonResult.ok(path_obj)
    except Exception as e:
        return FlextCommonResult.fail(f"Invalid directory path: {e}")


def ensure_directory(path: str | Path) -> FlextCommonResult[Path]:
    """Ensure directory exists.

    Args:
        path: Directory path to create

    Returns:
        FlextCommonResult containing created Path

    """
    try:
        path_obj = Path(path)
        path_obj.mkdir(parents=True, exist_ok=True)
        return FlextCommonResult.ok(path_obj)
    except Exception as e:
        return FlextCommonResult.fail(f"Failed to create directory: {e}")


def validate_meltano_project(project_root: str | Path) -> FlextCommonResult[Path]:
    """Validate Meltano project structure.

    Args:
        project_root: Project root directory

    Returns:
        FlextCommonResult containing validated project Path

    """
    try:
        project_path = Path(project_root)
        meltano_yml = project_path / "meltano.yml"

        if not project_path.exists():
            return FlextCommonResult.fail(
                f"Project directory does not exist: {project_root}",
            )
        if not meltano_yml.exists():
            return FlextCommonResult.fail(f"No meltano.yml found in: {project_root}")

        return FlextCommonResult.ok(project_path)
    except Exception as e:
        return FlextCommonResult.fail(f"Invalid Meltano project: {e}")


def validate_plugin_config(config: dict[str, Any]) -> FlextCommonResult[dict[str, Any]]:
    """Validate plugin configuration.

    Args:
        config: Plugin configuration to validate

    Returns:
        FlextCommonResult containing validated config

    """
    if not isinstance(config, dict):
        return FlextCommonResult.fail("Configuration must be a dictionary")

    if not config:
        return FlextCommonResult.fail("Configuration cannot be empty")

    return FlextCommonResult.ok(config)
