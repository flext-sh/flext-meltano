"""Go Bridge - JSON API para integração Go ↔ Python.

FUNÇÃO 2: Runtime Go Bridge
- FlextMeltanoBridge: API JSON para Go services
- Structured responses for Go consumption
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_core import get_logger

from .runtime import FlextMeltanoExecutor
from .meltano_wrapper import MeltanoBridge
from .dbt_wrapper import MeltanoDbtWrapper

logger = get_logger(__name__)


class FlextMeltanoBridge:
    """Bridge class for Go service integration via JSON API."""

    def __init__(self) -> None:
        self.executor = FlextMeltanoExecutor()
        self.meltano_bridge = MeltanoBridge()
        self.dbt_wrapper = MeltanoDbtWrapper()

    def get_version(self) -> dict[str, Any]:
        """Get version information for Go service."""
        try:
            return {
                "success": True,
                "data": {
                    "flext_meltano": "2.0.0-enterprise",
                    "meltano": "3.9.1",
                    "dbt_core": "1.10.5",
                    "singer_sdk": "0.48.0",
                    "python": "3.13+",
                    "integration_method": "native_apis",
                },
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def list_plugins(self) -> dict[str, Any]:
        """List available Meltano plugins."""
        try:
            result = self.meltano_bridge.discover_plugins()
            if result.is_success:
                return {"success": True, "data": result.value}
            return {"success": False, "error": result.error}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def run_pipeline(
        self, tap_name: str, target_name: str, project_root: str = "."
    ) -> dict[str, Any]:
        """Run ELT pipeline between tap and target."""
        try:
            project_path = Path(project_root)
            result = self.executor.run_elt_pipeline(project_path, tap_name, target_name)

            if result.is_success:
                return {"success": True, "data": result.value}
            return {"success": False, "error": result.error}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def execute_meltano_command(
        self, command: list[str], project_root: str = "."
    ) -> dict[str, Any]:
        """Execute arbitrary Meltano command."""
        try:
            project_path = Path(project_root)
            result = self.executor.execute_meltano_command(project_path, command)

            if result.is_success:
                return {"success": True, "data": result.value}
            return {"success": False, "error": result.error}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def execute_dbt_command(
        self, command: list[str], project_root: str = "."
    ) -> dict[str, Any]:
        """Execute arbitrary DBT command."""
        try:
            project_path = Path(project_root)
            result = self.executor.execute_dbt_command(project_path, command)

            if result.is_success:
                return {"success": True, "data": result.value}
            return {"success": False, "error": result.error}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def install_plugin(
        self, plugin_type: str, plugin_name: str, project_root: str = "."
    ) -> dict[str, Any]:
        """Install Meltano plugin."""
        try:
            project_path = Path(project_root)
            result = self.meltano_bridge.install_plugin(
                project_path, plugin_type, plugin_name
            )

            if result.is_success:
                return {"success": True, "data": result.value}
            return {"success": False, "error": result.error}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_project_info(self, project_root: str = ".") -> dict[str, Any]:
        """Get project information."""
        try:
            project_path = Path(project_root)
            result = self.executor.get_project_info(project_path)

            if result.is_success:
                return {"success": True, "data": result.value}
            return {"success": False, "error": result.error}
        except Exception as e:
            return {"success": False, "error": str(e)}


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = ["FlextMeltanoBridge"]
