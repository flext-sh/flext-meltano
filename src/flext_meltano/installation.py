"""FLEXT Meltano installation helpers using MANDATORY patterns.

Plugin installation and management using enterprise patterns.
Uses mandatory flext-core patterns for consistency.
"""

from __future__ import annotations

import json
import subprocess
import uuid
import warnings
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# FlextResult is MANDATORY for all operations
from flext_core import FlextResult
from injectable import injectable
from pydantic import BaseModel, Field

from flext_meltano.base import FlextMeltanoConfig
from flext_meltano.execution import FlextMeltanoResult


class FlextMeltanoInstallationContext(BaseModel):
    """Installation context for plugin operations."""

    installation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    started_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    plugin_name: str = Field(...)
    plugin_type: str = Field(...)
    project_root: Path = Field(default_factory=Path)
    timeout_seconds: int = Field(default=600)  # 10 minutes default
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True


class FlextMeltanoPluginInfo(BaseModel):
    """Plugin information entity."""

    name: str = Field(...)
    type: str = Field(...)
    namespace: str = Field(...)
    pip_url: str | None = Field(default=None)
    executable: str | None = Field(default=None)
    description: str = Field(default="")
    version: str | None = Field(default=None)
    installed: bool = Field(default=False)

    class Config:
        """Pydantic configuration."""

        frozen = True


@injectable
class FlextMeltanoInstaller:
    """Plugin installer using MANDATORY patterns."""

    def __init__(self, config: FlextMeltanoConfig) -> None:
        """Initialize with dependency injection."""
        self.config = config
        self.project_root = Path(config.project_root)
        self._initialized = False

    def validate(self) -> FlextResult[bool]:
        """Validate installation service."""
        try:
            # Check if project root exists
            if not self.project_root.exists():
                return FlextResult(
                    error=f"Project root does not exist: {self.project_root}",
                )

            # Check if meltano.yml exists
            meltano_yml = self.project_root / "meltano.yml"
            if not meltano_yml.exists():
                return FlextResult(error=f"No meltano.yml found in {self.project_root}")

            return FlextResult(data=True)
        except (OSError, ValueError) as e:
            return FlextResult(error=f"Validation failed: {e}")

    def initialize(self) -> FlextResult[bool]:
        """Initialize service."""
        self._initialized = True
        return FlextResult(data=True)

    def get_health_status(self) -> FlextResult[dict[str, Any]]:
        """Get installation service health status."""
        return FlextResult(
            data={
                "service": "installation",
                "project_root": str(self.project_root),
                "meltano_yml_exists": (self.project_root / "meltano.yml").exists(),
                "initialized": self._initialized,
            },
        )

    def add_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
        pip_url: str | None = None,
        context: FlextMeltanoInstallationContext | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Add plugin to meltano project using enterprise patterns."""
        if not context:
            context = FlextMeltanoInstallationContext(
                plugin_name=plugin_name,
                plugin_type=plugin_type,
                project_root=self.project_root,
            )

        try:
            # Validate first
            validation_result = self.validate()
            if not validation_result.is_success:
                return FlextResult(error=validation_result.error)

            # Build command
            cmd = ["meltano", "add", plugin_type, plugin_name]
            if pip_url:
                cmd.extend(["--custom", pip_url])

            # Execute subprocess
            result = subprocess.run(  # noqa: S603
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=context.timeout_seconds,
                check=False,
            )

            installation_result = {
                "installation_id": context.installation_id,
                "plugin_name": plugin_name,
                "plugin_type": plugin_type,
                "pip_url": pip_url,
                "command": " ".join(cmd),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "started_at": context.started_at.isoformat(),
                "completed_at": datetime.now(UTC).isoformat(),
                "duration_seconds": (
                    datetime.now(UTC) - context.started_at
                ).total_seconds(),
            }

            if result.returncode == 0:
                return FlextResult(data=installation_result)
            return FlextResult(
                error=f"Plugin add failed: {result.stderr or result.stdout}",
            )

        except subprocess.TimeoutExpired:
            return FlextResult(error="Plugin add timed out")
        except (OSError, subprocess.CalledProcessError) as e:
            return FlextResult(error=f"Plugin add error: {e}")

    def install_plugins(
        self,
        context: FlextMeltanoInstallationContext | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Install all plugins in meltano project."""
        if not context:
            context = FlextMeltanoInstallationContext(
                plugin_name="all",
                plugin_type="install",
                project_root=self.project_root,
            )

        try:
            # Validate first
            validation_result = self.validate()
            if not validation_result.is_success:
                return FlextResult(error=validation_result.error)

            # Execute meltano install
            cmd = ["meltano", "install"]
            result = subprocess.run(  # noqa: S603
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=context.timeout_seconds,
                check=False,
            )

            installation_result = {
                "installation_id": context.installation_id,
                "operation": "install_all",
                "command": " ".join(cmd),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "started_at": context.started_at.isoformat(),
                "completed_at": datetime.now(UTC).isoformat(),
                "duration_seconds": (
                    datetime.now(UTC) - context.started_at
                ).total_seconds(),
            }

            if result.returncode == 0:
                return FlextResult(data=installation_result)
            return FlextResult(
                error=f"Plugin install failed: {result.stderr or result.stdout}",
            )

        except subprocess.TimeoutExpired:
            return FlextResult(error="Plugin install timed out")
        except (OSError, subprocess.CalledProcessError) as e:
            return FlextResult(error=f"Plugin install error: {e}")

    def remove_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
        context: FlextMeltanoInstallationContext | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Remove plugin from meltano project."""
        if not context:
            context = FlextMeltanoInstallationContext(
                plugin_name=plugin_name,
                plugin_type=plugin_type,
                project_root=self.project_root,
                timeout_seconds=300,  # 5 minutes for removal
            )

        try:
            # Validate first
            validation_result = self.validate()
            if not validation_result.is_success:
                return FlextResult(error=validation_result.error)

            # Build command
            cmd = ["meltano", "remove", plugin_type, plugin_name]

            # Execute subprocess
            result = subprocess.run(  # noqa: S603
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=context.timeout_seconds,
                check=False,
            )

            removal_result = {
                "installation_id": context.installation_id,
                "operation": "remove",
                "plugin_name": plugin_name,
                "plugin_type": plugin_type,
                "command": " ".join(cmd),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
                "started_at": context.started_at.isoformat(),
                "completed_at": datetime.now(UTC).isoformat(),
                "duration_seconds": (
                    datetime.now(UTC) - context.started_at
                ).total_seconds(),
            }

            if result.returncode == 0:
                return FlextResult(data=removal_result)
            return FlextResult(
                error=f"Plugin remove failed: {result.stderr or result.stdout}",
            )

        except subprocess.TimeoutExpired:
            return FlextResult(error="Plugin remove timed out")
        except (OSError, subprocess.CalledProcessError) as e:
            return FlextResult(error=f"Plugin remove error: {e}")

    def list_plugins(self) -> FlextResult[list[FlextMeltanoPluginInfo]]:
        """List installed plugins in meltano project."""
        try:
            # Validate first
            validation_result = self.validate()
            if not validation_result.is_success:
                return FlextResult(error=validation_result.error)

            # Execute subprocess
            result = self._execute_meltano_list()
            if not result.is_success:
                return FlextResult(error=result.error)

            # Parse JSON response
            if result.data is not None:
                return self._parse_plugin_list(result.data)
            return FlextResult(error="No plugin data received")

        except subprocess.TimeoutExpired:
            return FlextResult(error="Plugin list timed out")
        except (OSError, subprocess.CalledProcessError) as e:
            return FlextResult(error=f"Plugin list error: {e}")

    def _execute_meltano_list(self) -> FlextResult[str]:
        """Execute meltano list command."""
        cmd = ["meltano", "list", "--format=json"]
        result = subprocess.run(  # noqa: S603
            cmd,
            cwd=self.project_root,
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )

        if result.returncode == 0:
            return FlextResult(data=result.stdout)
        return FlextResult(
            error=f"Plugin list failed: {result.stderr or result.stdout}",
        )

    def _parse_plugin_list(
        self,
        stdout: str,
    ) -> FlextResult[list[FlextMeltanoPluginInfo]]:
        """Parse plugin list JSON response."""
        try:
            plugins_data = json.loads(stdout)
            plugins: list[FlextMeltanoPluginInfo] = []

            if isinstance(plugins_data, dict):
                for plugin_type, plugin_list in plugins_data.items():
                    plugins.extend(self._convert_plugin_list(plugin_type, plugin_list))

            return FlextResult(data=plugins)
        except json.JSONDecodeError:
            return FlextResult(error="Failed to parse plugin list JSON")

    def _convert_plugin_list(
        self,
        plugin_type: str,
        plugin_list: object,
    ) -> list[FlextMeltanoPluginInfo]:
        """Convert plugin list to FlextMeltanoPluginInfo entities."""
        plugins = []
        if isinstance(plugin_list, list):
            for plugin in plugin_list:
                if isinstance(plugin, dict):
                    plugin_info = FlextMeltanoPluginInfo(
                        name=plugin.get("name", ""),
                        type=plugin_type,
                        namespace=plugin.get(
                            "namespace",
                            plugin.get("name", "").replace("-", "_"),
                        ),
                        pip_url=plugin.get("pip_url"),
                        executable=plugin.get("executable"),
                        description=plugin.get("description", ""),
                        version=plugin.get("version"),
                        installed=True,
                    )
                    plugins.append(plugin_info)
        return plugins


# === LEGACY COMPATIBILITY FUNCTIONS ===


def flext_meltano_install_plugin(
    plugin_type: str,
    plugin_name: str,
    project_root: Path | None = None,
    pip_url: str | None = None,
) -> FlextMeltanoResult:
    """Install plugin using installer (legacy compatibility).

    Args:
        plugin_type: Type of plugin (extractors, loaders, etc.)
        plugin_name: Name of the plugin
        project_root: Project directory
        pip_url: Optional pip URL for custom plugins

    Returns:
        Result with installation status

    """
    warnings.warn(
        "flext_meltano_install_plugin is deprecated. Use FlextMeltanoInstaller.add_plugin instead.",
        DeprecationWarning,
        stacklevel=2,
    )

    # Use new service implementation
    config = FlextMeltanoConfig(
        project_root=str(project_root or Path.cwd()),
    )
    installer = FlextMeltanoInstaller(config)

    # Convert FlextResult to legacy FlextMeltanoResult
    result = installer.add_plugin(plugin_type, plugin_name, pip_url)
    if result.is_success:
        return FlextMeltanoResult.ok(result.data)
    return FlextMeltanoResult.fail(result.error or "Unknown error")


# === FACTORY FUNCTION ===


def create_installer_service(
    config: FlextMeltanoConfig,
) -> FlextResult[FlextMeltanoInstaller]:
    """Create installer service using dependency injection."""
    try:
        service = FlextMeltanoInstaller(config)
        init_result = service.initialize()
        if not init_result.is_success:
            return FlextResult(
                error=f"Installer service initialization failed: {init_result.error}",
            )

        return FlextResult(data=service)
    except (ValueError, TypeError, ImportError) as e:
        return FlextResult(error=f"Failed to create installer service: {e}")


# === PUBLIC API ===
__all__ = [
    "FlextMeltanoInstallationContext",
    "FlextMeltanoInstaller",
    "FlextMeltanoPluginInfo",
    "create_installer_service",
    "flext_meltano_install_plugin",
]
