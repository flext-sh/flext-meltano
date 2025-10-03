"""FLEXT Meltano Execution Result - Command execution result model.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from typing import override

from flext_core import FlextTypes, FlextUtilities


class FlextMeltanoExecutionResult:
    """Execution result model for Meltano command operations following flext-core patterns."""

    @override
    def __init__(
        self,
        command: FlextTypes.StringList,
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

    def to_dict(self) -> dict[str, str | int | float | bool | FlextTypes.StringList]:
        """Convert to dictionary representation.

        Returns:
            dict[str, str | int | float | bool | FlextTypes.StringList]: Dictionary representation of execution result.

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
