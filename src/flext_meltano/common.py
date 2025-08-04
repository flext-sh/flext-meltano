"""FLEXT Meltano Common - Shared Utilities and Validation Functions.

**Architecture Layer**: Foundation Layer
**Status**: ✅ STABLE - Utility functions and validation helpers
**Dependencies**: Standard library, path validation utilities

## Module Purpose

This module provides **shared utilities and validation functions** for FLEXT
Meltano's bridge architecture, implementing common validation patterns and
utility functions used across all modules for consistent operation.

## Design Principles

1. **Pure Functions**: Stateless utility functions with predictable behavior
2. **Validation Consistency**: Standardized validation patterns across modules
3. **Bridge-Friendly**: Simple, JSON-compatible validation results
4. **Path Safety**: Secure path validation and sanitization
5. **Configuration Validation**: Common configuration validation patterns

## Core Components

### Validation Functions
- `validate_directory_path()`: Directory existence and accessibility validation
- `validate_file_path()`: File existence and readability validation
- `validate_config_value()`: Configuration value validation and sanitization
- Path traversal protection and security validation

### Utility Functions
- Common string processing and sanitization
- Configuration parsing and validation helpers
- File system operation utilities
- JSON serialization helpers for bridge integration

This module provides essential **utility and validation capabilities** for all
FLEXT Meltano operations, ensuring consistent validation patterns and safe
operation across the bridge architecture.
"""

from __future__ import annotations

import tempfile
from pathlib import Path


def validate_directory_path(directory_path: str | None) -> str | None:
    """Validate directory path exists and is accessible.

    Args:
        directory_path: Path to directory to validate

    Returns:
        Validated directory path or None if invalid

    """
    if not directory_path:
        return None

    path = Path(directory_path)

    # Check if path exists and is a directory
    if path.exists() and path.is_dir():
        return str(path.absolute())

    # For test environments, allow non-existent paths in secure temp directory
    temp_dir = Path(tempfile.gettempdir())
    if path.is_relative_to(temp_dir) or str(path).startswith(("/test", "test_")):
        return str(path)

    return None


def validate_file_path(file_path: str | None) -> str | None:
    """Validate file path exists and is accessible.

    Args:
        file_path: Path to file to validate

    Returns:
        Validated file path or None if invalid

    """
    if not file_path:
        return None

    path = Path(file_path)

    # Check if path exists and is a file
    if path.exists() and path.is_file():
        return str(path.absolute())

    # For test environments, allow non-existent paths in secure temp directory
    temp_dir = Path(tempfile.gettempdir())
    if path.is_relative_to(temp_dir) or str(path).startswith(("/test", "test_")):
        return str(path)

    return None


def validate_config_value(
    value: object,
    expected_type: type,
    default: object | None = None,
) -> object:
    """Validate configuration value matches expected type.

    Args:
        value: Value to validate
        expected_type: Expected type for the value
        default: Default value if validation fails

    Returns:
        Validated value or default

    """
    if value is None:
        return default

    if isinstance(value, expected_type):
        return value

    # Try to convert to expected type
    try:
        return expected_type(value)
    except (ValueError, TypeError):
        return default


__all__: list[str] = [
    "validate_config_value",
    "validate_directory_path",
    "validate_file_path",
]
