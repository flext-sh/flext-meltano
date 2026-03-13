"""FLEXT Meltano Execution Result - Model for command execution results.

This module provides the FlextMeltanoExecutionResult class for representing
Meltano command execution outcomes following flext-core patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Annotated

from flext_core import FlextModels, t
from pydantic import Field, computed_field

from flext_meltano import u


class FlextMeltanoExecutionResult(FlextModels.ArbitraryTypesModel):
    """Execution result model for Meltano command operations following flext-core patterns."""

    command: Annotated[list[str], Field(description="Command that was executed")]
    success: Annotated[bool, Field(description="Whether the command succeeded")]
    exit_code: Annotated[int, Field(description="Process exit code")]
    output: Annotated[str, Field(description="Standard output")]
    error: Annotated[str, Field(description="Standard error")]
    execution_time: Annotated[float, Field(description="Execution time in seconds")]

    @computed_field
    def timestamp(self) -> str:
        """ISO timestamp of when the result was generated."""
        return u.generate_iso_timestamp()

    def to_dict(self) -> Mapping[str, t.Scalar | list[str]]:
        """Convert to dictionary representation.

        Returns:
        Mapping[str, str | int | float | bool | list[str]]: Dictionary representation of execution result.

        """
        dumped: dict[str, t.Scalar | list[str]] = {}
        dumped["command"] = self.command
        dumped["success"] = self.success
        dumped["exit_code"] = self.exit_code
        dumped["output"] = self.output
        dumped["error"] = self.error
        dumped["execution_time"] = self.execution_time
        dumped["timestamp"] = u.generate_iso_timestamp()
        return dumped


__all__ = ["FlextMeltanoExecutionResult"]
