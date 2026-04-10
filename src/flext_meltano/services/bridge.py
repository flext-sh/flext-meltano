"""FLEXT Meltano Bridge - Go ↔ Python bridge communication.

This module provides the FlextMeltanoBridge class for JSON-based communication
between Go and Python components using the imported Meltano runtime.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import override

from flext_core import r
from flext_meltano.base import FlextMeltanoServiceBase
from flext_meltano.services._executor_base import FlextMeltanoExecutorBase
from flext_meltano.typings import FlextMeltanoTypes as t


class FlextMeltanoBridge(FlextMeltanoServiceBase):
    """Go Bridge - JSON API para integração Go ↔ Python.

    Provides JSON-based communication between Go and Python components
    for Meltano operations.
    """

    @staticmethod
    def discover_installed_plugins() -> r[t.StrSequence]:
        """Discover installed Meltano plugins from the active project runtime."""
        executor = FlextMeltanoExecutorBase()
        plugins_result = executor.get_project_plugins()
        if plugins_result.is_failure:
            return r[t.StrSequence].fail(
                plugins_result.error or "Plugin discovery failed",
            )
        plugin_names = [
            str(p.get("name", "")) for p in plugins_result.value if p.get("name")
        ]
        return r[t.StrSequence].ok(plugin_names)

    @staticmethod
    def execute_bridge_command(
        command: str,
        args: t.ConfigurationMapping | None = None,
    ) -> r[t.ContainerMapping]:
        """Execute a Meltano runtime command.

        Args:
            command: Command name to execute.
            args: Optional key-value arguments passed as --key=value flags.

        Returns:
            r with command execution results.

        """
        executor = FlextMeltanoExecutorBase()
        cmd = [command]
        if args:
            for k, v in args.items():
                cmd.append(f"--{k}={v}")
        command_result = executor.execute_meltano_command(cmd)
        if command_result.is_failure:
            return r[t.ContainerMapping].fail(
                command_result.error or "Command failed",
            )
        command_execution = command_result.value
        result: t.ContainerMapping = {
            "command": command,
            "output": command_execution.output,
            "error": command_execution.error,
        }
        return r[t.ContainerMapping].ok(result)

    @staticmethod
    def get_version() -> r[str]:
        """Get Meltano version from the imported library."""
        return FlextMeltanoExecutorBase.get_version()

    @override
    def execute(self) -> r[t.ContainerMapping]:
        """Execute bridge service returning current settings."""
        return r[t.ContainerMapping].ok(self.settings.model_dump())


__all__ = ["FlextMeltanoBridge"]
