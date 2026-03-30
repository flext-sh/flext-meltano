"""FLEXT Meltano Bridge - Go ↔ Python bridge communication.

This module provides the FlextMeltanoBridge class for JSON-based communication
between Go and Python components for Meltano operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import subprocess
from collections.abc import Mapping
from typing import override

from flext_core import r

from flext_meltano import FlextMeltanoServiceBase, t


class FlextMeltanoBridge(FlextMeltanoServiceBase):
    """Go Bridge - JSON API para integração Go ↔ Python.

    Provides JSON-based communication between Go and Python components
    for Meltano operations.
    """

    @staticmethod
    def discover_plugins() -> r[t.StrSequence]:
        """Discover installed Meltano plugins via CLI."""
        try:
            proc = subprocess.run(
                ["meltano", "list"],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            if proc.returncode != 0:
                return r[t.StrSequence].fail(f"meltano list failed: {proc.stderr}")
            plugins = [
                line.strip() for line in proc.stdout.splitlines() if line.strip()
            ]
            return r[t.StrSequence].ok(plugins)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            subprocess.TimeoutExpired,
        ) as e:
            return r[t.StrSequence].fail(f"Plugin discovery failed: {e}")

    @staticmethod
    def execute_bridge_command(
        command: str,
        args: t.ConfigurationMapping | None = None,
    ) -> r[t.Meltano.ExecutionResultDict]:
        """Execute a Meltano CLI command.

        Args:
            command: Command name to execute.
            args: Optional key-value arguments passed as --key=value flags.

        Returns:
            r with command execution results.

        """
        try:
            cmd = ["meltano", command]
            if args:
                cmd.extend(f"--{k}={v}" for k, v in args.items())
            proc = subprocess.run(
                cmd, capture_output=True, text=True, timeout=60, check=False
            )
            result: t.Meltano.ExecutionResultDict = {
                "command": command,
                "success": proc.returncode == 0,
                "output": proc.stdout,
                "error": proc.stderr,
            }
            return r[t.Meltano.ExecutionResultDict].ok(result)
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            subprocess.TimeoutExpired,
        ) as e:
            return r[t.Meltano.ExecutionResultDict].fail(f"Command failed: {e}")

    @staticmethod
    def get_version() -> r[str]:
        """Get Meltano version via CLI."""
        try:
            proc = subprocess.run(
                ["meltano", "version"],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if proc.returncode != 0:
                return r[str].fail(f"meltano version failed: {proc.stderr}")
            return r[str].ok(proc.stdout.strip())
        except (OSError, subprocess.TimeoutExpired) as e:
            return r[str].fail(f"Version check failed: {e}")

    @staticmethod
    def validate_connection() -> r[bool]:
        """Validate connection to Meltano CLI by running version check."""
        try:
            proc = subprocess.run(
                ["meltano", "version"],
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
            return r[bool].ok(proc.returncode == 0)
        except (OSError, subprocess.TimeoutExpired):
            return r[bool].ok(False)

    @override
    def execute(self) -> r[Mapping[str, t.NormalizedValue]]:
        """Execute bridge service returning current settings."""
        return r[Mapping[str, t.NormalizedValue]].ok(self.settings.model_dump())


__all__ = ["FlextMeltanoBridge"]
