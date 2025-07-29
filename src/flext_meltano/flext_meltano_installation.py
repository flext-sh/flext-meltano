"""FLEXT Meltano Installation - Plugin installation using flext-core patterns.

Installation utilities for FLEXT Meltano plugins using FlextDomainService composition.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from flext_core import FlextDomainService, FlextResult


class FlextMeltanoInstaller(FlextDomainService):
    """Plugin installer for FLEXT Meltano using flext-core patterns."""

    def __init__(self, project_root: Path = Path.cwd()) -> None:
        """Initialize installer with project root."""
        super().__init__()
        self.project_root = project_root

    def execute(self) -> FlextResult[dict[str, Any]]:
        """Execute installer operations using flext-core patterns."""
        return FlextResult(data={
            "installer_type": "flext_meltano",
            "project_root": str(self.project_root),
        })

    def flext_meltano_add_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
        pip_url: str | None = None,
    ) -> FlextResult[bool]:
        """Add plugin to meltano project."""
        try:
            # Build command
            cmd = ["meltano", "add", plugin_type, plugin_name]
            if pip_url:
                cmd.extend(["--custom", pip_url])

            # Execute command
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )

            if result.returncode == 0:
                return FlextResult(data=True)
            error_msg = result.stderr or result.stdout or "Unknown error"
            return FlextResult(error=f"Plugin add failed: {error_msg}")

        except subprocess.TimeoutExpired:
            return FlextResult(error="Plugin add timed out")
        except Exception as e:
            return FlextResult(error=f"Plugin add error: {e}")

    def flext_meltano_install_plugins(self) -> FlextResult[bool]:
        """Install all plugins in meltano project."""
        try:
            # Execute meltano install
            result = subprocess.run(
                ["meltano", "install"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=600,  # 10 minute timeout for installation
                check=False,
            )

            if result.returncode == 0:
                return FlextResult(data=True)
            error_msg = result.stderr or result.stdout or "Unknown error"
            return FlextResult(error=f"Plugin install failed: {error_msg}")

        except subprocess.TimeoutExpired:
            return FlextResult(error="Plugin install timed out")
        except Exception as e:
            return FlextResult(error=f"Plugin install error: {e}")

    def flext_meltano_remove_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
    ) -> FlextResult[bool]:
        """Remove plugin from meltano project."""
        try:
            # Build command
            cmd = ["meltano", "remove", plugin_type, plugin_name]

            # Execute command
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )

            if result.returncode == 0:
                return FlextResult(data=True)
            error_msg = result.stderr or result.stdout or "Unknown error"
            return FlextResult(error=f"Plugin remove failed: {error_msg}")

        except subprocess.TimeoutExpired:
            return FlextResult(error="Plugin remove timed out")
        except Exception as e:
            return FlextResult(error=f"Plugin remove error: {e}")

    def flext_meltano_list_plugins(self) -> FlextResult[dict[str, Any]]:
        """List installed plugins in meltano project."""
        try:
            # Execute meltano list
            result = subprocess.run(
                ["meltano", "list", "--format=json"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )

            if result.returncode == 0:
                import json
                try:
                    plugins_data = json.loads(result.stdout)
                    return FlextResult(data=plugins_data)
                except json.JSONDecodeError:
                    # Fallback to plain text output
                    return FlextResult(data={"output": result.stdout})
            else:
                error_msg = result.stderr or result.stdout or "Unknown error"
                return FlextResult(error=f"Plugin list failed: {error_msg}")

        except subprocess.TimeoutExpired:
            return FlextResult(error="Plugin list timed out")
        except Exception as e:
            return FlextResult(error=f"Plugin list error: {e}")


def flext_meltano_install_plugin(
    plugin_type: str,
    plugin_name: str,
    project_root: Path = Path.cwd(),
    pip_url: str | None = None,
) -> FlextResult[bool]:
    """Install plugin using installer."""
    try:
        installer = FlextMeltanoInstaller(project_root)
        return installer.flext_meltano_add_plugin(plugin_type, plugin_name, pip_url)
    except Exception as e:
        return FlextResult(error=f"Plugin install failed: {e}")


__all__ = [
    "FlextMeltanoInstaller",
    "flext_meltano_install_plugin",
]
