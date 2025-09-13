"""FLEXT Meltano Executors Meltano - Backward compatibility executors.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import json
from typing import cast

from flext_core import FlextTypes

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.typings import FlextMeltanoTypes

# =================================================================
# BACKWARD COMPATIBILITY ALIASES - Simple aliases only
# =================================================================


# Simple aliases for backward compatibility - no duplication
# Use lazy imports to avoid circular dependencies
def _get_executor_class() -> type:
    """Lazy import to avoid circular dependency."""
    from flext_meltano.executors import FlextMeltanoExecutor  # noqa: PLC0415

    return FlextMeltanoExecutor


# Create aliases using lazy loading
MeltanoExecutor = _get_executor_class()
SimpleMeltanoExecutor = _get_executor_class()
SimpleDbtExecutor = _get_executor_class()


class FlextMeltanoExecutors:
    """Backward compatibility wrapper with simple aliases."""

    # Aliases for nested classes using lazy loading
    MeltanoExecutor = _get_executor_class()
    SimpleMeltanoExecutor = _get_executor_class()
    SimpleDbtExecutor = _get_executor_class()

    class ExecutionResult:
        """Execution result with structured data for Go integration."""

        def __init__(
            self,
            command: FlextTypes.Core.StringList,
            *,
            success: bool,
            output: str = "",
            error: str = "",
            exit_code: int = 0,
            execution_time: float = 0.0,
            metadata: FlextMeltanoTypes.CLI.ProcessResult | None = None,
        ) -> None:
            """Initialize execution result with command and outcome data."""
            self.success = success
            self.command = command
            self.output = output
            self.error = error
            self.exit_code = exit_code
            self.execution_time = execution_time
            self.metadata = metadata or {}
            self.timestamp = FlextMeltanoConstants.Meltano.VERSION_REQUIRED

        def to_dict(self) -> FlextMeltanoTypes.CLI.ProcessResult:
            """Convert to dictionary for JSON serialization."""
            return {
                "success": self.success,
                "command": cast("FlextTypes.Core.JsonValue", self.command),
                "output": self.output,
                "error": self.error,
                "exit_code": self.exit_code,
                "execution_time": self.execution_time,
                "metadata": cast("FlextTypes.Core.JsonValue", self.metadata),
                "timestamp": self.timestamp,
            }

        def to_json(self) -> str:
            """Convert to JSON string."""
            return json.dumps(self.to_dict())
