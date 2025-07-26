"""FLEXT Meltano Bridge.

Go integration bridge using flext-meltano library.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from flext_meltano.constants import FlextMeltanoConstants


class FlextMeltanoBridge:
    """Bridge for Go integration using flext-meltano library."""

    def __init__(self, project_root: str = "/home/marlonsc/flext") -> None:
        """Initialize bridge.

        Args:
            project_root: Path to the flext project root directory

        """
        self.project_root = Path(project_root)

    def get_version(self) -> dict[str, Any]:
        """Get Meltano version."""
        try:
            cmd = ["meltano", "--version"]
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.COMMAND_TIMEOUT,
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout if result.returncode == 0 else "",
                "error": result.stderr if result.returncode != 0 else "",
                "returncode": result.returncode,
                "command": "--version",
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1,
                "command": "--version",
            }

    def list_plugins(self) -> dict[str, Any]:
        """List plugins."""
        try:
            cmd = ["meltano", "config", "meltano"]
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.COMMAND_TIMEOUT,
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout if result.returncode == 0 else "",
                "error": result.stderr if result.returncode != 0 else "",
                "returncode": result.returncode,
                "command": "config meltano",
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1,
                "command": "config meltano",
            }

    def add_plugin(self, plugin_type: str, plugin_name: str) -> dict[str, Any]:
        """Add plugin."""
        try:
            cmd = ["meltano", "add", plugin_type, plugin_name, "--install"]
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.COMMAND_TIMEOUT,
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout if result.returncode == 0 else "",
                "error": result.stderr if result.returncode != 0 else "",
                "returncode": result.returncode,
                "command": f"add {plugin_type} {plugin_name} --install",
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1,
                "command": f"add {plugin_type} {plugin_name} --install",
            }

    def discover_catalog(self, tap_name: str) -> dict[str, Any]:
        """Discover catalog."""
        try:
            cmd = ["meltano", "invoke", tap_name, "--discover"]
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.COMMAND_TIMEOUT,
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout if result.returncode == 0 else "",
                "error": result.stderr if result.returncode != 0 else "",
                "returncode": result.returncode,
                "command": f"invoke {tap_name} --discover",
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1,
                "command": f"invoke {tap_name} --discover",
            }

    def run_pipeline(self, tap_name: str, target_name: str) -> dict[str, Any]:
        """Run pipeline."""
        try:
            cmd = ["meltano", "run", tap_name, target_name]
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.PIPELINE_TIMEOUT,
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout if result.returncode == 0 else "",
                "error": result.stderr if result.returncode != 0 else "",
                "returncode": result.returncode,
                "command": f"run {tap_name} {target_name}",
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1,
                "command": f"run {tap_name} {target_name}",
            }

    def invoke_dbt(self, dbt_command: str, *args: str) -> dict[str, Any]:
        """Invoke DBT."""
        try:
            cmd = ["meltano", "invoke", f"dbt:{dbt_command}", *list(args)]
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.COMMAND_TIMEOUT,
            )

            return {
                "success": result.returncode == 0,
                "output": result.stdout if result.returncode == 0 else "",
                "error": result.stderr if result.returncode != 0 else "",
                "returncode": result.returncode,
                "command": f"invoke dbt:{dbt_command} {' '.join(args)}",
            }
        except Exception as e:
            return {
                "success": False,
                "output": "",
                "error": str(e),
                "returncode": -1,
                "command": f"invoke dbt:{dbt_command} {' '.join(args)}",
            }
