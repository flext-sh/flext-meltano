"""Go Bridge - JSON API para integração Go ↔ Python.

FUNÇÃO 2: Runtime Go Bridge
- FlextMeltanoBridge: API JSON para Go services
- Structured responses for Go consumption
"""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextLogger

from flext_meltano.dbt_adapters import MeltanoDbtWrapper
from flext_meltano.executors_meltano import FlextMeltanoExecutor, FlextMeltanoExecutors
from flext_meltano.meltano_adapters import MeltanoBridge

logger = FlextLogger(__name__)


class FlextMeltanoBridge:
    """Bridge class for Go service integration via JSON API."""

    def __init__(self) -> None:
        self.executor: FlextMeltanoExecutor = FlextMeltanoExecutor()
        self.meltano_bridge: MeltanoBridge = MeltanoBridge()
        self.wrapper_dbt: MeltanoDbtWrapper = MeltanoDbtWrapper()

    def get_version(self) -> dict[str, object]:
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
            return {"success": False, "data": None, "error": str(e)}

    def list_plugins(self) -> dict[str, object]:
        """List available Meltano plugins."""
        try:
            result = self.meltano_bridge.discover_plugins()

            # Handle both FlextResult and direct value (when flext-cli decorator is active)
            if hasattr(result, "success"):
                # It's a FlextResult
                if result.success:
                    return {"success": True, "data": result.value}
                return {"success": False, "data": None, "error": result.error}
            # It's the direct value (flext-cli decorator processed it)
            return {"success": True, "data": result}

        except Exception as e:
            return {"success": False, "data": None, "error": str(e)}

    def run_pipeline(
        self, tap_name: str, target_name: str, project_root: str = "."
    ) -> dict[str, object]:
        """Run ELT pipeline between tap and target."""
        try:
            project_path = Path(project_root)
            # Use SimpleMeltanoExecutor for pipeline operations
            result = FlextMeltanoExecutors.SimpleMeltanoExecutor.run_pipeline(
                project_path, tap_name, target_name
            )

            if result.success:
                return {"success": True, "data": result.data or {}}
            return {"success": False, "data": None, "error": result.error}
        except Exception as e:
            return {"success": False, "data": None, "error": str(e)}

    def execute_meltano_command(
        self, command: list[str], project_root: str = "."
    ) -> dict[str, object]:
        """Execute arbitrary Meltano command."""
        try:
            project_path = Path(project_root)
            result = self.executor.execute_meltano_command(project_path, command)

            if result.success:
                return {"success": True, "data": result.value}
            return {"success": False, "data": None, "error": result.error}
        except Exception as e:
            return {"success": False, "data": None, "error": str(e)}

    def execute_dbt_command(
        self, command: list[str], project_root: str = "."
    ) -> dict[str, object]:
        """Execute arbitrary DBT command."""
        try:
            project_path = Path(project_root)
            # Use execute_meltano_command for DBT operations via Meltano
            dbt_command = ["dbt", *command]
            result = self.executor.execute_meltano_command(project_path, dbt_command)

            if result.success:
                return {"success": True, "data": result.value}
            return {"success": False, "data": None, "error": result.error}
        except Exception as e:
            return {"success": False, "data": None, "error": str(e)}

    def install_plugin(
        self, plugin_type: str, plugin_name: str, project_root: str = "."
    ) -> dict[str, object]:
        """Install Meltano plugin."""
        try:
            project_path = Path(project_root)
            result = self.meltano_bridge.install_plugin(
                project_path, plugin_type, plugin_name
            )

            if result.success:
                return {"success": True, "data": result.value}
            return {"success": False, "data": None, "error": result.error}
        except Exception as e:
            return {"success": False, "data": None, "error": str(e)}

    def get_project_info(self, project_root: str = ".") -> dict[str, object]:
        """Get project information."""
        try:
            project_path = Path(project_root)
            result = self.executor.get_project_info(project_path)

            if result.success:
                return {"success": True, "data": result.value}
            return {"success": False, "data": None, "error": result.error}
        except Exception as e:
            return {"success": False, "data": None, "error": str(e)}

    def invoke_dbt(self, command: str, **kwargs: object) -> dict[str, object]:
        """Invoke DBT command with additional arguments."""
        try:
            cmd_list = [command]
            for key, value in kwargs.items():
                if key.startswith("_"):
                    # Convert _arg to --arg format
                    cmd_list.extend([f"--{key[1:].replace('_', '-')}", str(value)])
                else:
                    # Convert arg to --arg format
                    cmd_list.extend([f"--{key.replace('_', '-')}", str(value)])

            project_root_value = kwargs.get("project_dir", ".")
            project_root = str(project_root_value) if project_root_value else "."
            return self.execute_dbt_command(cmd_list, project_root)
        except Exception as e:
            return {"success": False, "data": None, "error": str(e)}


# =============================================================================
# FACTORY FUNCTIONS
# =============================================================================


def create_flext_meltano_bridge(
    _config: dict[str, object] | None = None,
) -> FlextMeltanoBridge:
    """Factory function to create FlextMeltanoBridge instance."""
    # For now, ignore config parameter for compatibility
    return FlextMeltanoBridge()


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = ["FlextMeltanoBridge", "create_flext_meltano_bridge"]
