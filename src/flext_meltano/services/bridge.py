"""FLEXT Meltano Bridge - Go ↔ Python bridge communication.

This module provides the FlextMeltanoBridge class for JSON-based communication
between Go and Python components using the imported Meltano runtime.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_meltano import FlextMeltanoServiceBase, p, r, settings, t, u
from flext_meltano.services.executor_base import FlextMeltanoExecutorBase


class FlextMeltanoBridge(FlextMeltanoServiceBase):
    """Go Bridge - JSON API para integração Go ↔ Python.

    Provides JSON-based communication between Go and Python components
    for Meltano operations.
    """

    @staticmethod
    def discover_installed_plugins() -> p.Result[t.StrSequence]:
        """Discover installed Meltano plugins from the active project runtime."""
        executor = FlextMeltanoExecutorBase()
        plugins_result = executor.fetch_project_plugins()
        if plugins_result.failure:
            return r[t.StrSequence].fail(
                plugins_result.error or "Plugin discovery failed",
            )
        plugin_names = [
            p.get("name", "") for p in plugins_result.value if p.get("name")
        ]
        return r[t.StrSequence].ok(plugin_names)

    @staticmethod
    def execute_bridge_command(
        command: str,
        args: t.ConfigurationMapping | None = None,
    ) -> p.Result[t.JsonMapping]:
        """Execute a Meltano runtime command.

        Args:
            command: Command name to execute.
            args: Optional key-value arguments passed as --key=value flags.

        Returns:
            r with command execution results.

        """
        executor = FlextMeltanoExecutorBase()
        cmd = u.Meltano.build_bridge_command_args(command, args)
        command_result = executor.execute_meltano_command(cmd)
        if command_result.failure:
            return r[t.JsonMapping].fail(
                command_result.error or "Command failed",
            )
        command_execution = command_result.value
        result = u.Meltano.build_command_execution_payload(
            command_execution,
            extra_fields={"command": command},
            duration_field=None,
        )
        return r[t.JsonMapping].ok(result)

    @staticmethod
    def fetch_version() -> p.Result[str]:
        """Get Meltano version from the imported library."""
        return FlextMeltanoExecutorBase.fetch_version()

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute bridge service returning current settings."""
        return r[t.JsonMapping].ok(settings.model_dump(mode="json"))


__all__: list[str] = ["FlextMeltanoBridge"]
