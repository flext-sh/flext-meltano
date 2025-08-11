"""FLEXT Meltano Installation - Plugin Installation and Management."""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from flext_core import FlextResult
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.common_schemas import FlextMeltanoPluginInfo
from flext_meltano.execution import FlextMeltanoExecutor

if TYPE_CHECKING:
    from collections.abc import Sequence


class FlextMeltanoInstallationContext:
    """Installation context for tracking plugin installation metadata."""

    def __init__(
        self,
        plugin_name: str,
        environment: str = "dev",
        installation_metadata: dict[str, object] | None = None,
    ) -> None:
        """Initialize installation context."""
        self.plugin_name = plugin_name
        self.environment = environment
        self.installation_metadata = installation_metadata or {}


# Use centralized FlextMeltanoPluginInfo from common_schemas

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

    def install_plugin(
        self,
        plugin_type: str,
        name: str,
        *,
        version: str | None = None,
        variant: str | None = None,
        pip_url: str | None = None,
        config: dict[str, object] | None = None,
    ) -> FlextResult[FlextMeltanoPluginInfo]:
        """Install plugin with configuration."""
        try:
            # Validate inputs
            if not plugin_type or not name:
                return FlextResult(error="Plugin type and name are required")

            # Create executor for installation
            executor = FlextMeltanoExecutor(self.config)

            # Build installation command
            cmd = ["add", plugin_type, name]
            if version:
                cmd.extend(["--version", version])
            if variant:
                cmd.extend(["--variant", variant])
            if pip_url:
                cmd.extend(["--pip-url", pip_url])

            # Execute installation
            result = executor.run_command(cmd)
            if not result.success:
                return FlextResult(error=f"Plugin installation failed: {result.error}")

            # Create plugin info
            plugin_info = FlextMeltanoPluginInfo(
                name=name,
                type=plugin_type,
                namespace=f"{plugin_type}-{name}",
                description=f"Installed {plugin_type}: {name}",
                version=version or "latest",
                pip_url=pip_url,
                installed=True,
            )

            return FlextResult(data=plugin_info)

        except (OSError, ValueError, TypeError) as e:
            return FlextResult(error=f"Failed to install plugin {name}: {e}")

    def install_plugin_with_context(
        self,
        plugin_type: str,
        name: str,
        context: FlextMeltanoInstallationContext,
        *,
        version: str | None = None,
    ) -> FlextResult[FlextMeltanoPluginInfo]:
        """Install plugin with installation context."""
        # Use context for enhanced installation tracking
        result = self.install_plugin(
            plugin_type,
            name,
            version=version,
        )

        if result.success and result.data:
            # Add context metadata to plugin info
            plugin_info = result.data
            plugin_info.description = f"{plugin_info.description} (env: {context.environment})"

        return result

    def uninstall_plugin(
        self,
        plugin_type: str,
        name: str,
    ) -> FlextResult[bool]:
        """Uninstall plugin."""
        try:
            executor = FlextMeltanoExecutor(self.config)
            cmd = ["remove", plugin_type, name]

            result = executor.run_command(cmd)
            if not result.success:
                return FlextResult(error=f"Plugin removal failed: {result.error}")

            return FlextResult(data=True)

        except (OSError, ValueError) as e:
            return FlextResult(error=f"Failed to uninstall plugin {name}: {e}")

    def list_installed_plugins(self) -> FlextResult[list[FlextMeltanoPluginInfo]]:
        """List all installed plugins."""
        try:
            executor = FlextMeltanoExecutor(self.config)
            result = executor.run_command(["list", "plugins"])

            if not result.success:
                return FlextResult(error=f"Failed to list plugins: {result.error}")

            # Parse plugin list (simplified)
            plugins = []
            if result.data and isinstance(result.data, dict):
                stdout = result.data.get("stdout", "")
                if isinstance(stdout, str):
                    for line in stdout.split("\n"):
                        line = line.strip()
                        if line and not line.startswith("#"):
                            # Parse plugin line (simplified format)
                            parts = line.split()
                            if len(parts) >= 2:  # noqa: PLR2004
                                plugin_type = parts[0]
                                plugin_name = parts[1]
                                plugins.append(FlextMeltanoPluginInfo(
                                    name=plugin_name,
                                    type=plugin_type,
                                    namespace=f"{plugin_type}-{plugin_name}",
                                    installed=True,
                                ))

            return FlextResult(data=plugins)

        except (OSError, ValueError, TypeError) as e:
            return FlextResult(error=f"Failed to list installed plugins: {e}")


def install_plugin(
    plugin_type: str,
    name: str,
    *,
    version: str | None = None,
    config: FlextMeltanoConfig | None = None,
) -> FlextResult[FlextMeltanoPluginInfo]:
    """Install plugin using default configuration."""
    installer_config = config or FlextMeltanoConfig()
    installer = FlextMeltanoInstaller(installer_config)
    return installer.install_plugin(plugin_type, name, version=version)


def create_installer_service(
    config: FlextMeltanoConfig | None = None,
) -> FlextResult[FlextMeltanoInstaller]:
    """Create installer service with configuration."""
    try:
        installer_config = config or FlextMeltanoConfig()
        service = FlextMeltanoInstaller(installer_config)
        validation_result = service.validate()
        
        if not validation_result.success:
            return FlextResult(error=f"Installer validation failed: {validation_result.error}")

        return FlextResult(data=service)

    except (ValueError, TypeError) as e:
        return FlextResult(error=f"Failed to create installer service: {e}")


__all__ = [
    "FlextMeltanoInstallationContext",
    "FlextMeltanoInstaller",
    "FlextMeltanoPluginInfo",
    "create_installer_service",
    "install_plugin",
]