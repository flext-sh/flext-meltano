"""Common validation utilities shared across plugins."""

from __future__ import annotations

import os
from pathlib import Path


def validate_file_path(path: str | None) -> str | None:
    """Validate file path exists and is readable.

    Args:
        path: File path to validate

    Returns:
        Validated path or None if path is None

    Raises:
        ValueError: If path does not exist or is not a file

    """
    if path is None:
        return None

    file_path = Path(path)
    if not file_path.exists():
        msg = f"File does not exist: {path}"
        raise ValueError(msg)

    if not file_path.is_file():
        msg = f"Path is not a file: {path}"
        raise ValueError(msg)

    return str(file_path.resolve())


def validate_directory_path(path: str | None) -> str | None:
    """Validate directory path exists and is readable.

    Args:
        path: Directory path to validate

    Returns:
        Validated path or None if path is None

    Raises:
        ValueError: If path does not exist or is not a directory

    """
    if path is None:
        return None

    dir_path = Path(path)
    if not dir_path.exists():
        msg = f"Directory does not exist: {path}"
        raise ValueError(msg)

    if not dir_path.is_dir():
        msg = f"Path is not a directory: {path}"
        raise ValueError(msg)

    return str(dir_path.resolve())


def ensure_directory(path: str | Path) -> Path:
    """Ensure directory exists, creating if necessary.

    Args:
        path: Directory path to ensure

    Returns:
        Path object for the directory

    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_env_or_default(key: str, default: str = "") -> str:
    """Get environment variable with default fallback.

    Args:
        key: Environment variable name
        default: Default value if not set

    Returns:
        Environment variable value or default

    """
    return os.environ.get(key, default)
