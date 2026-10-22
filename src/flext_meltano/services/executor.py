"""FLEXT Meltano Executor - CLI status and health operations.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import c, p, r, t
from flext_meltano.services.executor_base import FlextMeltanoExecutorBase


class FlextMeltanoExecutor(FlextMeltanoExecutorBase):
    """Core executor providing Meltano command execution with error handling."""

    def health(self) -> p.Result[t.JsonMapping]:
        """Check system health by running meltano invoke.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        result = self.execute_meltano_command([c.Meltano.ExecutorCommand.VERSION])
        return result.map(
            lambda cmd_result: {
                "status": c.Meltano.OperationStatus.HEALTHY
                if cmd_result.success
                else c.Meltano.OperationStatus.ERROR,
                "command": "health",
                "command_type": "health",
                "health": "OK" if cmd_result.success else "DEGRADED",
                "exit_code": cmd_result.exit_code,
            },
        )

    @staticmethod
    def run_cli() -> p.Result[t.JsonMapping]:
        """Report the CLI readiness status payload.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        ready_payload: t.JsonMapping = {
            "status": c.Meltano.OperationStatus.READY,
            "command_type": "cli",
            "message": "CLI ready for commands",
        }
        return r[t.JsonMapping].ok(ready_payload)


__all__: list[str] = ["FlextMeltanoExecutor"]
