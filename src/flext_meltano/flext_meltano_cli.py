"""FLEXT Meltano CLI - Command line interface using flext-core patterns.

CLI interface for FLEXT Meltano operations using FlextDomainService composition.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from flext_core import FlextDomainService, FlextResult


class FlextMeltanoCli(FlextDomainService):
    """CLI interface for FLEXT Meltano using flext-core patterns."""

    def __init__(self, project_root: Path = Path.cwd()) -> None:
        """Initialize CLI with project root."""
        super().__init__()
        self.project_root = project_root

    def execute(self) -> FlextResult[dict[str, Any]]:
        """Execute CLI operations using flext-core patterns."""
        return FlextResult(data={
            "cli_type": "flext_meltano",
            "project_root": str(self.project_root),
        })

    def flext_meltano_run_command(self, args: list[str]) -> FlextResult[dict[str, Any]]:
        """Run meltano command with arguments."""
        try:
            # Build command
            cmd = ["meltano", *args]

            # Execute command
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )

            output = {
                "command": " ".join(cmd),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            }

            if result.returncode == 0:
                return FlextResult(data=output)
            return FlextResult(
                error=f"Command failed: {result.stderr or result.stdout}",
                error_data=output,
            )

        except subprocess.TimeoutExpired:
            return FlextResult(error="Command timed out")
        except Exception as e:
            return FlextResult(error=f"Command error: {e}")

    def flext_meltano_version(self) -> FlextResult[str]:
        """Get meltano version."""
        result = self.flext_meltano_run_command(["--version"])
        if result.is_success:
            version = result.data["stdout"].strip() if result.data else "unknown"
            return FlextResult(data=version)
        return FlextResult(error=result.error)

    def flext_meltano_install(self) -> FlextResult[bool]:
        """Install meltano project dependencies."""
        result = self.flext_meltano_run_command(["install"])
        return FlextResult(data=result.is_success)

    def flext_meltano_invoke(self, plugin_name: str, *args: str) -> FlextResult[dict[str, Any]]:
        """Invoke specific plugin with arguments."""
        cmd_args = ["invoke", plugin_name, *args]
        return self.flext_meltano_run_command(cmd_args)


def flext_meltano_run_cli(project_root: Path = Path.cwd()) -> FlextResult[FlextMeltanoCli]:
    """Create and return CLI instance."""
    try:
        cli = FlextMeltanoCli(project_root)
        return FlextResult(data=cli)
    except Exception as e:
        return FlextResult(error=f"CLI creation failed: {e}")


__all__ = [
    "FlextMeltanoCli",
    "flext_meltano_run_cli",
]
