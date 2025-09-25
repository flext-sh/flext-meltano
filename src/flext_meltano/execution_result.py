"""FLEXT Meltano Execution Result - Command execution result model.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json

from flext_core import FlextUtilities


class FlextMeltanoExecutionResult:
    """Execution result model for Meltano command operations following flext-core patterns."""

    def __init__(
        self,
        command: list[str],
        *,
        success: bool,
        exit_code: int,
        output: str,
        error: str,
        execution_time: float,
    ) -> None:
        """Initialize execution result."""
        self.command = command
        self.success = success
        self.exit_code = exit_code
        self.output = output
        self.error = error
        self.execution_time = execution_time

    def to_dict(self: object) -> dict[str, str | int, float] | bool | list[str]:
        """Convert to dictionary representation.

        Returns:
            dict[str, str | int | float] | bool | list[str]: Dictionary representation of execution result.

        """
        return {
            "command": self.command,
            "success": self.success,
            "exit_code": self.exit_code,
            "output": self.output,
            "error": self.error,
            "execution_time": self.execution_time,
            "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
        }

    def to_json(self) -> str:
        """Convert to JSON representation.

        Returns:
            str: JSON string representation of execution result.

        """
        return json.dumps(self.to_dict())


__all__ = ["FlextMeltanoExecutionResult"]
