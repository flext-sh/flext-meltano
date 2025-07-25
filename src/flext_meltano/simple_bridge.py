"""FLEXT Meltano Simple Bridge - Interface para integração Go.

Bridge que USA a biblioteca flext-meltano em vez de bypass.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_meltano.helpers.execution import (
    flext_meltano_execute_job,
    flext_meltano_run_command,
)


class FlextMeltanoBridge:
    """Bridge que USA a biblioteca flext-meltano (não bypass)."""

    def __init__(self, project_root: str = "/home/marlonsc/flext") -> None:
        """Initialize FlextMeltanoBridge.

        Args:
            project_root: Path to the flext project root directory
        """
        self.project_root = Path(project_root)

    def get_version(self) -> dict[str, Any]:
        """Obtém versão do Meltano USANDO biblioteca."""
        result = flext_meltano_run_command(
            ["--version"],
            project_root=self.project_root,
        )
        return {
            "success": result.success,
            "output": result.data.get("stdout", "") if result.success and result.data else "",
            "error": result.error if not result.success else result.data.get("stderr", "") if result.data else "",
            "returncode": result.data.get("returncode", -1) if result.success and result.data else -1,
            "command": "--version",
        }

    def list_plugins(self) -> dict[str, Any]:
        """Lista plugins USANDO biblioteca."""
        result = flext_meltano_run_command(
            ["config", "meltano"],
            project_root=self.project_root,
        )
        return {
            "success": result.success,
            "output": result.data.get("stdout", "") if result.success and result.data else "",
            "error": result.error if not result.success else result.data.get("stderr", "") if result.data else "",
            "returncode": result.data.get("returncode", -1) if result.success and result.data else -1,
            "command": "config meltano",
        }

    def add_plugin(self, plugin_type: str, plugin_name: str) -> dict[str, Any]:
        """Adiciona plugin USANDO biblioteca."""
        result = flext_meltano_run_command(
            ["add", plugin_type, plugin_name, "--install"],
            project_root=self.project_root,
        )
        return {
            "success": result.success,
            "output": result.data.get("stdout", "") if result.success and result.data else "",
            "error": result.error if not result.success else result.data.get("stderr", "") if result.data else "",
            "returncode": result.data.get("returncode", -1) if result.success and result.data else -1,
            "command": f"add {plugin_type} {plugin_name} --install",
        }

    def discover_catalog(self, tap_name: str) -> dict[str, Any]:
        """Descobre catálogo USANDO biblioteca."""
        result = flext_meltano_run_command(
            ["invoke", tap_name, "--discover"],
            project_root=self.project_root,
        )
        return {
            "success": result.success,
            "output": result.data.get("stdout", "") if result.success and result.data else "",
            "error": result.error if not result.success else result.data.get("stderr", "") if result.data else "",
            "returncode": result.data.get("returncode", -1) if result.success and result.data else -1,
            "command": f"invoke {tap_name} --discover",
        }

    def run_pipeline(self, tap_name: str, target_name: str) -> dict[str, Any]:
        """Executa pipeline USANDO biblioteca."""
        result = flext_meltano_execute_job(
            tap_name=tap_name,
            target_name=target_name,
            project_root=self.project_root,
        )
        return {
            "success": result.success,
            "output": result.data.get("stdout", "") if result.success and result.data else "",
            "error": result.error if not result.success else result.data.get("stderr", "") if result.data else "",
            "returncode": result.data.get("returncode", -1) if result.success and result.data else -1,
            "command": f"run {tap_name} {target_name}",
        }

    def invoke_dbt(self, dbt_command: str, *args: str) -> dict[str, Any]:
        """Invoca DBT USANDO biblioteca."""
        cmd_args = ["invoke", f"dbt:{dbt_command}", *list(args)]
        result = flext_meltano_run_command(
            cmd_args,
            project_root=self.project_root,
        )
        return {
            "success": result.success,
            "output": result.data.get("stdout", "") if result.success and result.data else "",
            "error": result.error if not result.success else result.data.get("stderr", "") if result.data else "",
            "returncode": result.data.get("returncode", -1) if result.success and result.data else -1,
            "command": f"invoke dbt:{dbt_command} {' '.join(args)}",
        }
