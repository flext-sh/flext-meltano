"""Meltano SDK for FLEXT.

This module provides a high-level SDK for interacting with Meltano,
including custom exception classes for better error handling.
"""

from __future__ import annotations


class FlextMeltanoError(Exception):
    """MeltanoError - Custom Exception for Meltano operations.

    Base exception class for Meltano-related errors.
    Implements custom exception for domain-specific cases.
    Provides detailed error information.

    Attributes
    ----------
    message : str
        Error message describing the issue.

    Examples
    --------
    Typical usage:

    ```python
    raise MeltanoError("Meltano project not found")
    ```

    See Also
    --------
    Exception : Base exception class.

    """


class FlextMeltanoProjectError(FlextMeltanoError):
    """Raised for errors related to Meltano project management."""


class FlextMeltanoExecutionError(FlextMeltanoError):
    """Raised for errors during Meltano command execution."""

    def __init__(
        self,
        message: str,
        command: list[str] | None = None,
        returncode: int | None = None,
        stdout: str | None = None,
        stderr: str | None = None,
    ) -> None:
        """Initialize MeltanoExecutionError with execution details."""
        super().__init__(message)
        self.command = command
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


class FlextMeltanoPluginError(FlextMeltanoError):
    """Raised for errors related to Meltano plugin operations."""


class FlextMeltanoStateError(FlextMeltanoError):
    """Raised for errors related to Meltano state management."""


class FlextMeltanoConfigError(FlextMeltanoError):
    """Raised for errors related to Meltano configuration."""
