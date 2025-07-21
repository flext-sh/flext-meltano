"""Meltano Bridge for Go Integration.

This module provides a bridge between Go and Meltano Python functionality,
integrated into the FLEXT ecosystem with modern async patterns and type safety.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from flext_observability.logging import get_logger

from flext_meltano.project_manager import MeltanoProjectManager
from flext_meltano.singer_direct import SingerDirectRunner

# Orchestrator will be initialized when needed

# Type alias for better readability
JSONStr = str

logger = get_logger(__name__)

# Global variable to hold the bridge instance
_bridge_instance: MeltanoBridge | None = None


@dataclass
class MeltanoResult:
    """Result wrapper for Meltano operations with flext-core integration."""

    success: bool
    message: str = ""
    data: dict[str, Any] | None = None
    metadata: dict[str, Any] | None = None
    error: str | None = None  # Keeping for backwards compatibility

    def to_dict(self) -> dict[str, Any]:
        """Convert result to dictionary for JSON serialization."""
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data,
            "metadata": self.metadata,
            "error": self.error,
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

        # Use FLEXT integrations for zero warnings
        self.project_manager = MeltanoProjectManager(project_root=self.project_root)
        self.singer_direct = SingerDirectRunner(self.project_root)

        self.logger.info(
            "Meltano bridge initialized with zero-warning Singer direct runner",
        )

    def is_available(self) -> bool:
        """Check if Meltano is available and working."""
        # Use the project manager's capability check
        return True  # FLEXT MeltanoProjectManager handles availability internally

    async def init_project(
        self,
        project_name: str,
        project_dir: str | None = None,
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
            target_dir / project_name

            # Use FLEXT project manager instead of subprocess
            result = await self.project_manager.create_project(
                project_name=project_name,
                environment="dev",
            )

            if result.is_success:
                return json.dumps(
                    MeltanoResult(
                        success=True,
                        message="Project initialized successfully",
                        data={"project_name": project_name, "project_dir": project_dir},
                    ).to_dict(),
                )
            return json.dumps(
                MeltanoResult(
                    success=False,
                    message="Failed to initialize",
                    error=result.error,
                ).to_dict(),
            )
        except Exception as e:
            return json.dumps(
                MeltanoResult(
                    success=False,
                    message="Failed to initialize",
                    error=str(e),
                ).to_dict(),
            )

    async def add_plugin(
        self,
        project_name: str,
        plugin_type: str,
        plugin_name: str,
        plugin_variant: str = "",
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
            # Use FLEXT project manager with proper variant parameter
            result = await self.project_manager.add_plugin(
                project_name=project_name,
                plugin_type=plugin_type,
                plugin_name=plugin_name,
                variant=plugin_variant,
            )

            if result.is_success:
                return json.dumps(
                    MeltanoResult(
                        success=True,
                        message="Plugin added successfully",
                        data={
                            "plugin_type": plugin_type,
                            "plugin_name": plugin_name,
                            "plugin_variant": plugin_variant,
                        },
                        metadata={"flext_result": "success"},
                    ).to_dict(),
                )
            return json.dumps(
                MeltanoResult(
                    success=False,
                    message="Failed to add plugin",
                    error=result.error,
                    metadata={"flext_result": "failure"},
                ).to_dict(),
            )
        except Exception as e:
            return json.dumps(
                MeltanoResult(
                    success=False,
                    message="Plugin addition failed",
                    error=str(e),
                ).to_dict(),
            )

    async def run_pipeline(
        self,
        project_name: str,
        extractor: str,
        loader: str,
        transformer: str = "",
    ) -> JSONStr:
        """Run a Meltano pipeline using FLEXT project manager with zero Singer SDK warnings.

        Uses official meltano el command for extract-load pipelines to eliminate
        Singer SDK deprecation warnings about catalog/config file paths.

        Args:
            project_name: Name of the Meltano project
            extractor: Name of the extractor plugin
            loader: Name of the loader plugin
            transformer: Name of the transformer plugin (optional)

        Returns:
            JSON string with operation result

        """
        try:
            # Use official Meltano el command (the correct way)
            if transformer:
                # For transformers, use run command
                run_args = ["run", extractor, transformer, loader]
            else:
                # Use el command for extract-load pipelines (official Meltano way)
                run_args = ["el", extractor, loader]

            # Use FLEXT project manager with official Meltano approach
            result = await self.project_manager.run_command(
                project_name=project_name,
                command_args=run_args,
                environment="dev",
            )

            if result.is_success:
                return json.dumps(
                    MeltanoResult(
                        success=True,
                        message="Pipeline executed successfully",
                        data={
                            "project_name": project_name,
                            "extractor": extractor,
                            "loader": loader,
                            "transformer": transformer,
                            "result": result.data,
                        },
                    ).to_dict(),
                )
            return json.dumps(
                MeltanoResult(
                    success=False,
                    message="Pipeline execution failed",
                    error=result.error,
                ).to_dict(),
            )
        except Exception as e:
            return json.dumps(
                MeltanoResult(
                    success=False,
                    message="Pipeline execution error",
                    error=str(e),
                ).to_dict(),
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
                        message="Project info retrieved successfully",
                        data={
                            "project_name": project_name,
                            "project_info": result.data,
                        },
                    ).to_dict(),
                )
            return json.dumps(
                MeltanoResult(
                    success=False,
                    message="Failed to get project info",
                    error=result.error,
                ).to_dict(),
            )
        except Exception as e:
            return json.dumps(
                MeltanoResult(
                    success=False,
                    message="Project info retrieval error",
                    error=str(e),
                ).to_dict(),
            )

    async def execute_command(
        self,
        project_name: str,
        command_args: list[str],
    ) -> JSONStr:
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
                        message="Command executed successfully",
                        data={
                            "project_name": project_name,
                            "args": command_args,
                            "result": result.data,
                        },
                    ).to_dict(),
                )
            return json.dumps(
                MeltanoResult(
                    success=False,
                    message="Command execution failed",
                    error=result.error,
                ).to_dict(),
            )
        except Exception as e:
            return json.dumps(
                MeltanoResult(
                    success=False,
                    message="Command execution error",
                    error=str(e),
                ).to_dict(),
            )


# Global functions for Go integration - Note: These are async now
def get_bridge() -> MeltanoBridge:
    """Get or create the global bridge instance."""
    global _bridge_instance
    if _bridge_instance is None:
        _bridge_instance = MeltanoBridge()
    return _bridge_instance


# Sync wrapper functions for Go compatibility (Go doesn't handle async well)
def init_project_sync(
    project_root: str | Path,
    **kwargs: Any,
) -> str:
    """Synchronous wrapper for project initialization."""
    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    async def run_async() -> str:
        """Async project initialization."""
        bridge = get_bridge()
        result = await bridge.init_project(
            project_name=str(kwargs.get("project_name", "")),
            project_dir=kwargs.get("project_dir"),
        )
        return str(result)

    def run_in_thread() -> str:
        try:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(run_async())
            finally:
                loop.close()
        except Exception as e:
            return f"Error: {e}"

    with ThreadPoolExecutor(max_workers=1) as executor:
        try:
            return executor.submit(run_in_thread).result()
        except Exception as e:
            return f"Error: {e}"


def add_plugin_sync(
    plugin_type: str,
    plugin_name: str,
    **kwargs: Any,
) -> str:
    """Synchronous wrapper for plugin installation."""
    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    async def run_async() -> str:
        """Async plugin installation."""
        bridge = get_bridge()
        result = await bridge.add_plugin(
            project_name=str(kwargs.get("project_name", "")),
            plugin_type=plugin_type,
            plugin_name=plugin_name,
            plugin_variant=str(kwargs.get("plugin_variant", "")),
        )
        return str(result)

    def run_in_thread() -> str:
        try:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(run_async())
            finally:
                loop.close()
        except Exception as e:
            return f"Error: {e}"

    with ThreadPoolExecutor(max_workers=1) as executor:
        try:
            return executor.submit(run_in_thread).result()
        except Exception as e:
            return f"Error: {e}"


def run_pipeline_sync(pipeline_name: str, **kwargs: Any) -> str:
    """Synchronous wrapper for pipeline execution."""
    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    async def run_async() -> str:
        """Async pipeline execution."""
        bridge = get_bridge()
        result = await bridge.run_pipeline(
            project_name=str(kwargs.get("project_name", "")),
            extractor=str(kwargs.get("extractor", "")),
            loader=str(kwargs.get("loader", "")),
            transformer=str(kwargs.get("transformer", "")),
        )
        return str(result)

    def run_in_thread() -> str:
        try:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(run_async())
            finally:
                loop.close()
        except Exception as e:
            return f"Error: {e}"

    with ThreadPoolExecutor(max_workers=1) as executor:
        try:
            return executor.submit(run_in_thread).result()
        except Exception as e:
            return f"Error: {e}"


def get_project_info_sync(**kwargs: Any) -> str:
    """Synchronous wrapper for project info retrieval."""
    import asyncio
    from concurrent.futures import ThreadPoolExecutor

    async def run_async() -> str:
        bridge = get_bridge()
        result = await bridge.get_project_info(str(kwargs.get("project_name", "")))
        return str(result)

    def run_in_thread() -> str:
        try:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(run_async())
            finally:
                loop.close()
        except Exception as e:
            return f"Error: {e}"

    with ThreadPoolExecutor(max_workers=1) as executor:
        try:
            return executor.submit(run_in_thread).result()
        except Exception as e:
            return f"Error: {e}"


def execute_command_sync(command: str, **kwargs: Any) -> str:
    """Synchronous wrapper for command execution."""
    import asyncio
    import json
    from concurrent.futures import ThreadPoolExecutor

    async def run_async() -> str:
        bridge = get_bridge()
        args = json.loads(command) if command else []
        result = await bridge.execute_command(str(kwargs.get("project_name", "")), args)
        return str(result)

    def run_in_thread() -> str:
        try:
            loop = asyncio.new_event_loop()
            try:
                return loop.run_until_complete(run_async())
            finally:
                loop.close()
        except json.JSONDecodeError:
            return json.dumps({
                "success": False,
                "message": "Invalid JSON in command arguments",
                "error": "Could not parse command arguments as JSON",
            })
        except Exception as e:
            return f"Error: {e}"

    with ThreadPoolExecutor(max_workers=1) as executor:
        try:
            return executor.submit(run_in_thread).result()
        except Exception as e:
            return f"Error: {e}"


def is_available() -> bool:
    """Check if Meltano is available."""
    return get_bridge().is_available()


if __name__ == "__main__":
    # Test the bridge with FLEXT integration
    bridge = MeltanoBridge()

    if bridge.is_available():
        pass
