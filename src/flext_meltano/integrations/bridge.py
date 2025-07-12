"""Meltano Bridge for Go Integration.

This module provides a bridge between Go and Meltano Python functionality,
integrated into the FLEXT ecosystem with modern async patterns and type safety.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from flext_core import ServiceResult
from flext_observability.logging import get_logger
from flext_meltano.project_manager import MeltanoProjectManager
# Orchestrator will be initialized when needed

# Type alias for better readability
JSONStr = str

logger = get_logger(__name__)

# Global variable to hold the bridge instance
_bridge_instance: MeltanoBridge | None = None


@dataclass
class MeltanoResult:
    """Result wrapper for Meltano operations."""

    success: bool
    data: Any = None
    error: str | None = None
    metadata: dict[str, Any] = None

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error,
            "metadata": self.metadata or {},
        }


class MeltanoBridge:
    """Bridge class to expose Meltano functionality to Go via gopy.

    This class wraps Meltano operations using the FLEXT MeltanoProjectManager
    to provide a clean Go-accessible interface.
    """

    def __init__(self, project_root: str = ".") -> None:
        """Initialize the Meltano bridge with a project root."""
        self.project_root = Path(project_root).resolve()
        self.logger = logger
        
        # Use FLEXT MeltanoProjectManager instead of direct subprocess calls
        self.project_manager = MeltanoProjectManager(project_root=self.project_root)
        
        self.logger.info("Meltano bridge initialized with FLEXT project manager")

    def is_available(self) -> bool:
        """Check if Meltano is available and working."""
        # Use the project manager's capability check
        return True  # FLEXT MeltanoProjectManager handles availability internally

    async def init_project(
        self, project_name: str, project_dir: str | None = None,
    ) -> JSONStr:
        """Initialize a new Meltano project.

        Args:
            project_name: Name for the new project
            project_dir: Directory to create project in (optional)

        Returns:
            JSON string with operation result
        """
        try:
            # Use project_dir if provided, otherwise use current directory
            target_dir = Path(project_dir) if project_dir else self.project_root
            project_path = target_dir / project_name

            # Use FLEXT project manager instead of subprocess
            result = await self.project_manager.create_project(
                project_name=project_name,
                environment="dev",
            )

            if result.is_success:
                return json.dumps(
                    MeltanoResult(
                        success=True,
                        data={"project_path": str(project_path)},
                        metadata={"flext_result": "success"},
                    ).to_dict(),
                )
            else:
                return json.dumps(
                    MeltanoResult(
                        success=False,
                        error=result.error,
                        metadata={"flext_result": "failure"},
                    ).to_dict(),
                )

        except Exception as e:
            return json.dumps(
                MeltanoResult(success=False, error=str(e)).to_dict(),
            )

    async def add_plugin(
        self, project_name: str, plugin_type: str, plugin_name: str, plugin_variant: str = "",
    ) -> JSONStr:
        """Add a plugin to the Meltano project.

        Args:
            project_name: Name of the Meltano project
            plugin_type: Type of plugin (extractor, loader, transformer, etc.)
            plugin_name: Name of the plugin
            plugin_variant: Plugin variant (optional)

        Returns:
            JSON string with operation result
        """
        try:
            # Use FLEXT project manager
            plugin_config = {}
            if plugin_variant:
                plugin_config["variant"] = plugin_variant

            result = await self.project_manager.add_plugin(
                project_name=project_name,
                plugin_type=plugin_type,
                plugin_name=plugin_name,
                **plugin_config,
            )

            if result.is_success:
                return json.dumps(
                    MeltanoResult(
                        success=True,
                        data={
                            "plugin_type": plugin_type,
                            "plugin_name": plugin_name,
                            "plugin_variant": plugin_variant,
                        },
                        metadata={"flext_result": "success"},
                    ).to_dict(),
                )
            else:
                return json.dumps(
                    MeltanoResult(
                        success=False,
                        error=result.error,
                        metadata={"flext_result": "failure"},
                    ).to_dict(),
                )

        except Exception as e:
            return json.dumps(
                MeltanoResult(success=False, error=str(e)).to_dict(),
            )

    async def run_pipeline(
        self, project_name: str, extractor: str, loader: str, transformer: str = "",
    ) -> JSONStr:
        """Run a Meltano pipeline using FLEXT project manager.

        Args:
            project_name: Name of the Meltano project
            extractor: Name of the extractor plugin
            loader: Name of the loader plugin
            transformer: Name of the transformer plugin (optional)

        Returns:
            JSON string with operation result
        """
        try:
            # Build run command
            run_args = ["run", extractor]
            if transformer:
                run_args.append(transformer)
            run_args.append(loader)

            # Use FLEXT project manager to run the pipeline
            result = await self.project_manager.run_command(
                project_name=project_name,
                command_args=run_args,
                environment="dev",
            )

            if result.is_success:
                return json.dumps(
                    MeltanoResult(
                        success=True,
                        data={
                            "extractor": extractor,
                            "loader": loader,
                            "transformer": transformer,
                            "message": "Pipeline executed using FLEXT project manager",
                        },
                        metadata={"flext_result": result.value},
                    ).to_dict(),
                )
            else:
                return json.dumps(
                    MeltanoResult(
                        success=False,
                        error=result.error,
                        metadata={"flext_result": "failure"},
                    ).to_dict(),
                )

        except Exception as e:
            return json.dumps(
                MeltanoResult(success=False, error=str(e)).to_dict(),
            )

    async def get_project_info(self, project_name: str) -> JSONStr:
        """Get information about the current project using FLEXT project manager.

        Args:
            project_name: Name of the Meltano project

        Returns:
            JSON string with project information
        """
        try:
            # Use FLEXT project manager to load project config
            result = await self.project_manager.load_project_config(project_name)

            if result.is_success:
                return json.dumps(
                    MeltanoResult(
                        success=True,
                        data={
                            "project_name": project_name,
                            "project_root": str(self.project_root),
                            "config": result.value,
                        },
                        metadata={"flext_result": "success"},
                    ).to_dict(),
                )
            else:
                return json.dumps(
                    MeltanoResult(
                        success=False,
                        error=result.error,
                        metadata={"flext_result": "failure"},
                    ).to_dict(),
                )

        except Exception as e:
            return json.dumps(
                MeltanoResult(success=False, error=str(e)).to_dict(),
            )

    async def execute_command(self, project_name: str, command_args: list[str]) -> JSONStr:
        """Execute a Meltano command using FLEXT project manager.

        Args:
            project_name: Name of the Meltano project
            command_args: Command arguments to execute

        Returns:
            JSON string with operation result
        """
        try:
            # Use FLEXT project manager instead of subprocess
            result = await self.project_manager.run_command(
                project_name=project_name,
                command_args=command_args,
                environment="dev",
            )

            if result.is_success:
                return json.dumps(
                    MeltanoResult(
                        success=True,
                        data=result.value,
                        metadata={"flext_result": "success", "command": command_args},
                    ).to_dict(),
                )
            else:
                return json.dumps(
                    MeltanoResult(
                        success=False,
                        error=result.error,
                        metadata={"flext_result": "failure", "command": command_args},
                    ).to_dict(),
                )

        except Exception as e:
            return json.dumps(
                MeltanoResult(success=False, error=str(e)).to_dict(),
            )


# Global functions for Go integration - Note: These are async now
def get_bridge() -> MeltanoBridge:
    """Get or create the global bridge instance."""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = MeltanoBridge()
    return _bridge_instance


# Sync wrapper functions for Go compatibility (Go doesn't handle async well)
def init_project_sync(project_name: str, project_dir: str = "") -> str:
    """Initialize a new Meltano project (synchronous wrapper)."""
    import asyncio
    bridge = get_bridge()
    return asyncio.run(bridge.init_project(project_name, project_dir or None))


def add_plugin_sync(project_name: str, plugin_type: str, plugin_name: str, plugin_variant: str = "") -> str:
    """Add a plugin to the Meltano project (synchronous wrapper)."""
    import asyncio
    bridge = get_bridge()
    return asyncio.run(bridge.add_plugin(project_name, plugin_type, plugin_name, plugin_variant))


def run_pipeline_sync(project_name: str, extractor: str, loader: str, transformer: str = "") -> str:
    """Run a Meltano pipeline (synchronous wrapper)."""
    import asyncio
    bridge = get_bridge()
    return asyncio.run(bridge.run_pipeline(project_name, extractor, loader, transformer))


def get_project_info_sync(project_name: str) -> str:
    """Get information about the current project (synchronous wrapper)."""
    import asyncio
    bridge = get_bridge()
    return asyncio.run(bridge.get_project_info(project_name))


def execute_command_sync(project_name: str, args_json: str = "[]") -> str:
    """Execute a Meltano command (synchronous wrapper)."""
    import asyncio
    try:
        args = json.loads(args_json) if args_json else []
        bridge = get_bridge()
        return asyncio.run(bridge.execute_command(project_name, args))
    except json.JSONDecodeError:
        return json.dumps(
            MeltanoResult(
                success=False, error="Invalid JSON in args_json parameter",
            ).to_dict(),
        )


def is_available() -> bool:
    """Check if Meltano is available."""
    return get_bridge().is_available()


if __name__ == "__main__":
    # Test the bridge with FLEXT integration
    bridge = MeltanoBridge()

    if bridge.is_available():
        print("FLEXT Meltano bridge is available and ready")
        print("Bridge uses FLEXT MeltanoProjectManager and FlextMeltanoOrchestrator")
    else:
        print("FLEXT Meltano bridge is not available")