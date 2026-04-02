"""FLEXT Meltano Bridge - Go ↔ Python bridge communication.

This module provides the FlextMeltanoBridge class for JSON-based communication
between Go and Python components using the imported Meltano runtime.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from typing import override

from flext_core import r
from flext_meltano import FlextMeltanoExecutorBase, FlextMeltanoServiceBase, t, u


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
        plugin_names = u.Meltano.extract_plugin_names(plugins_result.value)
        return r[t.StrSequence].ok(plugin_names)

    @staticmethod
    def execute_bridge_command(
        command: str,
        args: t.ConfigurationMapping | None = None,
    ) -> r[t.Meltano.ExecutionResultDict]:
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
        if command_result.is_failure:
            return r[t.Meltano.ExecutionResultDict].fail(
                command_result.error or "Command failed",
            )
        command_execution = command_result.value
        result: t.Meltano.ExecutionResultDict = (
            u.Meltano.build_command_execution_payload(
                command_execution,
                extra_fields={"command": command},
                status_field=None,
                duration_field=None,
            )
        )
        return r[t.Meltano.ExecutionResultDict].ok(result)

    @staticmethod
    def get_version() -> r[str]:
        """Get Meltano version from the imported library."""
        return FlextMeltanoExecutorBase.get_version()

    @override
    def execute(self) -> r[Mapping[str, t.NormalizedValue]]:
        """Execute bridge service returning current settings."""
        return r[Mapping[str, t.NormalizedValue]].ok(
            u.Meltano.coerce_config_mapping(self.settings)
        )


__all__ = ["FlextMeltanoBridge"]
